# Phase: deck (one round)

You are running one round of the **deck loop** for the next hu-po stream. It runs unattended.
Do the round, log it, commit, and exit. The next invocation reads your log and continues.

- Stream folder: `{{DIR}}` (inside a git worktree on its own branch. Never push, and never touch `~/docs`).
- Tools: `{{TOOLS}}` (run them as `{{TOOLS}}/py <tool>.py ...`).
- Read `{{TOOLS}}/FORMAT.md` first. The deck rules there are non-negotiable.
- Read `{{DIR}}/log.md` next (research rounds + deck rounds so far), then `picks.json`, which is Hugo's review.
- Today is {{TODAY}}. The stream is on {{STREAM_DATE}}.

`picks.json` is Hugo's call and overrides your analysis:
`{"title": "...", "themes": {"t1": {"vote": 1|-1, "note": "..."}}, "papers": {"<id>": {"vote": 1|-1,
"note": "...", "figs": ["stem", ...]}}, "notes": "free text"}`.
- vote -1 (veto) → out of the deck. Don't bring it back.
- vote 1 (star) → must be in the deck. A starred paper that isn't in any theme needs a home.
- `figs` → Hugo prefers these visuals for that paper. Use them.
- Notes (per theme, per paper, global) are instructions. Follow them and quote them in the log.
- Unvoted → your judgment, using `analysis.json`.

`deck.json` is the only file you edit to change slides. `{{TOOLS}}/py deck.py {{DIR}}` builds
`slides.html` and the README references, and fails loudly on a missing figure or an unresolvable id.
Its docstring has the schema. The chrome (look and keys) is frozen, so don't edit `slides.html` by hand.

## Round 1: seed (no deck.json yet)

1. **Title → folder.** Use `picks.json` → `title`. If it's empty, use the first title candidate and
   say so in the log. Rename the folder to `YYYY.MM.DD.<snake_case_short_title>` with `git mv`
   (the date prefix stays). All later paths change, so tell the next round in the log. The runner finds
   the folder by date.
2. Write `deck.json`: sections from the non-vetoed themes, ordered for a good first 10 minutes (the
   strongest and most visual theme first, the quietest last), and slides from each paper's picked or
   best visuals. Write each `ctx` line from the figure's caption in `figures/captions.json` (open the
   figure to be sure the line matches what is shown). Write each section blurb.
3. Build and look. Open at least one new slide's image of each kind (arXiv figure, web image, video poster).

## Later rounds: improve

Each round, pick the 2–4 highest-value changes:
- **Weakest slides first.** Open the figures. Replace or recrop anything that fails the legibility rule
  (`figures.py crop`, a different figure number, or a project-page visual), and log the reason.
- **Missing visuals.** For starred papers with a project page or GitHub repo, check for a better
  video/GIF (`figures.py page` / `get`).
- **Order and flow.** Within a section, go overview → result → failure/limitation. Put visually
  contrasting neighbours next to each other.
- **Blurbs and ctx lines.** Make them factual and tighter. Make sure no line interprets or editorializes.
- **Size.** Stay inside FORMAT.md's range. Cut the weakest figure before adding one.
- Re-check any picks note you haven't satisfied yet.

## End of every round

1. `{{TOOLS}}/py deck.py {{DIR}}` must print a slide count with no errors. If you can't make it green
   in 10 minutes, `git checkout -- deck.json`, log the failure, and exit. A broken deck is worse than a
   missed round. `slides.html` may be open on Hugo's screen.
2. Append to `log.md`:
   ```
   ## Deck round N — <output of `date '+%F %H:%M'`>
   + <stem> (<section>): <why>
   − <stem>: <why>
   ~ <what else changed>
   Picks notes addressed: <which>
   Slides: <total> · Sections: <n> · Papers: <n>
   ```
3. `git add -A {{DIR}} && git commit -m "{{STREAM_DATE}} deck round N: +<k> −<j>"`. Never push.
4. Print a 3-line summary and exit.

## Stop

After round {{MAX_ROUNDS}}, or once the deck is inside the size range with no weak slides left, do a
**polish round**. It adds nothing: reorder for flow, tighten lines, fix any flagged crop, and run
`figures.py qa` on every stem in the deck. Then append `DECK DONE` as the last line of `log.md` and
exit. If that line is already there, exit immediately.
