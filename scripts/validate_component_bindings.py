#!/usr/bin/env python3
"""Validate upstream componentId declarations against the AES Component Index."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_ROOT = SKILL_ROOT / "references"
COMPONENT_ROOT = REFERENCES_ROOT / "06-components"
COMPONENT_INDEX = COMPONENT_ROOT / "index.md"


def parse_component_index() -> tuple[dict[str, Path], list[str]]:
    registrations: dict[str, Path] = {}
    owners: defaultdict[str, list[Path]] = defaultdict(list)
    errors: list[str] = []

    for line_number, line in enumerate(COMPONENT_INDEX.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] in {"组件能力", "---"}:
            continue

        component_ids = re.findall(r"`([A-Za-z][A-Za-z0-9_]*)`", cells[1])
        link_match = re.search(r"\(([^)]+\.md)\)", cells[3])
        if not component_ids or not link_match:
            errors.append(f"index.md:{line_number}: 组件行缺少 componentId 或 Reference 链接")
            continue

        reference_path = (COMPONENT_ROOT / link_match.group(1)).resolve()
        if not reference_path.is_file():
            errors.append(f"index.md:{line_number}: Reference 不存在：{reference_path.name}")
            continue

        reference_text = reference_path.read_text(encoding="utf-8")
        for component_id in component_ids:
            owners[component_id].append(reference_path)
            registrations[component_id] = reference_path
            identity_pattern = re.compile(
                rf"componentId:[^\n]*\b{re.escape(component_id)}\b"
            )
            if not identity_pattern.search(reference_text):
                errors.append(
                    f"index.md:{line_number}: {component_id} 未在 {reference_path.name} 中声明 Component 身份"
                )

    for component_id, paths in owners.items():
        if len(paths) > 1:
            names = ", ".join(path.name for path in paths)
            errors.append(f"重复登记：{component_id} -> {names}")

    indexed_references = set(registrations.values())
    for reference_path in COMPONENT_ROOT.glob("*.md"):
        if reference_path.name != "index.md" and reference_path.resolve() not in indexed_references:
            errors.append(f"Component Reference 未登记：{reference_path.name}")

    return registrations, errors


def find_upstream_component_ids() -> dict[str, list[tuple[Path, int]]]:
    declarations: defaultdict[str, list[tuple[Path, int]]] = defaultdict(list)
    pattern = re.compile(r"componentId:\s*([A-Za-z][A-Za-z0-9_]*)")

    for path in REFERENCES_ROOT.rglob("*.md"):
        if COMPONENT_ROOT in path.parents:
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for component_id in pattern.findall(line):
                declarations[component_id].append((path, line_number))

    return declarations


def main() -> int:
    registrations, errors = parse_component_index()
    declarations = find_upstream_component_ids()

    for component_id, occurrences in sorted(declarations.items()):
        if component_id not in registrations:
            locations = [
                f"{path.relative_to(SKILL_ROOT)}:{line_number}"
                for path, line_number in occurrences
            ]
            errors.append(
                f"component_gap: {component_id} 未在 Component Index 登记；来源：{', '.join(locations)}"
            )
            continue

        reference_name = registrations[component_id].name
        for path, line_number in occurrences:
            if path.parent.name not in {"04-patterns", "05-features"}:
                continue
            if reference_name not in path.read_text(encoding="utf-8"):
                relative_path = path.relative_to(SKILL_ROOT)
                errors.append(
                    f"component_gap: {relative_path}:{line_number} 声明 {component_id}，"
                    f"但未链接 {reference_name}"
                )

    if errors:
        print("Component binding validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Component binding validation passed: "
        f"{len(registrations)} registered IDs, {len(declarations)} upstream IDs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
