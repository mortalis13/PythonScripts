# Collects total OS uptime by day for the last N days
# Uses Windows Event Log data for getting event IDs
# 6005 (The Event log service was started.) and
# 6006 (The Event log service was stopped.)

import win32evtlog
import datetime
from collections import defaultdict

# pip install pywin32

DAYS = 7

STARTUP_ID = 6005
SHUTDOWN_ID = 6006

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=DAYS)

# Open the system event log
server = 'localhost'
log_type = 'System'
hand = win32evtlog.OpenEventLog(server, log_type)

# Read all events (batch size = 1024)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
events = []
while True:
  records = win32evtlog.ReadEventLog(hand, flags, 0)
  if not records:
    break
  for event in records:
    # Normalize 32 bit signed value to 16 bit event ID stored in the Event Log
    norm_id = event.EventID & 0xffff
    if norm_id in (STARTUP_ID, SHUTDOWN_ID) and start_date <= event.TimeGenerated <= end_date:
      events.append({
        'EventID': norm_id,
        'Time': event.TimeGenerated
      })

# Sort by time ascending
events = sorted(events, key=lambda e: e['Time'])

# Match startup/shutdown events
sessions = []
startup_stack = []
for event in events:
  if event['EventID'] == STARTUP_ID:
    startup_stack.append(event['Time'])
  elif event['EventID'] == SHUTDOWN_ID and startup_stack:
    start_time = startup_stack.pop()
    end_time = event['Time']
    if start_time < end_time:
      sessions.append((start_time, end_time))

# Aggregate daily uptime
daily_uptime = defaultdict(float)  # day → seconds
for start, end in sessions:
  day = start.date()
  uptime_seconds = (end - start).total_seconds()
  daily_uptime[day] += uptime_seconds

# Print results
print(f"{'Date':<14} {'Uptime':<10}")
print(f"{'-'*12}   {'-'*10}")

total_hours = 0
for day in sorted(daily_uptime, reverse=True):
  hours = int(daily_uptime[day] // 3600)
  minutes = int((daily_uptime[day] % 3600) // 60)
  print(f"{str(day):<14} {hours:02d}:{minutes:02d}")
  total_hours += hours

print(f"\nTotal [{DAYS} days]: {total_hours} hours")
