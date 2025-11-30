# GitHub Integration Guide

This guide explains how to integrate jules-specs into your GitHub workflows for automated specification generation.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Triggering Methods](#triggering-methods)
- [Workflow Examples](#workflow-examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Overview

Jules-specs can be integrated into GitHub Actions workflows to automatically generate specifications from:
- GitHub Issues
- Manual triggers (workflow_dispatch)
- Issue/PR comments
- Scheduled runs

The workflows will:
1. Extract the specification prompt
2. Generate specs using spec-kit
3. Create a new branch with the specifications
4. Open a pull request for review
5. Notify users of completion

## Setup

### 1. Add Workflow Files

Copy the workflow files from `.github/workflows/` to your repository:

```bash
.github/workflows/
├── generate-specs-on-issue.yml      # Trigger on issue label
├── generate-specs-on-comment.yml    # Trigger on /generate-spec command
└── generate-specs-manual.yml        # Manual trigger via GitHub UI
```

### 2. Configure Repository Permissions

Ensure your GitHub Actions have the necessary permissions:

**Settings → Actions → General → Workflow permissions:**
- ✅ Read and write permissions
- ✅ Allow GitHub Actions to create and approve pull requests

### 3. Install Dependencies in Workflows

All example workflows include steps to:
- Install Python and Node.js
- Install jules-specs package
- Install GitHub spec-kit

No additional configuration needed!

## Triggering Methods

### Method 1: Issue Labels

**Workflow**: `generate-specs-on-issue.yml`

1. Create an issue with your specification request
2. Add the `spec-request` label
3. GitHub Actions will automatically:
   - Extract the issue title as the prompt
   - Generate specifications
   - Create a PR with the results
   - Comment on the issue with the PR link

**Example**:
```
Issue Title: "Build a photo organizer app"
Labels: spec-request
→ Triggers automatic spec generation
```

### Method 2: Issue Comments

**Workflow**: `generate-specs-on-comment.yml`

1. Create or find an existing issue
2. Comment with: `/generate-spec <your prompt>`
3. GitHub Actions will:
   - Extract the prompt from your comment
   - Generate specifications
   - Create a PR
   - Reply to your comment with results

**Example**:
```
/generate-spec Build a CMMC-compliant photo organizer
```

If you don't provide a prompt after `/generate-spec`, it will use the issue title.

### Method 3: Manual Dispatch

**Workflow**: `generate-specs-manual.yml`

1. Go to **Actions** tab in your repository
2. Select "Generate Specs (Manual)"
3. Click "Run workflow"
4. Fill in the form:
   - **Prompt**: Your specification request
   - **Enhance**: Enable Jules compliance critique (default: true)
   - **Create PR**: Automatically create pull request (default: true)
5. Click "Run workflow"

**Screenshot Location**:
```
GitHub → Actions → Generate Specs (Manual) → Run workflow
```

### Method 4: Scheduled Generation

Add a scheduled trigger to any workflow:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
```

## Workflow Examples

### Basic Issue-Triggered Workflow

```yaml
name: Generate Specs from Issue

on:
  issues:
    types: [opened, labeled]

jobs:
  generate-specs:
    if: contains(github.event.issue.labels.*.name, 'spec-request')
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          pip install -e .
          npm install -g @github/spec-kit

      - name: Generate specs
        run: |
          python -m jules_specs "${{ github.event.issue.title }}" --enhance

      - name: Create PR
        run: |
          gh pr create --title "Specs: ${{ github.event.issue.title }}" --body "Auto-generated"
```

### Comment Command Handler

```yaml
name: Handle Spec Commands

on:
  issue_comment:
    types: [created]

jobs:
  handle-command:
    if: contains(github.event.comment.body, '/generate-spec')
    runs-on: ubuntu-latest

    steps:
      # Extract prompt from comment
      # Generate specs
      # Create PR
      # Reply to comment
```

### Custom Workflow with Options

```yaml
name: Custom Spec Generation

on:
  workflow_dispatch:
    inputs:
      prompt:
        required: true
      output_dir:
        default: '.specify/specs'
      enhance:
        type: boolean
        default: true

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Generate specs
        run: |
          ENHANCE=""
          if [ "${{ inputs.enhance }}" = "true" ]; then
            ENHANCE="--enhance"
          fi

          python -m jules_specs "${{ inputs.prompt }}" \
            --output-dir "${{ inputs.output_dir }}" \
            $ENHANCE
```

## Configuration

### Environment Variables

You can customize behavior with environment variables:

```yaml
env:
  JULES_SPECS_OUTPUT_DIR: '.specify/specs'
  JULES_SPECS_ENHANCE: 'true'
```

### Workflow Inputs

For `workflow_dispatch`, customize the input form:

```yaml
on:
  workflow_dispatch:
    inputs:
      prompt:
        description: 'What should we build?'
        required: true
        type: string

      framework:
        description: 'Preferred framework'
        type: choice
        options:
          - React
          - Vue
          - Angular
          - None
        default: 'React'

      enhance:
        description: 'Add compliance critique'
        type: boolean
        default: true
```

### Custom Labels

Change the trigger label in `generate-specs-on-issue.yml`:

```yaml
if: contains(github.event.issue.labels.*.name, 'your-custom-label')
```

### Custom Commands

Change the comment trigger in `generate-specs-on-comment.yml`:

```yaml
if: contains(github.event.comment.body, '/your-custom-command')
```

## Best Practices

### 1. Use Labels for Organization

Create and use labels:
- `spec-request` - Trigger spec generation
- `specs` - Mark spec-related PRs
- `automated` - Mark bot-generated content

### 2. Protect Main Branch

Configure branch protection:
- Require PR reviews
- Require status checks
- No direct pushes to main

### 3. Review Generated Specs

Always review auto-generated specifications before merging:
1. Check for completeness
2. Verify technical accuracy
3. Ensure alignment with requirements

### 4. Use Issue Templates

Create `.github/ISSUE_TEMPLATE/spec-request.md`:

```markdown
---
name: Specification Request
about: Request automated spec generation
labels: spec-request
---

## Feature Description

[Describe what you want to build]

## Requirements

- [ ] Requirement 1
- [ ] Requirement 2

## Additional Context

[Any additional information]
```

## Advanced Usage

### Chaining with Jules-Planner

Create a workflow that generates both specs and plans:

```yaml
name: Full Jules Pipeline

on:
  workflow_dispatch:
    inputs:
      prompt:
        required: true

jobs:
  generate-specs:
    runs-on: ubuntu-latest
    outputs:
      spec_dir: ${{ steps.generate.outputs.spec_dir }}
    steps:
      - name: Generate specs
        id: generate
        run: |
          OUTPUT=$(python -m jules_specs "${{ inputs.prompt }}")
          SPEC_DIR=$(echo "$OUTPUT" | grep "Output directory:" | sed 's/.*: //')
          echo "spec_dir=$SPEC_DIR" >> $GITHUB_OUTPUT

  generate-plan:
    needs: generate-specs
    runs-on: ubuntu-latest
    steps:
      - name: Generate plan
        run: |
          jules-planner --spec-dir ${{ needs.generate-specs.outputs.spec_dir }}
```

### Multi-Repository Setup

For organization-wide spec generation:

1. Create a central repository with jules-specs
2. Use `repository_dispatch` to trigger from other repos
3. Generate specs in the central repo
4. Create PRs back to source repositories

### Integration with Project Boards

Auto-add generated PRs to project boards:

```yaml
- name: Add to Project
  env:
    GH_TOKEN: ${{ github.token }}
  run: |
    gh project item-add <project-number> \
      --owner ${{ github.repository_owner }} \
      --url ${{ steps.create-pr.outputs.pr_url }}
```

## Troubleshooting

### Issue: Workflow not triggering

**Check**:
1. Workflow file in `.github/workflows/`
2. Correct label name (case-sensitive)
3. Actions enabled in repository settings
4. Workflow permissions configured

### Issue: Permission denied errors

**Solution**:
```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
```

### Issue: spec-kit not found

**Solution**:
Ensure spec-kit installation in workflow:
```yaml
- name: Install spec-kit
  run: npm install -g @github/spec-kit
```

### Issue: Git push fails

**Solution**:
Configure git identity:
```yaml
- name: Configure Git
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
```

### Issue: Branch already exists

**Solution**:
Add branch cleanup or use unique names:
```yaml
- name: Create unique branch
  run: |
    BRANCH="jules-specs-$(date +%s)"
    git checkout -b "$BRANCH"
```

## Examples from the Wild

### Example 1: E-commerce Platform

```
Issue: "Build a product recommendation engine"
Label: spec-request
Result:
  - spec.md (ML model requirements)
  - architecture.md (microservices design)
  - api.md (REST endpoints for recommendations)
```

### Example 2: Compliance System

```
Comment: /generate-spec CMMC Level 2 compliant document management system
Result:
  - Enhanced spec with CMMC requirements
  - Security controls architecture
  - Audit logging API
```

### Example 3: Mobile App

```
Manual Dispatch:
  Prompt: "iOS app for photo organization with ML tagging"
  Enhance: true
Result:
  - Detailed iOS app specification
  - Cloud architecture for ML processing
  - RESTful API for photo sync
```

## Support

For issues with GitHub integration:
1. Check workflow logs in Actions tab
2. Review this documentation
3. Open an issue in the jules-specs repository
4. Check [GitHub Actions documentation](https://docs.github.com/en/actions)

## Related Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub spec-kit](https://github.com/github/spec-kit)
- [Jules-planner](https://github.com/maravedi/jules-planner)
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
