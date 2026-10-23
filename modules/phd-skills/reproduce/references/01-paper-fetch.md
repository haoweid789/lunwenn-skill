# Stage 1: Paper acquisition

Fetch the paper into a structured local extract before doing anything else. Working from a polished local copy is much faster than re-scrolling arxiv on every hyperparam question.

## Inputs

- arxiv URL or arxiv ID (e.g. `2508.12345`, `https://arxiv.org/abs/2508.12345`)
- OpenReview URL or proceedings URL (CVPR / NeurIPS / ICLR / ICML / etc.)
- direct PDF URL as fallback

## Steps

### 1. Fetch the paper with Paper Search CLI

Use [fcakyon/paper-search-cli](https://github.com/fcakyon/paper-search-cli). Follow the paper search section of [setup](../../../commands/setup.md) if the command is missing.

For an arXiv paper, keep the supplied version suffix so the PDF matches the user's reference:

```bash
paper-search search 'id:1706.03762v7' -s arxiv -n 1
paper-search download arxiv 1706.03762v7 -o ./repro/1706.03762v7
paper-search read arxiv 1706.03762v7 -o ./repro/1706.03762v7
```

Replace the example ID and directory with the requested paper. Search returns JSON; inspect `errors`. The `read` command writes extracted plain text to stdout; it does not create the structured Markdown document. Keep the downloaded PDF as the primary source.

For a DOI, use `paper-search tool get_crossref_paper_by_doi <doi>`. Discover other providers with `paper-search sources` and their operations with `paper-search tool --help`. Do not pass an arbitrary URL as a provider paper ID.

For a direct PDF URL or an unsupported proceedings site, download the publisher's public PDF with `curl -fL` and use an available PDF reader. ArXiv HTML at `https://arxiv.org/html/<id>` can help with equations and tables. If access fails, report the failure; do not substitute abstract text for the full paper.

### 2. Verify the PDF and find the official code

Inspect rendered PDF pages for equations, figures, and table values that text extraction may scramble. Check author names, venue, and year against the published record. Follow the paper's code link or search GitHub with `gh search repos`; verify a candidate repository links back to the paper before calling it official.

### 3. Capture into `repro/<id>/paper.md`

Structured extract with these sections (copy verbatim from paper, do not paraphrase yet):

```markdown
# <Paper Title>

**arxiv**: <id>
**venue**: <conference/journal/year>
**authors**: <full author list>
**code**: <official repo url, "none" if not provided>
**abstract**: <verbatim>

## Method (verbatim from paper sections 3-4)

<copy-paste relevant sections>

## Hyperparameter tables (verbatim)

<every table that lists training hyperparameters, dataset stats, eval setup>

## Algorithm boxes (verbatim)

<every numbered algorithm or pseudocode block>

## Loss formulation (with equation numbers)

<every equation referenced from the method, with its number>

## Results tables (verbatim)

<the main result table + ablations>

## Caveats / negative results / mentioned-but-not-shown

<scan the paper for "we found", "in our experiments", "with X we observed", these often
hide critical implementation details>
```

### 4. Note what's missing

At the bottom of `paper.md`, add an `# Open questions` section listing every gap you noticed during the read:

- "Optimizer betas not specified, only said 'AdamW with default settings'"
- "Augmentation pipeline order ambiguous: does cutout happen before or after normalize?"
- "Eval protocol references appendix B which is not in the arxiv version"

These become inputs to stage 3 (gap analysis).

## Success criteria

- `paper.md` exists with all six sections populated
- the `# Open questions` list has at least 3-5 items (most papers have many; if you found zero, you didn't read carefully enough)
- you can answer "what does this paper actually do" in one paragraph from `paper.md` alone

If the paper has an official code repo, note its URL but do not clone yet, that's stage 2.
