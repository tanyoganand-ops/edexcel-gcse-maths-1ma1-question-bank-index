# Pipeline code

Original Python used to build this index. It needs the Pearson PDFs, which are not included and must be downloaded by you from Pearson's past-paper page (see `dl.py`, which reads a list of document links you collect yourself in `links.txt`). Paths are relative: run from a working folder with `pdf/` (the papers, named `<Series>__<file>.pdf`) and `work/private/` (intermediate files; never publish them, they contain Pearson text).

Order: `dl.py` (download), `seg.py` and `qstruct.py` (find questions, parts, nested subparts, totals), `msseg.py` and `extract.py` (read schemes, build records), `classify.py` and `scheme.py` (topic scoring using own cue words), `align.py` (align parts to scheme slices), `overlap.py` and `ov2.py` (Higher-Foundation twins), `qa_counts.py` and `validate.py` (checks), `build_out.py`, `build2.py`, `build_tpl.py` with `patterns.py` and `tdata.py` (public outputs).

These scripts were written during one working session and are not polished or tested outside it.
