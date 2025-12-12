#!/usr/bin/env python3
"""Check for lines exceeding the maximum line length in Python files."""

from pathlib import Path

MAX_LENGTH = 120


def check_line_lengths(src_dir: str = "src", max_length: int = MAX_LENGTH) -> list[dict]:
    """
    Check all Python files for lines exceeding the maximum length.

    Args:
        src_dir: Directory to scan (default: "src")
        max_length: Maximum allowed line length (default: 120)

    Returns:
        List of violations with file, line number, and length
    """
    violations = []

    for py_file in Path(src_dir).rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue

        with open(py_file, "r") as f:
            for line_num, line in enumerate(f, 1):
                line_content = line.rstrip("\n\r")
                if len(line_content) > max_length:
                    violations.append(
                        {
                            "file": str(py_file),
                            "line": line_num,
                            "length": len(line_content),
                            "content": line_content,
                        }
                    )

    return violations


def main():
    """Main function to check and report line length violations."""
    print(f"Checking for lines exceeding {MAX_LENGTH} characters...\n")

    violations = check_line_lengths()
    violations.sort(key=lambda x: (x["file"], x["line"]))

    if not violations:
        print(f"✓ All lines are within {MAX_LENGTH} characters!")
        return

    # Group by file
    files_with_violations = {}
    for v in violations:
        rel_path = v["file"].replace("src/", "")
        if rel_path not in files_with_violations:
            files_with_violations[rel_path] = []
        files_with_violations[rel_path].append(v)

    # Print summary by file
    print("=" * 80)
    print("LINE LENGTH VIOLATIONS")
    print("=" * 80)
    print()

    for file_path, file_violations in sorted(files_with_violations.items()):
        print(f"\n{file_path}:")
        for v in file_violations:
            print(f"  Line {v['line']:4d}: {v['length']} chars")
            # Show first 100 chars of the line
            preview = v["content"][:100]
            if len(v["content"]) > 100:
                preview += "..."
            print(f"           {preview}")

    # Print overall summary
    print()
    print("=" * 80)
    print(f"Total: {len(violations)} violations in {len(files_with_violations)} files")
    print("=" * 80)

    # Print top offenders
    print("\nTop 5 longest lines:")
    top_violations = sorted(violations, key=lambda x: x["length"], reverse=True)[:5]
    for i, v in enumerate(top_violations, 1):
        rel_path = v["file"].replace("src/", "")
        print(f"{i}. {rel_path}:{v['line']} - {v['length']} chars")


if __name__ == "__main__":
    main()
