from pathlib import Path


def remove_generated_files(root: Path = Path(".")) -> int:
    count = 0
    for folder in ("storage/raw", "storage/processed", "storage/curated", "monitoring/logs"):
        for path in (root / folder).glob("*"):
            if path.is_file() and path.name != ".gitkeep":
                path.unlink()
                count += 1
    return count


if __name__ == "__main__":
    print(f"removed {remove_generated_files()} generated files")
