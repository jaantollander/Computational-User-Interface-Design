# Computational User Interface Design
## Material
* [Computational Interaction](https://books.google.fi/books?id=NXFGDwAAQBAJ)


## Convert a notebook into PDF (for static reading)
Convert jupyter notebook to markdown file.
```bash
jypyter nbconvert filename.ipynb --to markdown
```

Convert markdown file to pdf via Pandoc and LaTeX.
```bash
FILENAME=""
pandoc $FILENAME.md \
--from=markdown+raw_tex+tex_math_dollars \
--to=latex \
--output=$FILENAME.pdf
```

## Submission Instructions

1. Upload one ZIP file per task, containing
    1) necessary code (E.g., in A1 the .ipynb files suffice, no need to include utility functions nor the imgs folder); and
    2) the PDF report. For example, if you did A1.1 and A1.2, you should upload 2 zip files, respectively.

2. The ZIP file and the files within must be named using this naming convention: “lastname_A_x_x.extension”, e.g. “oulasvirta_A_1_1.pdf”.

3. In addition to task-specific instructions, the PDF reports must contain:
    1) your name and student ID on the first page;
    2) task identifier in title (e.g., "A1.1"),
    3) a verbal summary of your approach and assumptions,
    4) screenshots of results, if relevant, and
    5) a verbal summary and assessment of the result.
