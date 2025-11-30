# jules-specs

A specification generator that wraps GitHub's [spec-kit](https://github.com/github/spec-kit) tool to create structured specifications for the jules-planner workflow.

## Overview

jules-specs is the first step in a three-stage development workflow:

1. **jules-specs** (this tool) - Generate specifications using GitHub spec-kit
2. **jules-planner** - Generate tasks and implementation plans from specs
3. **Implementation** - Execute the plan with Claude/Jules or other tools

## Installation

### Prerequisites

1. **Install spec-kit** (GitHub's specification toolkit):
   ```bash
   npm install -g @github/spec-kit
   ```

2. **Install jules-specs**:
   ```bash
   pip install jules-specs
   ```

   Or install from source:
   ```bash
   git clone https://github.com/maravedi/jules-specs.git
   cd jules-specs
   pip install -e .
   ```

## Usage

### Basic Usage

Generate specs from a prompt:

```bash
jules-specs "Build a photo organizer app"
```

### Pipe Input

You can also pipe input:

```bash
echo "Build a CMMC-compliant photo organizer app" | jules-specs
```

### Enhanced Mode

Add compliance and security considerations with Jules enhancement:

```bash
jules-specs --enhance "Create a REST API for user management"
```

### Options

- `--enhance` - Add Jules compliance critique to specifications
- `--output-dir DIR` - Specify output directory (default: `.specify/specs`)
- `--no-commit` - Skip automatic git commit

## Workflow

When you run jules-specs, it:

1. **Extracts the prompt** from CLI argument or stdin
2. **Finds the next spec number** (001, 002, 003, etc.)
3. **Invokes spec-kit CLI**: `specify cli spec "prompt" --output .specify/specs/001/`
4. **Generates files**:
   - `.specify/specs/001/spec.md` - Main specification
   - `.specify/specs/001/architecture.md` - System design
   - `.specify/specs/001/api.md` - OpenAPI spec (if applicable)
5. **Enhances with Jules** (if `--enhance` flag used) - Adds compliance critique
6. **Creates git branch**: `jules-specs-<hash>`
7. **Commits changes** to git
8. **Outputs path** for next step

## Example Workflow

```bash
# Step 1: Generate specifications
jules-specs "Build CMMC-compliant photo organizer app"
# Output: .specify/specs/001/

# Step 2: Generate plan from specs
jules-planner --spec-dir .specify/specs/001/
# Output: tasks + implementation plan

# Step 3: Implement (with Claude, Jules, or manually)
```

## Output Structure

```
.specify/
└── specs/
    ├── 001/
    │   ├── spec.md
    │   ├── architecture.md
    │   └── api.md
    ├── 002/
    │   ├── spec.md
    │   ├── architecture.md
    │   └── api.md
    └── ...
```

## Git Integration

jules-specs automatically:
- Creates a new branch `jules-specs-<hash>` based on your prompt
- Commits the generated specifications
- Prepares the branch for PR creation

To skip git operations:
```bash
jules-specs --no-commit "Your prompt here"
```

## Development

### Running from Source

```bash
python -m jules_specs "Your prompt"
```

### Testing

```bash
# Test basic functionality
jules-specs "Build a simple REST API"

# Test enhanced mode
jules-specs --enhance "Build a secure user authentication system"

# Test without git
jules-specs --no-commit "Build a file processor"
```

## Requirements

- Python >= 3.8
- spec-kit (npm package: `@github/spec-kit`)
- git (for auto-commit features)

## License

MIT

## Links

- [GitHub spec-kit](https://github.com/github/spec-kit)
- [jules-planner](https://github.com/maravedi/jules-planner)
