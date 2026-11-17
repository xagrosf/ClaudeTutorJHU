# Exam page: data format and build

Every exam is one self-contained interactive page built from `assets/exam-template.html`. The template's styling and script are fixed. The user likes the design and wants it identical each time, so never edit the template, write the page by hand, or restyle it. You supply content as JSON; `scripts/build_exam.py` fills the template and derives everything that depends on the question count.

What the page does on its own, so you don't need to build any of it: Study mode (a Check answer button per question) and Quiz mode (nothing marked until the whole exam is graded); clicking a selected answer again clears it; strike-out of choices; flags with jump-to-next and a flagged-only filter; sticky progress bar; section jump links; collapsible coverage map and question grid; results with score ring and breakdowns by Bloom level, section and source; review-incorrect-only; retake; light and dark themes; phone layout.

## Build

```
python3 <skill>/scripts/build_exam.py exam.json --audit-only          # validate and count, no page
python3 <skill>/scripts/build_exam.py exam.json --out "Renal Physiology Exam.html"
python3 <skill>/scripts/build_exam.py exam.json sec01.json sec02.json --out exam.html   # sections drafted as separate files
```

Run `--audit-only` after each batch and on the whole set during Stage 4. Errors block the build; fix them in the data. Warnings are for you to judge. The printed audit is the source for the numbers in your reply.

Deliver the built file the way this environment delivers an HTML page to the user (publish it as a page where that exists, otherwise send the .html file). Don't paste the HTML into the chat.

## exam.json

```json
{
  "course": "Renal Physiology",
  "title": "Renal Physiology — Practice Exam",
  "scope_label": "Course notes only",
  "intro_html": "Built from the eight Renal lecture notes and the slide decks for lectures 1 to 5. Weighted toward <b>application</b>: 4 questions need a calculation and 9 are built on a table, figure or experiment.",
  "scope_html": "<b>Scope.</b> Every stem, option and explanation is answerable from the lecture notes. ...",
  "source_noun": "lecture",
  "source_order": ["Body Fluids", "Glomerular Filtration", "Tubular Transport"],
  "sections": [ { "title": "Body Fluids & Filtration", "questions": [ ... ] } ]
}
```

- `course` and `scope_label` form the kicker line above the title, with the question count inserted between them automatically. `scope_label` is two to four words saying what the exam was built from ("Course notes only", "Notes and slides", "USMLE Step 1 style").
- `title` is the heading. `page_title` (optional) is the browser-tab title if it should differ.
- `intro_html` is the paragraph under the heading; `scope_html` is the footer note and starts with `<b>Scope.</b>`. What each must say is in section 14 of `exam-method.md`.
- `source_order` lists the lectures in course order. It sets the order of the coverage map, and every question's source must be in it. The coverage map (lecture, count, question numbers, with integrating questions listed under every lecture they draw on) is computed for you.
- `source_noun` is the word used in the coverage-map heading. Leave it as "lecture" for course exams; use "system" or "topic" for a USMLE-mode exam.
- `sections` can be given here or as separate files on the command line, each holding one section object (or a list of them). Files are taken in the order given.

Never type the question count anywhere. The kicker, counter, mode hints and action bar all read it from the data.

## Sections

Sections follow the lectures in course order. Give a lecture its own section when it has enough questions to stand alone; merge thin or closely related neighbours into one section named for both ("Membrane Traffic & Proteostasis"). Aim for sections of roughly 7 to 16 questions on a long exam. The per-lecture view is not lost by merging: the coverage map and the By-source results panel both work from each question's source tag. Put an integrating question in the section of the lecture it leans on most.

## A question

```json
{
  "stem": "A cell is bathed in 5 mM K<sup>+</sup>. Which change makes E<sub>K</sub> more negative?",
  "table": { "caption": "Ion concentrations", "headers": ["Ion", "Inside (mM)", "Outside (mM)"], "rows": [["K<sup>+</sup>", "150", "5"]] },
  "figure": { "svg": "<svg viewBox=\"0 0 560 350\" ...>...</svg>", "caption": "Inward currents are plotted downward." },
  "options": [
    { "text": "Raising external K<sup>+</sup>", "why": "Shrinks the gradient, so E<sub>K</sub> moves toward zero." },
    { "text": "Lowering external K<sup>+</sup>", "correct": true },
    { "text": "Raising K<sup>+</sup> permeability", "why": "Changes how closely V<sub>m</sub> follows E<sub>K</sub>, not E<sub>K</sub> itself." }
  ],
  "explanation": "E<sub>K</sub> depends only on the concentration ratio; a steeper gradient gives a larger magnitude.",
  "concept": "Equilibrium potential depends on the ratio, not on permeability",
  "bloom": "Apply",
  "source": ["Ion Channels"],
  "quantitative": false,
  "data": false
}
```

- `stem`: the question. `table` and `figure` are optional and appear below it, table first.
- `options`: two to five, in the order they will be shown. Exactly one has `"correct": true`. Every other option needs `why`: one line naming what that option is actually true of, or the error behind it.
- `explanation`: one to three sentences. `concept`: a short phrase naming the concept tested, unique within the exam.
- `bloom`: Remember, Understand, Apply, Analyze or Integrate.
- `source`: the lecture name exactly as in `source_order`. Give two or more for an integrating question. Names can't contain " / ".
- `quantitative`: true when the answer needs a calculation. `data`: true when the question is built on a table, figure or experiment (set automatically when a table or figure is present).

When revealed, the page shows the answer letter, the explanation, why the others are wrong, and a footer with concept, Bloom level, source and type. All of that comes from these fields.

Text fields (`stem`, option `text` and `why`, `explanation`, `concept`, table cells, captions, `intro_html`, `scope_html`) are HTML fragments. Use `<sub>`, `<sup>`, `<i>`, `<b>` for chemistry and emphasis, Unicode for symbols (µ, →, ⁺, −), and write literal `<` and `&` as `&lt;` and `&amp;`. Section titles and source names are plain text.

## Figures

A figure is one complete inline `<svg>` element. No images, no external references, no script.

For x-y figures (traces, time courses, current-voltage plots, dose-response and saturation curves) use the helper, which reproduces the house style:

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from svgfig import line_plot
svg = line_plot(title="...", xlabel="Time (min)", ylabel="Fluorescence (%)",
                xlim=(0, 10), ylim=(30, 100), xticks=[0, 2, 4, 6, 8, 10], yticks=[40, 60, 80, 100],
                series=[{"label": "+ valinomycin", "points": [(0, 100), (1, 100), (4, 45), (10, 40)]},
                        {"label": "no ionophore", "points": [(0, 100), (10, 97)]}],
                vlines=[{"x": 1, "label": "ATP added"}], marks=[{"x": 4, "y": 45, "text": "X"}])
```

For other diagrams (a pedigree, a circuit, a labelled schematic) write the SVG by hand with the same conventions: `viewBox` 560 wide so it scales on a phone, white background, text 11 to 13 px in the system sans font, ink `#14202A`, muted `#5D6C77`, grid `#E3E8EB`, series colours `#0F5F6B`, `#9C4A32`, `#5B4B9A`, line width about 2.4. Tell series apart by dash pattern as well as colour. Figures sit on a white card in both themes, so use these fixed colours and not theme variables.

Rules that matter more than style:

- Draw only what the materials show or state. Reproduce the experiment, curve shape and values from the notes or slides; don't invent data to make a nicer question.
- The figure must carry the answer unambiguously. Put exact values a student needs in the caption or stem as well, since reading a number off a small plot on a phone is unreliable.
- Label parts the options refer to with letters (W, X, Y, Z) and define them in the caption.
- Don't put the answer in the title or caption.

## Before delivering

Open the built page's audit output and confirm: the question count is what was agreed, every lecture in scope has questions, letter counts are balanced, and there are no errors. If the environment has a browser tool, load the page once and check a figure question and a table question render. Then deliver the page and write the reply audit from the script's numbers.
