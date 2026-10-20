"""Cron Jitter Scheduler Agent.
100% Python Standard Library.
"""
from datetime import datetime

class CronJitterScheduler:
    """Crontab syntax parser and distributed jittered task scheduler."""

    @staticmethod
    def _parse_field(field_str: str, min_val: int, max_val: int) -> set:
        res = set()
        for part in field_str.split(","):
            if part == "*":
                return set(range(min_val, max_val + 1))
            if "/" in part:
                subparts = part.split("/")
                step = int(subparts[1])
                start_range = range(min_val, max_val + 1) if subparts[0] == "*" else range(int(subparts[0]), max_val + 1)
                for v in start_range:
                    if (v - (min_val if subparts[0] == "*" else int(subparts[0]))) % step == 0:
                        res.add(v)
            elif "-" in part:
                s, e = map(int, part.split("-"))
                res.update(range(s, e + 1))
            else:
                res.add(int(part))
        return res

    @classmethod
    def matches(cls, cron_expr: str, dt: datetime = None) -> bool:
        dt = dt or datetime.now()
        parts = cron_expr.strip().split()
        if len(parts) != 5:
            raise ValueError("Cron expression must have exactly 5 parts: min hour day month dow")

        m_set = cls._parse_field(parts[0], 0, 59)
        h_set = cls._parse_field(parts[1], 0, 23)
        dom_set = cls._parse_field(parts[2], 1, 31)
        mon_set = cls._parse_field(parts[3], 1, 12)
        dow_set = cls._parse_field(parts[4], 0, 6)

        py_dow = (dt.weekday() + 1) % 7

        return (dt.minute in m_set and
                dt.hour in h_set and
                dt.day in dom_set and
                dt.month in mon_set and
                (py_dow in dow_set or dt.weekday() in dow_set))

    @classmethod
    def calculate_jittered_delay(cls, base_seconds: float, jitter_ratio: float = 0.2, seed_str: str = "task") -> float:
        h = sum(ord(c) for c in seed_str)
        factor = ((h % 1000) / 500.0 - 1.0) * jitter_ratio
        return round(max(0.0, base_seconds * (1.0 + factor)), 3)
