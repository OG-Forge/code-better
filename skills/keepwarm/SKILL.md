---
name: keepwarm
description: Use when the user types /keepwarm [duration] (for example /keepwarm 3h) or says they are stepping away and want this Claude Code session's prompt cache kept warm until they return.
argument-hint: "[duration, e.g. 3h; default 3h, max 12h]"
---

# keepwarm

Stop the prompt cache from expiring while the user is away, so their first message after the break doesn't rebuild the cache for the whole conversation. Each tick is a small cache read that resets the cache's time-to-live.

**Requires:**
- Claude Code with self-paced `/loop` (the `ScheduleWakeup` tool). If ScheduleWakeup isn't available, tell the user keepwarm isn't supported here and stop.
- A 1-hour prompt cache. That is the default on Claude subscriptions. On an API key or a cloud provider (Bedrock, Vertex, Foundry), it applies only if `ENABLE_PROMPT_CACHING_1H` or `promptCacheTtl: "1h"` is set; otherwise each tick would rebuild the cache, so tell the user and stop.
- The computer stays awake (plugged in, no sleep or hibernate). If it sleeps for more than an hour, the cache is lost anyway.

**Worth it when:** the conversation is long (large context) and the break is between about 1 and 12 hours. For a short conversation, or a break longer than about 18 hours, letting the cache expire costs less than the ticks (the 12h cap leaves margin).

## Start

1. Read the duration from the arguments: `30m`, `3h`, `1h30m` and similar. Default `3h`, maximum `12h`; clamp longer values and say so.
2. Get the current local time with whichever shell is available: `date '+%Y-%m-%d %H:%M %z'` (bash or zsh) or `Get-Date -Format 'yyyy-MM-dd HH:mm K'` (PowerShell). Add the duration to get the deadline as an absolute timestamp, for example `2026-10-24 18:30 +05:30`.
3. Invoke the `loop` skill in dynamic mode (no interval) with this prompt, with DEADLINE filled in:

   `keepwarm tick, deadline DEADLINE. Check the current time with one shell command. If it is past the deadline, stop the loop (ScheduleWakeup stop: true) and reply "keepwarm ended". If more than 60 minutes have passed since the previous tick, say the cache went cold (the computer probably slept) and stop the loop. Otherwise do no other work, reply with "warm" and the current time (so the next tick can measure the gap), and call ScheduleWakeup with delaySeconds 3000 and noop true.`

4. Tell the user in one line: keeping the session warm until DEADLINE; any message they send ends it, or they can just carry on working.

## Each tick

- Do only the time check: one shell command for the time, then ScheduleWakeup. No file reads and no other tools, because every token added to the context makes each later tick cost more.
- Use 3000 seconds (50 minutes): it leaves margin before the 1-hour expiry, and stays under Claude Code's idle auto-compaction of long conversations (about 54 minutes idle). Users who want no compaction while away can also turn it off in `/config`.
- If the user sends a real message, stop the loop (ScheduleWakeup stop: true) and handle their message.
