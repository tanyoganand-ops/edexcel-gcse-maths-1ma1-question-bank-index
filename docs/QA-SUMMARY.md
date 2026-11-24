# QA summary (Higher complete, Foundation complete with limits)

Date: 24 Nov 2026. Sources: Pearson past papers, mark schemes, specification (links in README). No Pearson text, crops or quotes are in this repo.

## Checked
- Higher: all questions extracted, mark totals reconciled, part rows reconciled, 50-item visual sample, examiner-report notes (June 2018, June 2019 only).
- Foundation: 943 questions, 2640 marks; 300 of 300 multi-part splits aligned; twin-part mismatches 0.
- Foundation templates: 43 patterns, 84 example schemes. A 30-claim audit found 8 wrong lines (27%), so all 84 were read against scheme text and corrected. jun2019-3f-28 now follows the scheme page.
- Leaf labels: every single-part Foundation label (642) now has a recorded review. 36 flagged ones and a random 60 were read in full detail; the remaining 546 were each read once in an earlier batch review (question text and scheme opening, not the full scheme; later superseded for method notes by the full-entry read below), with OCR of the question pages for nov2019 paper 2F, where text extraction had lost most wording. 19 labels were changed in total. One extraction fault was found (nov2024-3f-23 text began with the tail of question 22) and its label corrected.

## Not done or limited
- History and current state: the 546 labels were first reviewed from the scheme opening only; the 66 whose wording had been lost were then OCR'd from the question pages and re-graded, so no label is low now (116 high, 827 medium, 0 low). Method notes for all 707 non-inherited rows were later written from the full scheme entry. Labels were not checked against page images except the visual random 50, the nov2019 2F OCR and a handful of spot checks (two question pages, four scheme pages).
- Foundation hardest-question tables are heuristic.
- Examiner reports were found and collected only for Higher June 2018 and June 2019; I have not established that none exist elsewhere.
- Marking statements apply to the schemes read, not to every paper. Teaching skeletons are our advice.
- Optional variations not built.

## Schema
- Confidence values are high, medium or low only (docs/CONFIDENCE-RULE.md): Foundation 116 high, 827 medium, 0 low.
- methodNote is filled for all 943 Foundation questions. 236 are hand-written Higher-twin routes. 707 are own-words notes written from each question's scheme entry (707 full, 0 partial, 0 unfinished); the earlier generated structural notes were withdrawn. The method notes were checked against the scheme text for these rows, not against page images, and wording that did not extract is flagged in the note. Public notes carry mark structure only: question-specific figures and answer values were removed (repo/code/scrub_notes.py, apply_public_scrub.py).
- Extraction fault nov2024-3f-23 fixed in text, source pages (19) and label (N11).
