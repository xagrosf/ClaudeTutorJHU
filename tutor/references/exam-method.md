# Practice exam method

How to write a practice exam or question set that matches a course. Read this whole file before starting. The page format and build commands are in `exam-page.md`; read that when you reach Stage 6.

Contents: 1. What the exam is for. 2. What is fixed and what is derived. 3. Sources and priority. 4. Source boundaries. 5. Style. 6. Mix and difficulty. 7. Quantitative items. 8. Data and figure items. 9. Answer choices. 10. Answer length and position (hard rules). 11. Coverage. 12. Pipeline. 13. Quality checklist. 14. What goes in the page and what goes in the reply. 15. USMLE variant.

## 1. What the exam is for

A student who understands the course materials should do well, and one who memorized term lists should struggle. Difficulty comes from discrimination between close ideas and from reasoning, never from obscurity, pathway recall, or arithmetic. Each question has one clearly best answer, with no gotchas and no ambiguous wording. A practice exam that tests things the real one won't, or that can be passed by test-taking tricks, trains the wrong thing and gives a false score.

## 2. What is fixed and what is derived

The rules in this file are the method and apply to every course. Everything specific to a course is derived fresh from the user's materials in Stages 0 and 1, and never carried over from another course or assumed from general knowledge of the subject:

- the lecture list, and which sources exist for each lecture
- lecturer scope signals ("do not memorize", "not covered", "general concepts are asked")
- instructor-flagged concepts
- the equations and constants the materials actually use
- the clinical or applied contexts the materials use
- the confusion sets (groups of ideas students mix up) that distractors are drawn from
- which lectures deserve more weight

Two things are not derived but asked: how many questions to generate, and what content to base them on. That is the Intake step at the start of the pipeline (section 12).

## 3. Sources and priority

Work out which of these the user has provided, and rank them in this order unless the course itself says otherwise:

1. **The primary source**: whatever the course treats as authoritative, usually lecture notes or handouts. A stated list of objectives at the top of a lecture defines its scope.
2. **The secondary source**: usually slides. A closing "you should be able to" list counts as objectives. If a lecture has no slides, say "slides: not available" and work from the primary source. Never invent what a missing source might contain.
3. **The instructors' own questions** (review quizzes, past exams, practice sets), when provided: the model for style, format mix and difficulty, and a list of concepts the instructors have already flagged as exam-relevant. Check their date against the current materials. If the materials have been revised since, confirm each flagged concept still appears before testing it.

If it isn't clear which source the course treats as authoritative, ask at the map stage.

When sources disagree, the primary source wins on content, but don't silently pick. Flag the conflict in the map and in the page's scope note, and avoid the question unless it can be written so that both sources support the answer. The user should learn about the conflict from you, not from a wrong answer on the real exam.

## 4. Source boundaries

**Every question maps to a stated objective of a specific lecture.** The objective is what keeps the exam in scope. If a lecture states no objectives, derive candidates from its headings, summaries and take-home statements, mark them "derived" in the map, and let the user confirm them.

**Test concepts and logic, not minutiae.** Don't test step-by-step pathway detail: ordered lists of intermediates, which enzyme or adaptor acts at which step, specific names inside a cascade, the location of each step. If a pathway specific is tested, the stem must supply enough (what each component does, what was removed or mutated) that a student with little background can reason to the answer from the logic. Prefer "what happens to the output", "which direction does it shift", "which component is upstream" over "which protein does X". The same holds outside biology: test whether the student can use the idea, not whether they can recite the list.

Narrow exception: a one-step role of a named component is fair when it appears in an objective or in the instructors' own questions, because the instructors have shown they test it. Multi-step sequences and long lists stay out.

**No outside facts.** If it is not in the materials, don't test it, and don't let a stem or a distractor depend on it. This is stricter than tutoring, where flagged outside knowledge is fine. In an exam, an outside fact in a distractor makes the question unanswerable from the course, and the user can't tell which questions to trust.

**Respect lecturer scope signals.** Where a lecturer says something won't be asked, or that only general concepts are asked, or marks a table "do not memorize", follow it exactly. Record each signal in the map so the user can see it was read.

**No trivia.** Copy numbers, residue counts, masses, consensus sequences, speeds and sizes outside a calculation the materials model, reading assignments, lecturer names, dates and historical anecdotes.

**Applied contexts come from the materials.** Clinical or real-world examples the materials use are fair contexts. The question tests what the objective tests: in a basic-science course that means the mechanism, not diagnosis or management, unless the objectives include those.

## 5. Style

**When the user provides the instructors' questions**, model on them, and measure before writing instead of assuming: typical stem length, the share that are short scenarios, the formats used (single best answer, NOT/EXCEPT, sentence completion, numbered items with combination answers, classification items), how many options, how often "all of the above" or "none of the above" appears and how often it is correct, and what their quantitative items look like. Reproduce those proportions. When a special option like "all of the above" is used, make it correct about half the time, never by default. Write new questions on the instructors' concepts from a different angle; never copy their questions or option sets.

**When there are no instructor questions**, say so in the map and use these defaults: five options, single best answer, short direct stems with about one in four a short scenario or applied-reasoning item, no "all/none of the above", NOT/EXCEPT in at most 10% of items with the word in capitals.

In both cases:

- Keep scenarios lean. Add a value or detail only if it carries information.
- Wrong options teach. In each distractor's "why this is wrong" line, name what the option is actually true of ("that describes primary active transport", "that applies to the intrinsic pathway"), or for a calculation distractor, the error that produces it.
- Explanations are one to three sentences on why the answer is correct, tied to the materials. Calculations are shown in one or two short lines with units.

## 6. Mix and difficulty

There are two profiles. Offer both when you show the map and let the user choose each time; don't pick for them.

| | Standard | Application-heavy |
|---|---|---|
| Remember / Understand | ~30% | ~15%, no pure recall |
| Apply | ~40% | ~40% |
| Analyze | ~20% | ~35% |
| Integrate (two or more lectures in one stem) | ~10% | ~10% |
| Quantitative | ~3-5% | ~10-15% |
| Data / figure / experiment | ~10% | ~30% |

Tag each question with one of: Remember, Understand, Apply, Analyze, Integrate.

The quantitative and data shares are ceilings set by the materials, not quotas. Place quantitative items only in lectures where the materials compute something, and don't invent calculations for qualitative lectures. If the course is not quantitative, say so in the map and drop that row.

Integrating stems link lectures the materials themselves link (a disease, a process or a structure that appears in more than one lecture). Don't force a link the course doesn't make.

## 7. Quantitative items

Keep the math light. The exam tests whether the student knows which quantity matters and which way it moves, not whether they can do arithmetic under time pressure.

- Solvable by mental math in about 20 seconds: round numbers, ratios of 10 or 100, values that divide evenly, one step and at most two.
- No unit-conversion chains. Give all quantities in the units the options use.
- Prefer direction and relative magnitude ("more positive", "doubles", "which term dominates") over computed numbers. A numeric answer should be recognizable from a reference value or a simple ratio.
- Use only the equations and constants the materials give, in the form the materials give them, and keep the arithmetic below the level of the materials' own worked examples. List them in the map.
- Numeric distractors are visibly different from each other, and each comes from a nameable mistake (wrong sign, inverted ratio, a dropped factor). List numeric options in ascending order.

## 8. Data and figure items

Data items are read qualitatively or by simple comparison (up or down, before and after, with and without, which condition differs), not by computing. State the data precisely, with units, so the answer follows from the data.

The page supports data tables and figures, so when a trace, plot, or diagram would help, draw it as an SVG figure in the question instead of describing it in words. Build figures and tables only from what the materials show or state: the experiments, curves and values that appear in the notes or slides. A figure is data, and invented data is an outside fact. `exam-page.md` covers how to draw them.

## 9. Answer choices

Distractors come from the same conceptual neighborhood as the answer and represent real conceptual errors, not arithmetic slips or obscure swaps. The source for them is the course's confusion sets, derived in Stage 1: for each topic, the neighboring ideas a student is likely to mix up with it, each with a property that is correctly stated but doesn't fit this question. Typical shapes of a confusion set:

- the sibling category with its own true property (the other transporter class, the other polymer, the parallel pathway)
- the same quantity with the wrong sign, direction or reciprocal
- the neighboring step, compartment or signal
- gain versus loss, upstream versus downstream, cause versus consequence
- two terms that sound alike or that the materials introduce together

Avoid distractors from unrelated lectures and distractors that can be eliminated by terminology alone. Give extra weight to confusion pairs and to instructor-flagged concepts when choosing what to test.

## 10. Answer length and position (hard rules)

The failure these rules prevent: the correct answer is usually the longest, most detailed, most qualified option, so a student can pass by picking it without knowing the material. That makes the score meaningless. In instructors' real questions the correct answer is often short and the long options are often wrong.

1. Build options as minimal pairs. Write the correct answer, then make each distractor by changing one element of it, keeping the same grammatical frame, level of specificity and length. Word counts of all options in a question fall within about 20% of each other, or within 3 words, whichever is larger.
2. Put the discriminating detail in the stem where possible, so options are short and parallel.
3. The correct answer must not be the only option with a "because / by / which" clause, a named entity, a number, a qualifier ("only", "primarily", "in the absence of"), or extra jargon. If one option has such an element, at least two others get the same kind.
4. Distractors may be, and often should be, the most detailed and technical-sounding option. Across the five-option questions, the correct answer is the single longest option in no more than 20% and the shortest or tied-shortest in at least 20%.
5. Don't hedge only the correct answer ("can", "may", "in some cases") and don't put absolutes ("always", "never") only in distractors. Use absolutes in correct answers sometimes and hedges in distractors sometimes.
6. Position: decide the correct letter before writing the options, from a schedule made for the whole exam with each letter near an equal share and no letter more than twice in a row. Don't default to C or D. Where options have a natural order (ascending numbers, sequence steps), keep that order and let the letter fall where it falls. Letters are fixed in the page; it does not shuffle.
7. Self-test every question: cover the stem and ask whether the answer could be guessed by choosing the longest, the most specific, the odd one out, or the "all of the above". If yes, rewrite.

`scripts/build_exam.py --audit-only` counts all of this. Use its numbers; don't estimate.

## 11. Coverage

- Every covered lecture gets at least one question. Weight toward lectures with dense mechanistic or quantitative objectives and away from descriptive ones, unless the user says otherwise. Propose the per-lecture counts in the map.
- Don't test the same fact twice in different wording.
- Every instructor-flagged concept still present in the current materials gets at least one new question.

## 12. Pipeline

Run the stages in order and don't skip any. For a long exam, work section by section and write each finished section to its own file as you go, so drafts don't exist only in the conversation.

**Intake. Ask before anything else.** In one message, ask the user:

1. How many questions they want generated.
2. What content the exam should be based on: which lectures, units, files or topics, and which of their materials to draw from if there is more than one kind (notes, slides, instructor questions).

Ask this every time, and wait for the answer before Stage 0. To make the second question easy to answer, take a quick look at what materials are available (file and lecture names only, not a deep read) and list them, so the user can pick from the list instead of typing names. If the request already states the count or the content, restate it in the same message for confirmation instead of asking it open-ended. If they answer "everything", say back what everything is by name. If the environment has a tool for asking the user structured questions, use it.

Don't guess either answer and don't fall back to a default. The count sets the per-lecture weights and how thin coverage gets, and the content sets what the inventory and map are built on, so a wrong assumption is carried through every later stage. The mix profile is a separate choice, made when the map is shown.

**Stage 0. Inventory.** For each lecture in the content the user chose, list which sources exist: primary source, secondary source, objectives list, instructor questions. Say what is missing. Do not fill gaps from general knowledge.

**Stage 1. Exam-signal map.** For each lecture: objectives mapped to testable concepts; instructor-flagged concepts that belong to it; lecturer scope signals; anything the secondary source emphasizes that the primary does not ("slide-only"). For the course as a whole: the equations and constants the materials use, the usable clinical or applied contexts, the confusion sets, the links between lectures that the materials themselves make (the basis for integrating questions), and source conflicts found.

**Confirmation gate.** Show the user the map and wait for their confirmation before drafting anything. Keep it compact enough to check in a few minutes: one row per lecture (sources available, proposed question count, scope signals, flagged concepts), then the course-wide lists, the proposed section grouping, and the two mix profiles to choose from. Ask them to correct anything wrong. Every later stage is built on this map, so an error here costs the whole exam, while fixing it here costs one message.

**Stage 2. Draft.** Write questions following the confirmed map, the style rules, the chosen mix and the letter schedule.

**Stage 3. Exam-relevance cross-reference.** For every draft, find three anchors: (a) the lecture objective, (b) the passage in the primary source (section or page), (c) the place in the secondary source (deck and slide number). Keep these in a working log; the user may ask to see it. Then give a verdict:

- Objective + primary + secondary: keep.
- Objective + primary, and the lecture has no secondary source: keep, marked "single source".
- Objective + primary, but a secondary source exists and never mentions the concept: keep only if the primary source treats it as core (in the objectives or a clear take-home); otherwise rewrite toward a concept both sources support, or drop.
- In the secondary source only: keep only if it is in that source's objectives list, and only if the answer doesn't depend on outside knowledge.
- In neither source, contradicted by either, inside a "do not memorize" or "not covered" area, or a flagged concept no longer in the current materials: drop and replace.
- Sources conflict: flag it, and avoid the question unless both support the answer.

Then check every option, not only the answer. A distractor that is actually true according to the materials makes the question ambiguous; fix or replace it. Finally, confirm every instructor-flagged concept present in the current materials has a question, and list any that are absent from the materials.

**Stage 4. Answer-balance pass.** Run the audit on the whole batch and apply section 10: option word counts, longest and shortest, letter distribution and runs, give-away features. Rewrite offenders and rerun until the numbers meet the rules.

**Stage 5. Quality check.** Apply section 13 to every question. Rewrite any that fails.

**Stage 6. Build and report.** Build the page (see `exam-page.md`), deliver it, and put the audit in the reply.

## 13. Quality checklist

1. Supported by the materials, with no outside facts in the stem or any option?
2. Maps to a stated objective, and not something a lecturer said not to memorize?
3. Passed the Stage 3 cross-reference, with its anchors recorded?
4. Exactly one best answer, and no distractor that is true per the materials?
5. Distractors from the same neighborhood, each a realistic error?
6. Options parallel and similar in length; the correct answer not the longest, most qualified or most specific by default?
7. Would a knowledgeable student plausibly hesitate between two or three options?
8. Tests reasoning, not recognition of wording from the notes?
9. Not a duplicate of another question, and not a copy of an instructor question?
10. Explanation teaches the distinguishing concept and stays short; each distractor's line names what it is true of?
11. Quantitative: mental math in about 20 seconds, no conversion chain, round numbers, each distractor matching its stated error?
12. Pathway or sequence content: answerable from the stem plus the logic, or covered by the narrow exception? If it needs recall of intermediates or step order, rewrite.
13. Data and figure items: answer readable unambiguously from what is shown, and everything shown taken from the materials?

## 14. What goes in the page and what goes in the reply

**In the page's footer scope note**, written for the user to read before trusting the exam: which sources it was built from (and which were missing), which lecturer scope signals were respected, which equations and constants were used, any source conflicts avoided, the mix profile, and the answer-letter balance.

**In the page's intro paragraph**: what the exam covers and how it is weighted, including how many items are quantitative and how many are built on a table, figure or experiment.

**In the reply, not the page**, the batch audit: letter counts; how often the correct answer is the longest and the shortest option, against the targets; what was dropped or rewritten at cross-reference, with a phrase of reason each; instructor-flagged concepts covered and those absent from the materials; conflicts flagged. If any target was missed after rewriting, say so plainly with the number. The audit is process information the user wants once; in the page it would be clutter on every reopening.

## 15. USMLE variant

Use this instead of sections 2 to 8, 11 and 12 when USMLE mode is on. The page, the answer-choice standards, the length and position rules (sections 9 and 10), and the quality checks on single best answer and distractors still apply.

- The standard is what Step tests (Step 1 unless the user says otherwise), written from general knowledge. There is no course map, no objectives anchor and no confirmation gate. The Intake step still applies: ask how many questions to generate and what content to base them on (here, which systems or topics), every time. Then state the blueprint in a line or two (systems, disciplines, count), and start.
- Write single-best-answer clinical vignettes in the style and difficulty of the real exam: patient, presentation, relevant history, vitals and labs in conventional units, then a focused lead-in. Up to five options. Test across disciplines within a stem where it fits.
- Distractors are the plausible alternatives a prepared student would consider: the neighboring diagnosis, the drug from the same class with the wrong mechanism, the right pathway at the wrong step.
- Explanations say why the right answer is right; each distractor's line says why it is wrong and what presentation it would fit.
- Findings that would need a photograph (histology, radiology, skin) are described in words. Draw only what can be drawn honestly as a figure: plots, curves, traces, pedigrees.
- Tag each question's source with its system or discipline, group sections by system or topic, and set the page's source noun accordingly (see `exam-page.md`). Bloom tags still apply.
- The footer scope note says the exam follows the Step standard and not the user's course materials, that the vignettes are written to imitate exam style and are not real exam items, and where a tested point is known to differ from the user's course materials. Where a fact is the kind that changes (first-line therapies, screening guidelines), check it before using it.
- The reply still carries the letter and length audit.
