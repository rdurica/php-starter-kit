#!/usr/bin/env python3
"""Rename template placeholders when a new repo is created from the template."""

import os
import re


def to_kebab(name: str) -> str:
    return name.lower().replace("_", "-")


def to_title(name: str) -> str:
    return " ".join(word.capitalize() for word in re.split(r"[-_]", name) if word)


def sanitize_docker(name: str) -> str:
    if not name:
        return "app"
    if name[0].isdigit():
        name = "app-" + name
    return re.sub(r"[^a-z0-9-]", "-", name)


def main():
    repo_full = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo_full:
        raise RuntimeError("GITHUB_REPOSITORY not set")

    repo_name = repo_full.split("/")[-1]
    kebab = sanitize_docker(to_kebab(repo_name))
    title = to_title(repo_name) or repo_name

    replacements = [
        (
            ".env.example",
            [
                ("COMPOSE_PROJECT_NAME=php-starter-kit", f"COMPOSE_PROJECT_NAME={kebab}"),
                ('APP_NAME="PHP Starter Kit"', f'APP_NAME="{title}"'),
            ],
        ),
        (
            ".devcontainer/devcontainer.json",
            [
                ('"name": "PHP Starter Kit"', f'"name": "{title}"'),
            ],
        ),
        (
            "src/public/index.php",
            [
                ("<title>PHP Starter Kit — Setup Wizard</title>", f"<title>{title} — Setup Wizard</title>"),
                ('<div class="hero-badge">PHP Starter Kit</div>', f'<div class="hero-badge">{title}</div>'),
                ("PHP Starter Kit &copy;", f"{title} &copy;"),
            ],
        ),
        (
            "README.md",
            [
                ('<h1 align="center">PHP Starter Kit</h1>', f'<h1 align="center">{title}</h1>'),
                ("# PHP Starter Kit", f"# {title}"),
                ("https://github.com/rdurica/php-starter-kit.git", f"https://github.com/{repo_full}.git"),
                ("https://github.com/rdurica/php-starter-kit/actions", f"https://github.com/{repo_full}/actions"),
                ("cd php-starter-kit", f"cd {repo_name}"),
            ],
        ),
        (
            "AGENTS.md",
            [
                ("# Agent Context for PHP Starter Kit", f"# Agent Context for {title}"),
            ],
        ),
    ]

    for filepath, rules in replacements:
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} not found, skipping")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original = content
        for old, new in rules:
            content = content.replace(old, new)

        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {filepath}")
        else:
            print(f"No changes: {filepath}")

    with open(".template-configured", "w", encoding="utf-8") as f:
        f.write(f"Configured from template for {repo_full}\n")
    print("Created: .template-configured")


if __name__ == "__main__":
    main()
