"""Shared utilities for devcontainer scripts."""

import json
import re
from pathlib import Path


def sanitize_name(name):
    """Convert a display name to a docker-safe identifier."""
    name = re.sub(r'[^a-zA-Z0-9_.-]', '-', name).lower()
    name = re.sub(r'-+', '-', name).strip('-')
    return name


_JSON_TOKEN_RE = re.compile(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/', re.DOTALL)


def _strip_json_comments(content):
    """Strip // and /* */ comments, leaving string literals (e.g. URLs) untouched."""
    def replace(match):
        token = match.group(0)
        if token.startswith('"'):
            return token
        return '\n' * token.count('\n')

    return _JSON_TOKEN_RE.sub(replace, content)


def load_devcontainer_json(path):
    """Read and parse devcontainer.json, stripping comments."""
    with open(path, 'r') as f:
        content = f.read()
    content = _strip_json_comments(content)
    return json.loads(content)


def get_container_name(devcontainer_config, project_path):
    """Derive a descriptive container name from devcontainer config or project dir."""
    raw = devcontainer_config.get('name', Path(project_path).name)
    return sanitize_name(raw)


def load_devcontainer_context(project_path):
    """Resolve config, devcontainer dir, and container name for a project path.

    Returns (devcontainer_config, devcontainer_dir, container_name).
    devcontainer_config is {} when no devcontainer.json exists.
    """
    devcontainer_dir = project_path / '.devcontainer'
    devcontainer_json_path = devcontainer_dir / 'devcontainer.json'

    devcontainer_config = {}
    if devcontainer_json_path.exists():
        devcontainer_config = load_devcontainer_json(devcontainer_json_path)

    container_name = get_container_name(devcontainer_config, project_path)
    return devcontainer_config, devcontainer_dir, container_name
