"""Simple Hall of Fame (high scores) implementation backed by JSON.

Keeps a list of top N entries with fields: name, score, date.
Provides load, save, add_entry, and get_top functions.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List

DEFAULT_PATH = Path(__file__).resolve().parent / "hall_of_fame.json"
MAX_ENTRIES = 10


@dataclass
class Entry:
    name: str
    score: int
    date: str


def _ensure_file(path: Path) -> None:
    if not path.exists():
        path.write_text("[]", encoding="utf-8")


def load(path: Path | str = DEFAULT_PATH) -> List[Entry]:
    p = Path(path)
    _ensure_file(p)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        data = []
    entries: List[Entry] = []
    for item in data:
        try:
            entries.append(Entry(name=item.get("name", "Player"), score=int(item.get("score", 0)), date=item.get("date", "")))
        except Exception:
            continue
    entries.sort(key=lambda e: e.score, reverse=True)
    return entries[:MAX_ENTRIES]


def save(entries: List[Entry], path: Path | str = DEFAULT_PATH) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    data = [asdict(e) for e in entries[:MAX_ENTRIES]]
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def add_entry(name: str, score: int, path: Path | str = DEFAULT_PATH) -> None:
    entries = load(path)
    entry = Entry(name=name or "Player", score=int(score), date=datetime.utcnow().isoformat())
    entries.append(entry)
    entries.sort(key=lambda e: e.score, reverse=True)
    save(entries, path)


def get_top(n: int = 10, path: Path | str = DEFAULT_PATH) -> List[Entry]:
    entries = load(path)
    return entries[:n]
