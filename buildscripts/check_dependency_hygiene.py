#!/usr/bin/env python3
"""Validate runtime/build dependency separation and minimum secure build tooling."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FORBIDDEN = {"setuptools", "pyinstaller", "pathlib"}


def parse_simple_requirements(path: Path) -> list[str]:
    entries: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line)
    return entries


def requirement_name(req: str) -> str:
    req = req.strip()
    match = re.match(r"^([A-Za-z0-9_.-]+)", req)
    if not match:
        return req.lower()
    return match.group(1).lower()


def parse_setup_install_requires(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "setup":
            continue
        for kw in node.keywords:
            if kw.arg != "install_requires":
                continue
            if not isinstance(kw.value, (ast.List, ast.Tuple)):
                raise ValueError("setup.py install_requires is not a list/tuple literal")
            values: list[str] = []
            for elt in kw.value.elts:
                if not isinstance(elt, ast.Constant) or not isinstance(elt.value, str):
                    raise ValueError("setup.py install_requires contains non-string entry")
                values.append(elt.value)
            return values
    raise ValueError("setup() call with install_requires not found in setup.py")


def parse_min_version(req: str) -> tuple[str, tuple[int, ...]]:
    name = requirement_name(req)
    match = re.search(r">=\s*([0-9]+(?:\.[0-9]+)*)", req)
    if not match:
        return name, tuple()
    version = tuple(int(p) for p in match.group(1).split("."))
    return name, version


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []

    requirements_txt = ROOT / "requirements.txt"
    runtime_reqs = parse_simple_requirements(requirements_txt)
    runtime_names = {requirement_name(req) for req in runtime_reqs}
    check(
        runtime_names.isdisjoint(RUNTIME_FORBIDDEN),
        "requirements.txt must not include build-only/backport deps: "
        + ", ".join(sorted(runtime_names & RUNTIME_FORBIDDEN)),
        errors,
    )

    setup_py = ROOT / "setup.py"
    install_requires = parse_setup_install_requires(setup_py)
    setup_names = {requirement_name(req) for req in install_requires}
    check(
        setup_names.isdisjoint(RUNTIME_FORBIDDEN),
        "setup.py install_requires must not include build-only/backport deps: "
        + ", ".join(sorted(setup_names & RUNTIME_FORBIDDEN)),
        errors,
    )

    build_reqs_path = ROOT / "buildscripts" / "requirements-build.txt"
    build_reqs = parse_simple_requirements(build_reqs_path)
    parsed_build = dict(parse_min_version(req) for req in build_reqs)
    check(
        parsed_build.get("setuptools", tuple()) >= (78, 1, 1),
        "buildscripts/requirements-build.txt must pin setuptools>=78.1.1",
        errors,
    )
    check(
        parsed_build.get("pyinstaller", tuple()) >= (6, 0, 0),
        "buildscripts/requirements-build.txt must pin pyinstaller>=6.0.0",
        errors,
    )

    pyproject_toml = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    check(
        "setuptools>=78.1.1" in pyproject_toml,
        "pyproject.toml build-system.requires must include setuptools>=78.1.1",
        errors,
    )

    flatpak_manifest = (
        ROOT / "buildscripts" / "flatpak-scripts" / "python3-requirements.yaml"
    ).read_text(encoding="utf-8")
    check(
        "python3-pathlib" not in flatpak_manifest,
        "Flatpak manifest must not include python3-pathlib",
        errors,
    )
    check(
        '"networkx~=3.6.1"' in flatpak_manifest,
        "Flatpak manifest must pin networkx~=3.6.1",
        errors,
    )
    check(
        '"watchdog==6.0.0"' in flatpak_manifest,
        "Flatpak manifest must pin watchdog==6.0.0",
        errors,
    )
    check(
        '"pygame~=2.6.1"' in flatpak_manifest,
        "Flatpak manifest must pin pygame~=2.6.1",
        errors,
    )

    if errors:
        print("Dependency hygiene check failed:")
        for err in errors:
            print(f" - {err}")
        return 1

    print("Dependency hygiene check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

