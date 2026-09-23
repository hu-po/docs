# Phase: thumbnail prompt

Write `{{DIR}}/thumbnail_prompt.md` for the stream on {{STREAM_DATE}}. Hugo makes the thumbnail in Google Flow
(Nano Banana Pro, 16:9), so you write the prompts and he generates and picks the image.

1. Read the Thumbnail section of `{{TOOLS}}/FORMAT.md` (house style and past examples). Then read
   `{{DIR}}/deck.json` (title and sections) and the summary in `{{DIR}}/analysis.md`.
2. Find the single visual idea of the week: one image a viewer gets at a glance, with the white bengal
   cat acting it out. It should come from the deck's strongest theme or from what the themes share.
   Avoid clichés (a glowing brain, "AI" text, a handshake).
3. Write three prompts, each with a different idea. Each one covers: scene; the cat's pose and action;
   lighting and palette (dark cinematic lab, teal/cyan and magenta rim light, haze); composition,
   keeping the top-left third clear for the title; and the title text itself, in bold white condensed
   uppercase, top-left, 1–3 words per line. Add a one-line "why this idea" under each.
4. Commit: `git add {{DIR}}/thumbnail_prompt.md && git commit -m "{{STREAM_DATE}} thumbnail prompts"`. Never push.

Hugo saves his chosen image as `{{DIR}}/thumbnail.jpg`. The next `deck.py` build uses it as the title slide.
