from __future__ import annotations

import json
from pathlib import Path

from app.models import ResourceLink

_RESOURCES_PATH = Path(__file__).resolve().parent.parent / "data" / "dwave_resources.json"


def links_for_class(class_id: str, limit: int = 5) -> list[ResourceLink]:
    with _RESOURCES_PATH.open(encoding="utf-8") as f:
        raw = json.load(f)
    matched = [r for r in raw if r["problem_class"] in (class_id, "*")]
    out: list[ResourceLink] = []
    for r in matched[:limit]:
        out.append(ResourceLink(title=r["title"], url=r["url"], kind=r["kind"]))
    return out
