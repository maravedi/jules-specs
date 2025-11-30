# Jules-Specs Workflow Diagrams

Visual guides for understanding how jules-specs integrates with GitHub.

## Complete Development Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    JULES DEVELOPMENT PIPELINE                    │
└─────────────────────────────────────────────────────────────────┘

Step 1: SPEC GENERATION (jules-specs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    User Input
        ↓
  ┌─────────────┐
  │ GitHub Issue │ → Label: "spec-request"
  │  or Comment  │    or /generate-spec
  └─────────────┘
        ↓
  ┌─────────────┐
  │   GitHub    │
  │   Actions   │ → Workflow triggers
  └─────────────┘
        ↓
  ┌─────────────┐
  │ jules-specs │ → python -m jules_specs "prompt"
  └─────────────┘
        ↓
  ┌─────────────┐
  │  spec-kit   │ → Generate spec.md, architecture.md, api.md
  └─────────────┘
        ↓
  ┌─────────────┐
  │  Git Commit │ → jules-specs-<hash> branch
  └─────────────┘
        ↓
  ┌─────────────┐
  │ Pull Request│ → Ready for review
  └─────────────┘
        ↓
    .specify/specs/001/

Step 2: PLAN GENERATION (jules-planner)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  .specify/specs/001/
        ↓
  ┌─────────────┐
  │jules-planner│ → jules-planner --spec-dir .specify/specs/001/
  └─────────────┘
        ↓
  ┌─────────────┐
  │ Task List + │ → Detailed implementation plan
  │    Plan     │
  └─────────────┘

Step 3: IMPLEMENTATION
━━━━━━━━━━━━━━━━━━━━━

  Task List
        ↓
  ┌─────────────┐
  │ Claude/Jules│ → Execute tasks
  │  or Manual  │
  └─────────────┘
        ↓
  ┌─────────────┐
  │ Working Code│ ✨
  └─────────────┘
```

## GitHub Integration Methods

### Method 1: Issue Label Trigger

```
┌──────────────┐
│  User creates│
│  GitHub Issue│
│              │
│  Title: "Build│
│  a photo app" │
└──────┬───────┘
       │
       │ Adds label
       ↓
┌──────────────┐
│ Label Added: │
│spec-request │
└──────┬───────┘
       │
       │ Triggers
       ↓
┌──────────────────────────────┐
│ GitHub Actions Workflow      │
│ (generate-specs-on-issue.yml)│
└──────┬───────────────────────┘
       │
       ↓
┌──────────────┐     ┌──────────────┐
│ Install deps │ →   │ Run jules-   │
│ - Python     │     │ specs        │
│ - Node.js    │     └──────┬───────┘
│ - spec-kit   │            │
└──────────────┘            │
                            ↓
                    ┌──────────────┐
                    │ Generate     │
                    │ Specs        │
                    └──────┬───────┘
                           │
                           ↓
                    ┌──────────────┐     ┌──────────────┐
                    │ Create       │ →   │ Comment on   │
                    │ Pull Request │     │ Issue        │
                    └──────────────┘     └──────────────┘
                           │
                           ↓
                    User reviews PR
```

### Method 2: Comment Command Trigger

```
┌──────────────────┐
│ Existing GitHub  │
│ Issue            │
└────────┬─────────┘
         │
         │ User comments
         ↓
┌──────────────────┐
│ Comment:         │
│ "/generate-spec  │
│  Build photo app"│
└────────┬─────────┘
         │
         │ Triggers
         ↓
┌──────────────────────────────┐
│ GitHub Actions Workflow      │
│(generate-specs-on-comment.yml)│
└────────┬─────────────────────┘
         │
         │ Extracts prompt from comment
         ↓
┌──────────────────┐
│ Run jules-specs  │
│ with extracted   │
│ prompt           │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐     ┌──────────────┐
│ Create PR        │ →   │ Reply to     │
│                  │     │ comment with │
│                  │     │ PR link      │
└──────────────────┘     └──────────────┘
```

### Method 3: Manual Workflow Dispatch

```
┌──────────────────┐
│ User navigates   │
│ to Actions tab   │
└────────┬─────────┘
         │
         │ Clicks "Run workflow"
         ↓
┌──────────────────┐
│ Fills form:      │
│ - Prompt         │
│ - Enhance? ☑     │
│ - Create PR? ☑   │
└────────┬─────────┘
         │
         │ Submits
         ↓
┌──────────────────────────────┐
│ GitHub Actions Workflow      │
│ (generate-specs-manual.yml)  │
└────────┬─────────────────────┘
         │
         ↓
┌──────────────────┐
│ Generate specs   │
│ based on inputs  │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Create PR        │
│ (if selected)    │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Job summary in   │
│ Actions tab      │
└──────────────────┘
```

## File Flow

```
jules-specs Repository Structure
─────────────────────────────────

jules-specs/
├── .github/
│   ├── workflows/
│   │   ├── generate-specs-on-issue.yml    ← Workflow 1
│   │   ├── generate-specs-on-comment.yml  ← Workflow 2
│   │   └── generate-specs-manual.yml      ← Workflow 3
│   │
│   └── ISSUE_TEMPLATE/
│       ├── spec-request.yml               ← Issue form
│       └── config.yml                     ← Template config
│
├── jules_specs/
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py                             ← Main logic
│
├── docs/
│   ├── GITHUB_INTEGRATION.md              ← Full guide
│   ├── QUICKSTART_GITHUB.md               ← 5-min setup
│   └── WORKFLOWS.md                       ← This file
│
└── README.md                              ← Overview


Generated Output Structure
───────────────────────────

your-project/
└── .specify/
    └── specs/
        ├── 001/
        │   ├── spec.md          ← Main specification
        │   ├── architecture.md  ← System design
        │   └── api.md          ← API documentation
        │
        ├── 002/
        │   ├── spec.md
        │   ├── architecture.md
        │   └── api.md
        │
        └── 003/
            └── ...
```

## Workflow Decision Tree

```
                    Need to generate specs?
                            │
                            ↓
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    Want to use         Want to use        Want to run
    GitHub UI?         Issue tracking?      manually?
        │                   │                   │
        ↓                   ↓                   ↓
    ┌──────┐          ┌──────────┐        ┌──────────┐
    │Manual│          │ Issue or │        │  Local   │
    │ Run  │          │ Comment? │        │   CLI    │
    └───┬──┘          └────┬─────┘        └────┬─────┘
        │                  │                    │
        ↓                  ↓                    ↓
   Go to Actions    ┌─────────────┐      jules-specs
   → Run workflow   │ Issue? → Add│      "your prompt"
                    │ spec-request│
                    │ label       │
                    │             │
                    │ Comment? →  │
                    │ /generate-  │
                    │ spec prompt │
                    └─────────────┘
```

## Integration Points

```
External Systems Integration
─────────────────────────────

┌──────────────┐
│   GitHub     │
│   Issues     │ ──→ Webhook ──→ GitHub Actions
└──────────────┘

┌──────────────┐
│   Project    │
│   Boards     │ ←── API ──── Workflow (optional)
└──────────────┘

┌──────────────┐
│   Slack/     │
│   Discord    │ ←── Webhook ── Workflow (optional)
└──────────────┘

┌──────────────┐
│   jules-     │
│   planner    │ ←── Input ──── Generated specs
└──────────────┘


Authentication Flow
───────────────────

GitHub Actions
      ↓
Uses: GITHUB_TOKEN (automatic)
      ↓
Permissions:
  - contents: write      (push to repo)
  - pull-requests: write (create PRs)
  - issues: write        (comment on issues)
      ↓
No secrets needed! ✨
```

## Timing Diagram

```
Time-based Flow (typical execution)
───────────────────────────────────

00:00  User triggers workflow (issue/comment/manual)
       │
00:10  ├── GitHub Actions starts
       │   └── Job queued
       │
00:20  ├── Runner assigned (ubuntu-latest)
       │   └── Environment setup
       │
00:30  ├── Checkout repository
       │
00:40  ├── Setup Python 3.11
       │
01:00  ├── Setup Node.js 20
       │
01:20  ├── Install jules-specs
       │   └── pip install -e .
       │
01:50  ├── Install spec-kit
       │   └── npm install -g @github/spec-kit
       │
02:00  ├── Configure Git
       │
02:10  ├── Run jules-specs
       │   ├── Create branch
       │   ├── Generate specs (calls spec-kit)
       │   │   └── AI generation (~60-90s)
       │   └── Commit files
       │
03:40  ├── Push to remote
       │
03:50  ├── Create Pull Request
       │
04:00  ├── Comment on issue (if applicable)
       │
04:10  └── Workflow complete ✅

Total: ~4-5 minutes (varies by spec complexity)
```

## Error Handling Flow

```
Error Scenarios
───────────────

jules-specs execution
        ↓
┌───────────────┐
│ Success? ────┼──→ Yes ──→ Create PR ──→ Comment success
└───────┬───────┘
        │
        No
        ↓
┌───────────────┐
│ What failed?  │
└───────┬───────┘
        │
        ├──→ spec-kit not found
        │    └──→ Install step failed
        │         └──→ Check Node.js setup
        │
        ├──→ Permission denied
        │    └──→ Check workflow permissions
        │         └──→ Settings → Actions
        │
        ├──→ Git push failed
        │    └──→ Check branch protection rules
        │         └──→ Ensure Actions can push
        │
        └──→ Other error
             └──→ Comment on issue with error
                  └──→ Link to workflow logs
```

## Best Practices Flow

```
Recommended Usage Pattern
─────────────────────────

Development Team
       ↓
┌──────────────────┐
│ Plan new feature │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Create GitHub    │ ← Use issue template
│ Issue with       │
│ spec-request     │
│ label            │
└────────┬─────────┘
         │
         ↓ (automated)
┌──────────────────┐
│ Specs generated  │
│ PR created       │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Team reviews PR  │ ← Code review process
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Refine specs     │ ← Make edits in PR
│ if needed        │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Merge PR         │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Run jules-planner│
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Implementation   │
└──────────────────┘
```

## See Also

- [GITHUB_INTEGRATION.md](GITHUB_INTEGRATION.md) - Comprehensive guide
- [QUICKSTART_GITHUB.md](QUICKSTART_GITHUB.md) - 5-minute setup
- [README.md](../README.md) - Project overview
