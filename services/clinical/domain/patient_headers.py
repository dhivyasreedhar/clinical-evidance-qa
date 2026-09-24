"""Conservative header identity used for routing; never infer identity from filenames."""

import re
from dataclasses import dataclass
from datetime import date

from clinical.domain.evidence import Source


class UnconfirmedIdentity(ValueError):
    pass


@dataclass(frozen=True)
class PatientHeader:
    mrn: str
    birth_date: date
    display_name: str


def patient_header(source: Source) -> PatientHeader:
    if not source.mrns or not source.birth_dates:
        raise UnconfirmedIdentity("identity_unconfirmed")
    if len(source.mrns) != 1 or len(source.birth_dates) != 1:
        raise UnconfirmedIdentity("conflicting_identifiers")
    mrn = next(iter(source.mrns))
    try:
        birth_date = date.fromisoformat(next(iter(source.birth_dates)))
    except ValueError as exc:
        raise UnconfirmedIdentity("invalid_birth_date") from exc
    if len(mrn) > 100:
        raise UnconfirmedIdentity("invalid_mrn")
    names = set()
    # Only a name on the same identity-header line can become a display label.
    # DOB/MRN remain the grouping keys. No name-only identity resolution.
    for line in source.text.splitlines():
        if "DOB" in line and "MRN" in line and "|" in line:
            prefix = line.split("|", 1)[0].strip().lstrip("\ufeff")
            prefix = re.sub(
                r"^(?:Patient(?: chart| copy)?|Member|Chart routing)\s*:\s*",
                "",
                prefix,
                flags=re.IGNORECASE,
            )
            if not re.search(r"\b(?:MRN|DOB)\b", prefix) and 0 < len(prefix) <= 200:
                names.add(prefix)
    # Ambiguous or absent names remain an identifier label; never pick a guessed person.
    return PatientHeader(mrn, birth_date, next(iter(names)) if len(names) == 1 else mrn)
