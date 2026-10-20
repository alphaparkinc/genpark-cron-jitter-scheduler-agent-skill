"""Example usage for Cron Jitter Scheduler Agent."""
from client import CronJitterScheduler
from datetime import datetime

cron = "*/15 * * * *"
now = datetime.now()
is_due = CronJitterScheduler.matches(cron, now)
print(f"Is '{cron}' due at {now}? -> {is_due}")

delay = CronJitterScheduler.calculate_jittered_delay(base_seconds=60.0, jitter_ratio=0.15, seed_str="agent_crawler_42")
print(f"Calculated jittered delay: {delay}s")
