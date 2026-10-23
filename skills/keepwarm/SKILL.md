---
name: keepwarm
description: Use when the user types /keepwarm [duration] (for example /keepwarm 3h) or says they are stepping away and want this Claude Code session's prompt cache kept warm until they return.
argument-hint: "[duration, e.g. 3h; default 3h, max 12h]"
---

# keepwarm

Stop the prompt cache from expiring while the user is away, so their first message after the break doesn't rebuild the cache for the whole conversation. Each tick is a small cache read that resets the cache's time-to-live.

**Requires:** Claude Code with the `loop` skill and the `ScheduleWakeup` tool (dynamic `/loop`). Assumes a 1-hour cache TTL. If either tool is missing, tell the user keepwarm isn't supported in this environment and stop.

**Worth it when:** the conversation is long (large context) and the break is between about 1 and 12 hours. For a short conversation, or a break longer than about 12 hours, letting the cache expire costs less than the ticks.

## Start

1. Read the duration from the arguments: `30m`, `3h`, `1h30m` and similar. Default `3h`, maximum `12h`; clamp longer values and say so.
2. Get the current local time with whichever shell is available: `date '+%Y-%m-%d %H:%M %Z'` (bash or zsh) or `Get-Date -Format 'yyyy-MM-dd HH:mm K'` (PowerShell). Add the duration to get the deadline as an absolute timestamp, for example `2026-10-24 18:30 +05:30`.
3. Invoke the `loop` skill in dynamic mode (no interval) with this prompt, with DEADLINE filled in:

   `keepwarm tick, deadline DEADLINE. Check the current time with one shell command. If it is past the deadline, stop the loop (ScheduleWakeup stop: true) and reply "keepwarm ended". Otherwise do no other work, reply with the single word "warm", and call ScheduleWakeup with delaySeconds 3300 and noop true.`

4. Tell the user in one line: keeping the session warm until DEADLINE; any message they send ends it, or they can just carry on working.

## Each tick

- Do only the time check: one shell command for the time, then ScheduleWakeup. No file reads and no other tools, because every token added to the context makes each later tick cost more.
- Use 3300 seconds (55 minutes), not 3600, to leave a margin before the 1-hour expiry.
- If the user sends a real message, stop the loop (ScheduleWakeup stop: true) and handle their message.
