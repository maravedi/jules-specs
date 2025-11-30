"""Command-line interface for jules-specs."""

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


def get_prompt_input() -> str:
    """Get prompt from CLI argument or stdin."""
    parser = argparse.ArgumentParser(
        description="Generate specifications using GitHub spec-kit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jules-specs "Build a photo organizer app"
  echo "Build a CMMC-compliant system" | jules-specs
  jules-specs --enhance "Create a REST API"
        """
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="The specification prompt (or read from stdin if not provided)"
    )
    parser.add_argument(
        "--enhance",
        action="store_true",
        help="Enhance specification with Jules compliance critique"
    )
    parser.add_argument(
        "--output-dir",
        default=".specify/specs",
        help="Base output directory (default: .specify/specs)"
    )
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Skip automatic git commit"
    )

    args = parser.parse_args()

    # Get prompt from argument or stdin
    if args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    else:
        parser.error("Prompt required as argument or via stdin")

    if not prompt:
        parser.error("Prompt cannot be empty")

    return prompt, args


def get_next_spec_number(base_dir: Path) -> str:
    """Find the next available spec number (001, 002, etc.)."""
    if not base_dir.exists():
        return "001"

    existing_dirs = [
        d.name for d in base_dir.iterdir()
        if d.is_dir() and re.match(r'^\d{3}$', d.name)
    ]

    if not existing_dirs:
        return "001"

    max_num = max(int(d) for d in existing_dirs)
    return f"{max_num + 1:03d}"


def run_speckit(prompt: str, output_dir: Path) -> bool:
    """Invoke spec-kit CLI to generate specifications."""
    print(f"🔧 Generating specifications with spec-kit...")
    print(f"📝 Prompt: {prompt}")
    print(f"📂 Output: {output_dir}")

    try:
        # Run the specify CLI command
        cmd = [
            "specify",
            "cli",
            "spec",
            prompt,
            "--output",
            str(output_dir)
        ]

        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

        print("✅ Spec-kit generation completed")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running spec-kit: {e}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Error: 'specify' CLI not found. Please install spec-kit:")
        print("   npm install -g @github/spec-kit")
        return False


def enhance_with_jules(spec_file: Path) -> bool:
    """Optionally enhance spec with Jules compliance critique."""
    if not spec_file.exists():
        print(f"⚠️  Warning: {spec_file} not found, skipping enhancement")
        return False

    print("🤖 Enhancing specification with Jules...")

    # Read existing spec
    content = spec_file.read_text()

    # Add Jules enhancement section
    enhancement = """

---

## Compliance & Security Considerations (Jules Enhancement)

This section provides additional compliance and security considerations:

### Security Requirements
- Input validation and sanitization
- Authentication and authorization
- Data encryption (at rest and in transit)
- Secure configuration management
- Logging and monitoring

### Compliance Framework Alignment
- Consider relevant standards (CMMC, SOC2, GDPR, etc.)
- Data retention and privacy requirements
- Audit trail requirements
- Access control policies

### Risk Assessment
- Identify potential security vulnerabilities
- Document threat model
- Define mitigation strategies
- Establish incident response procedures

"""

    enhanced_content = content + enhancement
    spec_file.write_text(enhanced_content)

    print("✅ Enhancement completed")
    return True


def create_git_branch(prompt: str) -> Optional[str]:
    """Create and checkout a new git branch based on the prompt."""
    # Generate branch name from prompt hash
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:8]
    branch_name = f"jules-specs-{prompt_hash}"

    try:
        # Check if we're in a git repo
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            check=True,
            capture_output=True
        )

        # Create and checkout branch
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            check=True,
            capture_output=True
        )

        print(f"🌿 Created git branch: {branch_name}")
        return branch_name

    except subprocess.CalledProcessError:
        print("⚠️  Warning: Not in a git repository, skipping branch creation")
        return None


def commit_specs(output_dir: Path, prompt: str) -> bool:
    """Commit generated specs to git."""
    try:
        # Add the specs directory
        subprocess.run(
            ["git", "add", str(output_dir)],
            check=True,
            capture_output=True
        )

        # Commit with descriptive message
        commit_msg = f"Generate specifications: {prompt[:60]}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=True,
            capture_output=True
        )

        print(f"✅ Committed specs to git")
        return True

    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Git commit failed: {e}")
        return False


def main() -> int:
    """Main CLI entry point."""
    try:
        # Get input
        prompt, args = get_prompt_input()

        # Determine output directory
        base_dir = Path(args.output_dir)
        spec_number = get_next_spec_number(base_dir)
        output_dir = base_dir / spec_number

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create git branch if not skipping commit
        if not args.no_commit:
            create_git_branch(prompt)

        # Run spec-kit
        if not run_speckit(prompt, output_dir):
            return 1

        # Enhance with Jules if requested
        if args.enhance:
            spec_file = output_dir / "spec.md"
            enhance_with_jules(spec_file)

        # Commit to git
        if not args.no_commit:
            commit_specs(output_dir, prompt)

        # Output final path
        print(f"\n✨ Specifications generated successfully!")
        print(f"📁 Output directory: {output_dir.absolute()}")
        print(f"\n💡 Next steps:")
        print(f"   jules-planner --spec-dir {output_dir}")

        return 0

    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        return 130
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
