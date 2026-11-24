# Edexcel GCSE Maths (1MA1) question bank: topic index (Higher and Foundation)

A topic-sorted index of the Higher tier papers for Pearson Edexcel GCSE Mathematics (1MA1), June 2019 to June 2025 (11 series, 33 papers, 740 questions, 2640 marks). The Foundation tier (943 questions, 2640 marks) is covered further down.

This repository holds metadata and original writing only. It does NOT contain Pearson question papers, mark schemes, crops, question text, mark-scheme text or examiner reports. Get the papers from Pearson: https://qualifications.pearson.com/en/support/support-topics/exams/past-papers.html . Question ids look like `jun2019-1h-1` (June 2019, paper 1H, question 1).

## What is here
- `questions.json` and `docs/higher-classification.csv`: one row per question with marks, calculator flag, primary and secondary topic, confidence, a method note in our own words, command words, question type, spec refs, Foundation twin (`alsoOn`) and hardest flags.
- `docs/higher-parts.csv`: parts, nested subparts and marks (sums to 2640). One question's per-part marks are unknown and flagged.
- `topic-packs/`: one page per sub-topic (66), plus an index.
- `docs/TOPIC-SCHEME.md`: our 66 sub-topics, spec refs, tagging rules, comparison with Pearson and Physics & Maths Tutor groupings.
- `docs/SPEC-FACTS.md`: facts from the official specification, with page references and source tags.
- `docs/tier-overlap.csv`: Higher questions with a verified Foundation twin (236) plus one unresolved candidate.
- `docs/hardest-parts.csv` (top 15% of parts per paper and topic, at least one each) and `docs/hardest-15pct.csv` (top 15% of parts overall): a heuristic, not Pearson data.
- `docs/mark-patterns.csv`: mark-code sequence and note flags per question (no scheme wording).
- `docs/examiner-insights.csv`: paraphrased findings from the one examiner report found that covers Higher papers (June 2019).
- `docs/templates-evidence.csv`: 38 examiner-report claims and 75 marking-method evidence rows, each with a status tag.
- `docs/MS-MINING.md`: aggregate shares of mark types per topic. No scheme wording.
- `docs/TEMPLATES.md` and `TEMPLATES.pdf`: 37 answer-template patterns with set-out skeletons, marking-method summaries in our own words (scheme file and page cited), alternatives, common errors and seen-in counts; `template-patterns.csv` lists the questions.
- `code/`: the original pipeline scripts (they need the Pearson PDFs, which you download yourself).
- `docs/QA-LOG.md`, `docs/GAPS.md`: checks done, known limits, and what could not be collected.

## Known limits
- Topic labels are our judgment. A random sample of 50 was visually checked and about 6% of labels in it needed correcting, so unsampled labels are provisional.
- The overlap check compared wording and figures; see QA-LOG.md.
- Foundation is not done. Examiner-report evidence was found only for June 2019 (not established that no others exist), so template common-error advice rests on one report. Variations (step 11) were not produced.

Pearson, Edexcel and GCSE are Pearson trademarks. This project is unofficial.

## Foundation (partial)
- `questions-foundation.json` and `docs/foundation-classification.csv`: 943 questions, 2640 marks. Confidence is high (116), medium (827) or low (0) by docs/CONFIDENCE-RULE.md; all 642 single-part labels have a recorded method review (see docs/GAPS.md); 236 are inherited from verified Higher twins.
- `docs/foundation-parts.csv`: part rows (marks sum to 2640; stems 0; nov2019-1f-27 split unknown, counted once at question level) with scheme-code split where it fits.
- `docs/foundation-mark-patterns.csv`, `docs/foundation-method-by-topic.csv`, `docs/foundation-hardest-*.csv` (heuristic), `topic-packs-foundation/`.
- `docs/FOUNDATION-TEMPLATES.md` and `.pdf`: 43 Foundation patterns with own-words marking lines from 84 example schemes; `foundation-template-patterns.csv`, `foundation-templates-evidence.csv`, `foundation-templates-audit30.csv` (30-claim audit). No Foundation examiner report was found.
- Not done: template patterns for some topics, step 11 variations. See `docs/GAPS.md`.
