"""Load policy.toml and answer the few questions the engine asks of it."""

from __future__ import annotations

import re
import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Any

DEFAULT = Path(__file__).with_name("policy.toml")


class Policy:
    def __init__(self, data: dict[str, Any]):
        self.data = data
        self.version: str = data["version"]
        self.kinds: dict[str, Any] = data["kinds"]
        self.admissible: dict[str, list[str]] = data["admissible"]
        self.rank: dict[str, int] = data["precedence"]["attestation_rank"]
        self.contemporaneous_days: int = data["precedence"]["contemporaneous_days"]
        self.attended: set[str] = set(data["attendance"]["attended"])
        self.not_attended: set[str] = set(data["attendance"]["not_attended"])
        self.max_scenarios: int = data["counting"]["max_scenarios"]
        self.link: dict[str, Any] = data["link"]
        self.services: dict[str, Any] = data["services"]
        self.refine: set[str] = set(data.get("refine", {}).get("fields", []))
        self.refinements: dict[str, dict[str, list[str]]] = data.get("refine", {}).get("values", {})
        self.not_care: set[str] = set(data["services"].get("not_care", []))
        absence = dict(data.get("absence", {}))
        self.relative: list[str] = list(absence.pop("relative", []))
        self.absence: dict[str, list[str]] = absence

    def is_category(self, field: str, value: object) -> bool:
        """True when the value names a known category for a refinable field."""
        return field == "service" and value in self.services["order"] and value not in self.not_care

    def refined_by(self, field: str, value: object, others: set[Any]) -> bool:
        """True when a more specific value among the others refines this one."""
        if field == "service":
            return not self.is_category(field, value) and any(
                self.is_category(field, v) for v in others
            )
        specifics = self.refinements.get(field, {}).get(str(value), [])
        return any(v in others for v in specifics)

    def field_types(self, kind: str) -> dict[str, dict[str, Any]]:
        return {f["name"]: f for f in self.kinds.get(kind, {}).get("fields", [])}

    def service(self, text: str | None) -> str | None:
        """Canonical service name for a service text (policy keywords), else the text itself."""
        if not text:
            return None
        lowered = text.lower()
        for name in self.services["order"]:
            for keyword in self.services[name]:
                if re.search(rf"\b{re.escape(keyword)}\b", lowered):
                    return str(name)
        return " ".join(lowered.split())

    def categories(self, text: str | None) -> set[str]:
        """Every service category a service text names ("family collateral" -> family, collateral)."""
        if not text:
            return set()
        lowered = text.lower()
        found = {
            name
            for name in self.services["order"]
            for keyword in self.services[name]
            if re.search(rf"\b{re.escape(keyword)}\b", lowered)
        }
        return found or {" ".join(lowered.split())}

    def admits(self, field: str, evidence_kind: str) -> bool:
        return evidence_kind in self.admissible.get(field, [evidence_kind])


@lru_cache(maxsize=4)
def load(path: str | None = None) -> Policy:
    return Policy(tomllib.loads(Path(path or DEFAULT).read_text()))
