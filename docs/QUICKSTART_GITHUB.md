# GitHub Integration Quick Start

Get up and running with automated spec generation in 5 minutes.

## Prerequisites

- GitHub repository with Actions enabled
- Admin access to configure repository settings

## Step-by-Step Setup

### 1. Add Workflow Files (1 minute)

Copy the workflow files to your repository:

```bash
# From the jules-specs repository
cp -r .github/workflows/ /path/to/your/repo/.github/

# Or manually create the files from the examples
```

Your repository should now have:
```
your-repo/
└── .github/
    └── workflows/
        ├── generate-specs-on-issue.yml
        ├── generate-specs-on-comment.yml
        └── generate-specs-manual.yml
```

### 2. Configure Permissions (1 minute)

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Scroll to "Workflow permissions"
4. Select **"Read and write permissions"**
5. Check **"Allow GitHub Actions to create and approve pull requests"**
6. Click **Save**

### 3. Create the Label (30 seconds)

1. Go to **Issues** → **Labels**
2. Click **New label**
3. Enter:
   - Name: `spec-request`
   - Description: `Triggers automatic spec generation`
   - Color: `#0E8A16` (green) or your preference
4. Click **Create label**

### 4. Test It! (2 minutes)

#### Option A: Test with Issue Label

1. Create a new issue
2. Title: `Build a simple REST API for user management`
3. Add the `spec-request` label
4. Submit the issue
5. Watch the **Actions** tab - you should see the workflow running!

#### Option B: Test with Comment

1. Create or open any issue
2. Add a comment: `/generate-spec Build a photo organizer app`
3. Watch for the bot's response

#### Option C: Test Manual Trigger

1. Go to **Actions** tab
2. Select **"Generate Specs (Manual)"** from the left sidebar
3. Click **"Run workflow"** button (top right)
4. Fill in:
   - Prompt: `Build a task management system`
   - Enhance: ✅ (checked)
   - Create PR: ✅ (checked)
5. Click **"Run workflow"** (green button)
6. Watch the workflow run!

## What to Expect

### Timeline
- ⏱️ Workflow starts: ~10 seconds
- 🔧 Dependencies install: ~30-60 seconds
- 📝 Spec generation: ~1-2 minutes
- 🔀 PR creation: ~5 seconds
- **Total: ~2-5 minutes**

### Success Indicators

✅ **In Actions tab**:
- Green checkmark next to workflow run
- "Generate specs" job completed successfully

✅ **In Pull Requests tab**:
- New PR titled "Specifications: [your prompt]"
- Contains generated spec files
- Has "specs" and "automated" labels

✅ **In the Issue** (if triggered by issue):
- Comment from github-actions bot
- Link to the created PR

### Output Files

After successful generation, you'll find:

```
.specify/
└── specs/
    └── 001/  (or next available number)
        ├── spec.md          ← Main specification
        ├── architecture.md  ← System design
        └── api.md          ← API documentation
```

## Troubleshooting

### Workflow doesn't start

**Check**:
- Workflow file is in `.github/workflows/`
- Actions are enabled (Settings → Actions)
- Issue has correct label (`spec-request`)

### Permission denied error

**Fix**:
1. Settings → Actions → General
2. Enable "Read and write permissions"
3. Enable "Allow GitHub Actions to create and approve pull requests"
4. Re-run the workflow

### spec-kit not found

**This is normal** - the workflow installs spec-kit automatically.

If you see this error, check that the workflow includes:
```yaml
- name: Install dependencies
  run: |
    npm install -g @github/spec-kit
```

### No PR created

**Check**:
1. Actions tab for error messages
2. Workflow logs for details
3. Branch was created (see branches list)

If branch exists but no PR:
```bash
# Create PR manually
gh pr create --title "Specs: your topic" --body "Auto-generated specs"
```

## Next Steps

### 1. Review the Generated Specs

Click on the PR and review:
- spec.md - Is it complete?
- architecture.md - Is the design sound?
- api.md - Are the endpoints correct?

### 2. Make Adjustments (Optional)

You can edit the files directly in the PR:
1. Click on a file in the PR
2. Click the pencil icon (Edit)
3. Make changes
4. Commit to the PR branch

### 3. Merge the PR

Once satisfied:
1. Approve the PR (if reviews required)
2. Click "Merge pull request"
3. Specs are now in your main branch!

### 4. Generate Implementation Plan

```bash
# Pull the latest changes
git pull origin main

# Run jules-planner on the specs
jules-planner --spec-dir .specify/specs/001/
```

## Customization

### Change the Trigger Label

Edit `.github/workflows/generate-specs-on-issue.yml`:

```yaml
if: contains(github.event.issue.labels.*.name, 'your-custom-label')
```

### Change the Command

Edit `.github/workflows/generate-specs-on-comment.yml`:

```yaml
if: contains(github.event.comment.body, '/your-command')
```

### Add Issue Template

Create `.github/ISSUE_TEMPLATE/spec-request.yml` to provide a form for users.

See the example in this repository.

## Advanced Setup

### Enable Only What You Need

Don't need all three workflows? Delete the ones you don't want:

- Only manual triggers? Keep `generate-specs-manual.yml`
- Only issue-based? Keep `generate-specs-on-issue.yml`
- Only comment commands? Keep `generate-specs-on-comment.yml`

### Multiple Repositories

For organizations with multiple repos:

1. Create a template repository with the workflows
2. Clone it when creating new repos
3. Or use repository templates feature

### Integration with Project Boards

Add to any workflow after PR creation:

```yaml
- name: Add to Project Board
  run: |
    gh project item-add YOUR_PROJECT_NUMBER \
      --owner ${{ github.repository_owner }} \
      --url ${{ steps.create-pr.outputs.pr_url }}
```

## Support

- 📖 [Full Documentation](GITHUB_INTEGRATION.md)
- 💬 [Discussions](https://github.com/maravedi/jules-specs/discussions)
- 🐛 [Report Issues](https://github.com/maravedi/jules-specs/issues)

## Summary

You now have:
- ✅ Automated spec generation from issues
- ✅ Command-based triggering via comments
- ✅ Manual trigger via GitHub UI
- ✅ Automatic PR creation
- ✅ Structured spec output

**Ready to generate your first spec?** Create an issue with the `spec-request` label!
