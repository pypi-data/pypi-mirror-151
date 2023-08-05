# discord_limits

### This is a small library that allows you to easily make requests API requests to Discord without having to worry about ratelimits.

---

# Basic usage

```py
import discord_limits
client = discord_limits.DiscordClient()

channel_id = 940366310943125527
client.send_message(channel_id, content="Hello, world!")
```

---
### Based off of:
- [unbelipy](https://github.com/chrisdewa/unbelipy)
- [discord.py](https://github.com/Rapptz/discord.py)