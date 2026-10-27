---
name: research-cycle
description: |
  A closed-loop research workflow: Literature Survey → Multi-Agent Adversarial Gap Discovery → Innovation Design → Experiment Validation → Paper Writing.
  Integrates multi-agent adversarial debate and Semantic Scholar API literature validation.
  Works for any research domain requiring "find innovation + run experiments + publish papers".
  Triggers: research cycle, research workflow, literature survey, research brainstorming,
  scientific brainstorming, research gap, find research gap, adversarial debate,
  innovation design, experiment design, run experiments, paper writing,
  do research, research process, help me find innovations, scientific gap finder,
  multi-agent debate, gap analysis, literature review, academic research.
  User provides: research direction, available datasets, baseline methods, target journal/conference.
---

# Research Cycle Skill

## Overview

A general-purpose research cycle skill for [Codex](https://github.com/OpenAI/codex). Covers the entire pipeline from literature survey to paper publication, with built-in **multi-agent adversarial debate** for gap discovery and **Semantic Scholar API** for literature validation.

## When to Use

Use this skill when the user needs to:
- Find publishable research gaps in a given domain
- Design theoretically grounded innovations
- Validate innovations through rigorous experiments
- Write and publish academic papers

## Required Input

The user should provide:
1. **Research direction**: The specific problem to solve
2. **Available resources**: Datasets, baseline code, compute
3. **Target**: Journal/conference, required improvement margin
4. **Preferences**: Cross-domain sources, forbidden directions, etc.

## Full Research Cycle

```
┌─────────────────────────────────────────────────────────┐
│                  Research Cycle                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Phase 1: Literature Survey & Adversarial Gap Discovery  │
│     ├── 1a: Literature Search + Semantic Scholar Verify  │
│     ├── 1b: Multi-Agent Adversarial Debate               │
│     │      (Proposer / Reviewer / Evidence)              │
│     └── 1c: GO / REVISE / KILL Decision                 │
│     ↓                                                   │
│  Phase 2: Innovation Design                              │
│     ↓                                                   │
│  Phase 3: Baseline Reproduction                          │
│     ↓                                                   │
│  Phase 4: Innovation Implementation                      │
│     ↓                                                   │
│  Phase 5: Experimental Validation                        │
│     ↓                                                   │
│  Phase 6: Analysis & Iteration → Back to Phase 2        │
│     ↓                                                   │
│  Phase 7: Paper Writing                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Literature Survey & Adversarial Gap Discovery

### Phase 1a: Literature Search

#### Goal

Gain deep understanding of the state-of-the-art and identify 3-5 publishable research gaps.

#### Process

1. **Breadth search**: Search top venues from the last 3 years using relevant keywords
2. **Deep reading**: For each paper, ask three core questions:
   - Why was this accepted? (Innovation analysis: new problem? new approach? rigorous experiments?)
   - How to improve it? (Find limitations: untested scenarios, untuned parameters)
   - Can the method transfer? (Move method from domain A to domain B)
3. **Gap summary**: After each search round, summarize discovered gaps
4. **Iterate**: At least 15 rounds of search → summarize → find gaps

#### Three Core Questions (ask for every paper)

| Question | Purpose | Output |
|----------|---------|--------|
| Why accepted? | Understand the nature of innovation | Innovation type: new problem / new approach / rigorous experiments |
| How to improve? | Find improvement space | 1-2 concrete improvement points |
| Can it transfer? | Find cross-domain opportunities | "Method translator" opportunities |

#### Semantic Scholar API Literature Validation

Use the Semantic Scholar API to validate the number of papers in a candidate direction and assess the true gap size:

- API: `https://api.semanticscholar.org/graph/v1/paper/search`
- Request interval: ≥1.5 seconds (avoid rate limiting)
- Set `S2_API_KEY` environment variable for higher quotas

**Gap Size Classification**:

| Paper Count | Gap Size | Meaning |
|-------------|----------|---------|
| < 50 | Narrow gap | High risk, high reward — possibly a new or untouched direction |
| 50-100 | Medium-narrow gap | Some foundation but significant room |
| 100-500 | Medium gap | Mature direction, needs a fine-grained entry point |
| > 500 | Wide gap | Highly competitive, requires strong differentiation |

```bash
# Literature validation example
curl -H "x-api-key: ${S2_API_KEY}" \
  "https://api.semanticscholar.org/graph/v1/paper/search?query=QUERY&limit=1&fields=totalResults"
```

### Phase 1b: Multi-Agent Adversarial Debate

#### Role Assignment

Launch 3 agents in parallel:

1. **Proposer**: Drafts the research proposal
   - Output: 3 innovation modules + complete experiment design
   - Each module must have theoretical motivation, implementation plan, expected effect

2. **Reviewer**: Prepares the attack checklist
   - Output: 10 FATAL-level attacks + 23 MAJOR-level attacks
   - Attack dimensions: theoretical flaws, experiment design gaps, insufficient novelty, reproducibility

3. **Evidence**: Verifies literature claims
   - Output: EVIDENCE_CHECK.md
   - Validates: whether each citation is real, data is accurate, conclusions are supported

#### Adversarial Process

```
Round 1: Proposer presents 3 proposals → Reviewer attacks each → Survivors revise
    ↓
Round 2: Revised proposals attacked again → GO / REVISE / KILL
    ↓
Round 3+: If REVISE, continue revise → attack loop
    ↓
Final: Find a viable proposal (GO) or confirm direction is infeasible (KILL)
```

#### Decision Criteria

| Decision | Condition | Next Step |
|----------|-----------|-----------|
| **GO** | Proposal passes all FATAL checks, ≤ 3 fixable MAJORs | Proceed to Phase 2 |
| **REVISE** | 1-2 fixable FATALs, or too many MAJORs | Revise and re-review |
| **KILL** | Irreparable FATALs, or core assumptions disproven | Change direction |

### Phase 1c: Final Decision Output

```markdown
# Research Gap Report

## Recommended Direction: [Name]
- Gap Size: [Narrow / Medium-narrow / Medium]
- Literature Validation: [Paper count and trend]
- Adversarial Debate Result: [GO / REVISE] Rounds: [N]

## Candidate Gaps

### Gap 1: [Name]
- Source Paper: [Paper title]
- Current Limitation: [Specific description]
- Improvement Idea: [Concrete approach]
- Cross-domain Source: [Which domain's method can transfer]
- Expected Effect: [Quantitative estimate]
- Feasibility: [High / Medium / Low]
- Debate Result: [Passed / Defeated — reason]
```

#### Structured Output Files

After completing Phase 1, generate:
- `PROPOSAL_FINAL.md`: Detailed research proposal
- `REVIEW_FINAL_PREP.md`: Attack checklist and defense strategy
- `EVIDENCE_CHECK.md`: Literature verification report
- `FINAL_SUMMARY.md`: Compressed summary (1 page)

---

## Phase 2: Innovation Design

### Design Principles

1. **Theoretically grounded**: Each innovation must have a clear mathematical / physical / statistical motivation
2. **Explainable**: Can be justified in 1-2 sentences for why it works
3. **Verifiable**: Has a clear comparative experiment design
4. **Non-degrading**: A single innovation must not worsen results
5. **Additive**: Multiple innovations should have cumulative effects

### Two Practical Strategies

**Borrow-and-Swap**: Take an open-source top-venue paper, keep the framework, swap the domain
- Example: Natural image classification → industrial defect detection
- Advantage: reviewers implicitly credit "first application"

**Core-Upgrade**: Replace a single core component in a classical model
- Example: Standard convolution → deformable convolution for irregular targets
- Focus: write "improved for the XX pain point"

### Innovation Design Template

```markdown
## Innovation N: [Name]

### Problem Motivation
[Under what conditions does the current method fail? Why?]

### Theoretical Foundation
[From which domain and theory? What is the mathematical formula?]

### Implementation Plan
[What exactly to change? Which module/function?]

### Parameter Design
[New parameters? Default values?]

### Expected Effect
[Which metric improves? By how much?]

### Validation Method
[Comparative experiment: baseline vs +InnovationN]
```

---

## Phase 3: Baseline Reproduction

### Reproduction Principles

1. **Use official code**: Never use a self-written simplified version
2. **Use official parameters**: Obtain from the paper / GitHub
3. **Align results**: Compare with numbers reported in the paper

### Reproduction Report Template

```markdown
# Baseline Reproduction Report

## Method: [Name]
- Paper: [Paper title]
- Code: [GitHub link]
- Dataset: [Dataset name and split]
- Hardware: [GPU/CPU model]

### Reproduction Results
| Metric | Reported | Reproduced | Deviation | Reason |
|--------|----------|------------|-----------|--------|
| ... | ... | ... | ... | ... |

### Conclusion
- [x] Reproduction successful, results can serve as baseline
- [ ] Reproduction has deviation, reason: ...
```

---

## Phase 4: Innovation Implementation

### Implementation Principles

1. **Minimal changes**: Only modify necessary code, keep the framework intact
2. **Modular**: Toggle via configuration, default OFF
3. **Reproducible**: Record all modifications, version control
4. **Documented**: Every modification has explanatory comments

### Implementation Flow

1. **Backup original**: `cp -r original/ backup/`
2. **Understand code**: Read key functions, understand data flow
3. **Locate modification points**: Find the specific functions/lines to change
4. **Implement innovation**: Add new code
5. **Unit test**: Confirm no bugs introduced
6. **Integration test**: Compare with original, confirm no regression

### Code Modification Log

```markdown
# Modification Log

## Innovation 1: [Name]
### Modified Files
- path/to/file1.py: [Change description]
- path/to/file2.py: [Change description]

### New Parameters
- param_name: [type] [default] [description]

### Toggle Method
[How to enable/disable this innovation]
```

---

## Phase 5: Experimental Validation

### Experiment Design Principles

1. **Fair comparison**: Same data, same split, same hardware
2. **Multiple runs**: At least 3, report mean and standard deviation
3. **Ablation study**: Validate each innovation independently
4. **Cross-dataset**: Validate on at least 2 datasets

### Experiment Matrix

```
| Config     | Dataset1 | Dataset2 | Dataset3 |
|------------|----------|----------|----------|
| Baseline   | ✓        | ✓        | ✓        |
| +Innov. 1  | ✓        | ✓        | ✓        |
| +Innov. 2  | ✓        | ✓        | ✓        |
| +Innov. 3  | ✓        | ✓        | ✓        |
| +All       | ✓        | ✓        | ✓        |
```

### Results Template

```markdown
# Experiment Results

## Configuration
- Method: [Method name]
- Datasets: [Dataset list]
- Hardware: [Configuration]
- Runs: [N]

## Results
| Config     | Dataset1    | Dataset2    | Dataset3    |
|------------|-------------|-------------|-------------|
| Baseline   | X.XX±X.XX   | X.XX±X.XX   | X.XX±X.XX   |
| +Innov. 1  | X.XX±X.XX   | X.XX±X.XX   | X.XX±X.XX   |
| +Innov. 2  | X.XX±X.XX   | X.XX±X.XX   | X.XX±X.XX   |
| +All       | X.XX±X.XX   | X.XX±X.XX   | X.XX±X.XX   |

## Analysis
- Innovation 1: [Effective / Ineffective] [Reason]
- Innovation 2: [Effective / Ineffective] [Reason]
- Combined: [Additive / Synergistic / Conflicting]
```

### Success Criteria

- **Single innovation**: Must not be worse than baseline
- **Combined effect**: Shows cumulative improvement
- **Cross-dataset**: Effective on multiple datasets
- **Improvement margin**: Meets target (e.g., ≥10%)

---

## Phase 6: Analysis & Iteration

### Analysis Dimensions

1. **Quantitative**: Metric mean, standard deviation, significance test
2. **Qualitative**: Visualization, case studies
3. **Ablation**: Independent contribution of each innovation
4. **Failure analysis**: Under what conditions does the innovation fail

### Iteration Decision

| Situation | Decision | Next Step |
|-----------|----------|-----------|
| Innovation effective | Keep, add next one | Back to Phase 2 |
| Innovation ineffective | Analyze reason, adjust or abandon | Modify and retry, or new direction |
| Innovation degrades | Abandon immediately, record reason | New direction |
| Combination conflicts | Analyze conflict reason | Adjust combination |

---

## Phase 7: Paper Writing

### Paper Structure

1. **Introduction**: Problem motivation, related work, our contributions
2. **Related Work**: Grouped summary, identify gaps
3. **Method**: Problem definition, innovation details, theoretical analysis
4. **Experiments**: Datasets, setup, result analysis
5. **Conclusion**: Summary, limitations, future work

### Writing Principles

1. **Clear storyline**: Why it must be done → How we do it → How well it works
2. **Highlight innovations**: Each innovation has clear motivation and validation
3. **Rigorous experiments**: Multiple runs, standard deviation, ablation study
4. **Clear figures and tables**: Key results have both

### Target Venue Selection

Based on research direction and innovation type:
- **Theoretical innovation**: IEEE TPAMI, IJCV, NeurIPS
- **Applied innovation**: IEEE TRO, IROS, ICRA
- **Cross-domain**: Nature Machine Intelligence, Science Robotics

---

## General Rules

### Code Standards

- Preserve the original official code; make modifications on a copy
- Every modification has explanatory comments
- Use version control to track changes

### Experiment Standards

- Must use official baselines, never write simplified versions
- Multiple runs reported as mean ± standard deviation
- Ablation experiments validate each innovation

### Documentation Standards

- Each Phase has an output document
- Record all decisions and reasons
- Keep intermediate results for traceability

---

## Quick Command Templates

### Literature Survey
```
Search [keyword] papers from top venues in the last 3 years, summarize innovations and limitations
```

### Multi-Agent Adversarial Gap Discovery
```
Launch 3 adversarial agents: Proposer/Reviewer/Evidence,
research direction is [direction], target journal is [journal], at least 3 rounds
```

### Literature Validation
```
Use Semantic Scholar API to count papers in the [keyword] direction and assess gap size
```

### Innovation Design
```
Based on [gap description], design a theoretically grounded innovation sourced from [domain]
```

### Baseline Reproduction
```
Reproduce [method] on [dataset] using official code, official config is...
```

### Experimental Validation
```
Run ablation study for [method], comparing baseline vs each innovation independently
```

### Paper Writing
```
Write the Method section for [innovation name], including theoretical analysis
```