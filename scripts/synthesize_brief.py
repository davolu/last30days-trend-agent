"""Turn a last30days raw evidence file into a short brief and five video ideas.

Usage:
    python scripts/synthesize_brief.py ~/Documents/Last30Days/<slug>-raw.md > brief.md

Needs ANTHROPIC_API_KEY in the environment. The key is read, never printed.
"""
import os
import sys
from pathlib import Path

import anthropic

MODEL = os.environ.get("BRIEF_MODEL", "claude-haiku-5-5")
PROMPT = Path(__file__).resolve().parent.parent / "prompts" / "youtube-brief.md"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: synthesize_brief.py <raw evidence .md>")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set")
    raw = Path(sys.argv[1]).expanduser().read_text(encoding="utf-8")
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        system=PROMPT.read_text(encoding="utf-8"),
        messages=[{"role": "user", "content": f"<evidence>\n{raw}\n</evidence>"}],
    )
    print("".join(b.text for b in msg.content if b.type == "text"))
    u = msg.usage
    print(f"\n<!-- model={msg.model} input_tokens={u.input_tokens} "
          f"output_tokens={u.output_tokens} -->", file=sys.stderr)


if __name__ == "__main__":
    main()
