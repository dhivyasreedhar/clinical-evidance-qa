"""Structured model calls, cached on disk by a hash of everything that shapes the output."""

from __future__ import annotations

import contextvars
import hashlib
import json
import os
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, TypeVar

WRITER = os.environ.get("RECORD_ENGINE_WRITER", "claude-sonnet-4-6")
SMALL = os.environ.get("RECORD_ENGINE_SMALL", "claude-haiku-4-5-20251001")
PLANNER = os.environ.get("RECORD_ENGINE_PLANNER", WRITER)
# list prices in USD per million tokens (input, output); anything else is costed at the writer's
PRICES: dict[str, tuple[float, float]] = {
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5-20251001": (1.0, 5.0),
}


def cost(model: str, input_tokens: int, output_tokens: int) -> float:
    price_in, price_out = PRICES.get(model, PRICES["claude-sonnet-4-6"])
    return (input_tokens * price_in + output_tokens * price_out) / 1_000_000


CACHE = Path(os.environ.get("RECORD_ENGINE_CACHE", ".local/record_engine/cache"))


class ModelError(RuntimeError):
    pass


# Set by a host application (the clinical service passes its configured key); otherwise the key
# comes from the environment or .env.
KEY: str | None = None


def api_key() -> str:
    key = KEY or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("EHR_ANTHROPIC_API_KEY")
    if not key and Path(".env").exists():
        for line in Path(".env").read_text().splitlines():
            if line.startswith(("EHR_ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=")):
                key = line.split("=", 1)[1].strip()
    if not key:
        raise ModelError("no Anthropic API key (ANTHROPIC_API_KEY or .env)")
    return key


class Usage:
    """Calls, tokens and cost. `cost_usd` is what this run paid; `full_cost_usd` adds what the
    cached calls cost when they were first made (known for calls cached with their usage)."""

    def __init__(self) -> None:
        self.calls = 0
        self.cached = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.cost_usd = 0.0
        self.cached_cost_usd = 0.0
        self.cached_seconds = 0.0  # model time the cached calls took when first made
        self.by_stage: dict[str, int] = {}
        self.lock = threading.Lock()

    def add(self, stage: str, model: str, usage: dict[str, Any] | None, cached: bool) -> None:
        with self.lock:
            spent = cost(model, usage["input"], usage["output"]) if usage else 0.0
            if cached:
                self.cached += 1
                self.cached_cost_usd += spent
                self.cached_seconds += float((usage or {}).get("seconds") or 0.0)
                return
            self.calls += 1
            self.input_tokens += usage["input"] if usage else 0
            self.output_tokens += usage["output"] if usage else 0
            self.cost_usd += spent
            self.by_stage[stage] = self.by_stage.get(stage, 0) + 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "calls": self.calls,
            "cached": self.cached,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cost_usd": round(self.cost_usd, 4),
            "full_cost_usd": round(self.cost_usd + self.cached_cost_usd, 4),
            "cached_seconds": round(self.cached_seconds, 1),
            "by_stage": self.by_stage,
        }


USAGE = Usage()
_SCOPE: contextvars.ContextVar[tuple[Usage, ...]] = contextvars.ContextVar(
    "usage_scope", default=()
)


@contextmanager
def scope() -> Iterator[Usage]:
    """Usage of the calls made inside the block (per question, per build), besides the total.
    Scopes nest: a call counts toward every open scope (a question inside a scenario)."""
    usage = Usage()
    token = _SCOPE.set((*_SCOPE.get(), usage))
    try:
        yield usage
    finally:
        _SCOPE.reset(token)


T = TypeVar("T")
R = TypeVar("R")


def carry(fn: Callable[[T], R]) -> Callable[[T], R]:  # noqa: UP047 - TypeVar form, as in the rest of the engine
    """`fn` for a worker thread, running in the caller's context so its calls reach the open
    scopes (threads do not inherit context variables)."""
    context = contextvars.copy_context()
    return lambda x: context.copy().run(fn, x)


def _record(stage: str, model: str, usage: dict[str, Any] | None, cached: bool) -> None:
    USAGE.add(stage, model, usage, cached)
    for current in _SCOPE.get():
        current.add(stage, model, usage, cached)


# Every call is deterministic (temperature 0) unless a block asks for an independent sample:
# the second reading of a document, or a separate run for the stability evaluation. `trial`
# makes such a call a fresh one instead of a cache hit of an earlier identical call.
_SAMPLING: contextvars.ContextVar[tuple[float, str]] = contextvars.ContextVar(
    "sampling", default=(0.0, "")
)


@contextmanager
def sampling(temperature: float = 0.0, trial: str = "") -> Iterator[None]:
    """Calls inside the block use this temperature and cache under this trial. A trial nests
    inside an outer one ("run2" + "reading-b" = "run2/reading-b")."""
    outer = _SAMPLING.get()[1]
    token = _SAMPLING.set((temperature, "/".join(t for t in (outer, trial) if t)))
    try:
        yield
    finally:
        _SAMPLING.reset(token)


def call(
    stage: str,
    system: str,
    user: str,
    schema: dict[str, Any],
    model: str = WRITER,
    max_tokens: int = 16000,
) -> dict[str, Any]:
    """Return the JSON object the model submits through a forced tool call."""
    temperature, trial = _SAMPLING.get()
    key = hashlib.sha256(
        json.dumps(
            [model, system, user, schema, max_tokens, temperature, trial], sort_keys=True
        ).encode()
    ).hexdigest()
    path = CACHE / f"{key}.json"
    if path.exists():
        entry = json.loads(path.read_text())
        _record(stage, entry.get("model", model), entry.get("usage"), cached=True)
        cached: dict[str, Any] = entry["output"]
        return cached
    import anthropic

    client = anthropic.Anthropic(api_key=api_key(), max_retries=3, timeout=600)
    started = time.monotonic()
    last: Exception | None = None
    for attempt in range(3):
        try:
            with client.messages.stream(
                model=model,
                max_tokens=max_tokens,
                # the SDK no longer names sampling parameters; the API accepts them in the body
                extra_body={"temperature": temperature},
                system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": user}],
                tools=[
                    {
                        "name": "submit",
                        "description": "Submit the result as JSON. It performs no action.",
                        "input_schema": schema,
                    }
                ],
                tool_choice={"type": "tool", "name": "submit"},
            ) as stream:
                message = stream.get_final_message()
            break
        except anthropic.APIStatusError as error:  # pragma: no cover - network
            last = error
            time.sleep(10 * (attempt + 1))
    else:  # pragma: no cover - network
        raise ModelError(f"{stage}: {last}")
    if message.stop_reason == "max_tokens":
        raise ModelError(f"{stage}: output truncated at {max_tokens} tokens")
    output: dict[str, Any] = next(b.input for b in message.content if b.type == "tool_use")
    usage = {
        "input": message.usage.input_tokens,
        "output": message.usage.output_tokens,
        "seconds": round(time.monotonic() - started, 2),
    }
    _record(stage, model, usage, cached=False)
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "model": model,
                "stage": stage,
                "temperature": temperature,
                "trial": trial,
                "usage": usage,
                "output": output,
            }
        )
    )
    return output


def as_list(value: Any, keys: tuple[str, ...] = ()) -> list[Any]:
    """A list the model may have serialized as text (or cut off): parse it, or keep every complete
    object in it; items that are themselves serialized objects are parsed too. With keys, only
    objects holding one of them are kept."""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            decoder = json.JSONDecoder()
            found: list[Any] = []
            pos = value.find("{")
            while pos != -1:
                try:
                    item, end = decoder.raw_decode(value, pos)
                except json.JSONDecodeError:
                    pos = value.find("{", pos + 1)
                    continue
                if isinstance(item, dict) and (not keys or any(k in item for k in keys)):
                    found.append(item)
                    pos = value.find("{", end)
                else:
                    pos = value.find("{", pos + 1)
            value = found
    if not isinstance(value, list):
        value = [value] if value else []
    out = []
    for item in value:
        if isinstance(item, str) and item.lstrip().startswith("{"):
            try:
                item = json.loads(item)
            except json.JSONDecodeError:
                continue
        if isinstance(item, dict):
            out.append(item)
    return out
