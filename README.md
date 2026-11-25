# last30days trend agent

Companion code for the Agentic AI Hub video **"Let's Build an AI Trend Research Agent with last30days"**.

[last30days](https://github.com/mvanhorn/last30days-skill) is an open-source (MIT) Agent Skill and Python engine. It researches a topic across public sources for the last 30 days, ranks what people actually engaged with, and saves a raw evidence file. This repo adds a small script that turns that evidence file into a short brief and five YouTube video ideas, each tied to a source.

Everything here was run on 25 Nov 2026 with last30days **v4.6.0**.

## What you need

- Python 3.12 or newer (last30days refuses older versions)
- Node.js (first-run setup installs some free CLIs with `npx`)
- Git
- An Anthropic API key, only for the brief step

## 1. Install last30days and run setup

```bash
git clone https://github.com/mvanhorn/last30days-skill.git
cd last30days-skill
git checkout v4.6.0
python3 skills/last30days/scripts/last30days.py setup
```

Plain `setup` reads nothing from your browser. It installs the free yt-dlp, Digg, arXiv, Techmeme and Yahoo Finance helpers when it can. Browser-cookie access is a separate opt-in (`setup --allow-browser-cookies`) and is not used here.

If setup creates `~/.config/last30days/.env`, lock it down:

```bash
chmod 600 ~/.config/last30days/.env
```

## 2. Check what is on

```bash
python3 skills/last30days/scripts/last30days.py --preflight
```

Preflight lists the available sources and confirms browser cookies are off. It never prints key values.

Want to be sure no keys from your shell reach the engine? Use `scripts/run_clean.sh` from this repo as a prefix:

```bash
../last30days-trend-agent/scripts/run_clean.sh python3 skills/last30days/scripts/last30days.py --preflight
```

## 3. Discover what's trending

```bash
python3 skills/last30days/scripts/last30days.py --discover "AI" --save-dir ~/Documents/Last30Days
```

If nothing clears the engine's confidence floor, it says "Nothing solid this window" instead of inventing topics.

## 4. Deep-research one topic

```bash
python3 skills/last30days/scripts/last30days.py "AI-generated code open source" \
  --days 30 --store --save-dir ~/Documents/Last30Days
```

This writes `~/Documents/Last30Days/ai-generated-code-open-source-raw.md`. `--store` also saves findings to a local SQLite database for the watchlist.

## 5. Write the brief

```bash
cd ../last30days-trend-agent
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then add your key, or export it in your shell
export ANTHROPIC_API_KEY=... # never commit or print it
python scripts/synthesize_brief.py ~/Documents/Last30Days/ai-generated-code-open-source-raw.md > brief.md
```

The prompt is in [`prompts/youtube-brief.md`](prompts/youtube-brief.md). It tells the model to copy numbers exactly from the evidence and to flag low-confidence dates. Token usage is printed to stderr.

On the recording day, one call to `claude-haiku-5-5` used 19,109 input and 902 output tokens. At the list prices on 25 Nov 2026 ($0.10 / 1M input, $0.50 / 1M output, prompts under 100,000 tokens), that is about $0.0024. See [`examples/sample-brief.md`](examples/sample-brief.md) for the output.

## 6. Rerun it weekly

```bash
cd ../last30days-skill
python3 skills/last30days/scripts/watchlist.py add "AI-generated code open source" --weekly
python3 skills/last30days/scripts/watchlist.py run-one "AI-generated code open source"
python3 skills/last30days/scripts/briefing.py generate --weekly
```

`--weekly` only stores the schedule. Attach a real scheduler: see [`examples/crontab.example`](examples/crontab.example).

## Sources used (free, no key)

| Source | What you need |
|---|---|
| Hacker News | nothing |
| Reddit (public) | nothing (some networks get HTTP 403 from Reddit search; the engine reports it) |
| Polymarket | nothing |
| GitHub (public) | nothing; a token only raises rate limits |
| YouTube | yt-dlp (installed by setup) |
| arXiv, Techmeme, Digg | free CLIs installed by setup |

Sources that need paid keys, credits or signed-in sessions (X, TikTok, Instagram, LinkedIn, Perplexity, Amazon reviews) are not used. See the official last30days README for the full list.

## Files

- `prompts/youtube-brief.md`: the brief prompt
- `scripts/synthesize_brief.py`: raw evidence file in, brief out
- `scripts/run_clean.sh`: run last30days with no keys in the environment
- `examples/crontab.example`: weekly schedule example (not installed)
- `examples/sample-brief.md`: the brief from the recording day
- `.env.example`: the one variable this repo uses

## Credits

- [last30days](https://github.com/mvanhorn/last30days-skill) by Matt Van Horn, MIT
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)

MIT licence for the code in this repo.
