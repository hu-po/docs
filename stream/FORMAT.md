# Stream format (living)

Every phase prompt reads this file first. It is the one place the format is defined: change the rules
here, not in the prompts. Record every change in the changelog at the bottom (date + one line why).

## The stream

- Friday livestream, 9–11am CT. Hugo (hu-po) talks over the deck live with a voice agent, and chat joins
  in. Hugo wants to learn *alongside* the audience, so the deck gives him things to react to, not a speech.
- **The shape is data → analysis → deck.** The topic and title come from what the week's sources
  actually contain. Never choose a topic first and then go looking for papers to fit it.
- **Format: figure review.** The best visuals of the week, grouped into emergent themes. The window is
  mostly the last 7 days, but older and historical papers can be pulled in when they tie the week into a
  larger thread (ancestors, callbacks to past streams).

## Deck rules

- **Figures, not text.** A slide is one visual in a white frame (dark frame for dark video), one factual
  context line and one cite line.
- **No commentary.** The context line says what is shown and what the axes or parts mean, taken from
  the authors' own caption. No "notice that", no opinions, no takeaways. Hugo supplies those live.
- **Legible on its own at 1920×1080.** If a figure needs the paper to make sense, or its labels are
  unreadable at slide size, it doesn't go in. Prefer overview/Figure-1 diagrams, result curves with clear
  axes, qualitative sample grids, and project-page videos. Avoid tables of numbers, dense ablation
  grids, portrait strips, and crops that include body text or cut labels.
- **Visuals can come from:** arXiv figures, project pages, GitHub READMEs (videos/GIFs are welcome) and
  launch or blog posts (charts). X screenshots are not used.
- **Themes, not paper order.** Sections are themes that emerge from the week's papers. Each section
  must be droppable on Friday morning without breaking the rest of the deck. A paper can appear in more
  than one section.
- **Section divider:** a title plus a one- or two-sentence blurb saying what ties the section together.
  The blurb is factual and may be provocative, but it states no conclusions.
- **Size:** 3 sections of about 4 papers each, at most 2 visuals per paper: about 20–25 figure slides.
  Small enough for Hugo to review in one sitting and to talk through each paper on stream.
- **Verify everything.** Every arXiv id is resolved against the arXiv API (sweep.py / deck.py do this).
  Never type a title, author or date from memory. Web visuals carry a cite with the source URL.
- **Live, not slides:** model or product launches from the week go in `analysis.json` → `news` for a
  screen-shared cold open. They get no slides unless a launch post has a real chart.

## Thumbnail

16:9, 1376×768, made by Hugo in Google Flow (Nano Banana Pro). House style: a **white bengal cat** in a dark,
cinematic lab (teal/cyan and magenta rim light, haze, monitors, robot arms), acting out the week's idea
visually, with the title in **bold white condensed uppercase, top-left**. Recent examples:
- 09.11 World Action Models: the cat leaping across a lab, trailed by translucent holographic copies of
  itself, one per predicted future frame.
- 09.18 Recursive Self-Improvement: the cat sitting on a lab bench, dreaming a fractal tree made of itself.

## Changelog

- 2026-09-23: file created from the 09.11, 09.18 and 09.25 decks. Topic now comes out of the data, not before
  it. Review gate added. Web media allowed.
- 2026-09-24: cut from 5–8 sections to 3 of about 4 papers, ≤2 visuals each. The 09.25 research came out
  at 9 themes, 58 papers and 168 visuals, too much to review or to stream.
