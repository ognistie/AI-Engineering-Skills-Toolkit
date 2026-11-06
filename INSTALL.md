# Installation

## For a coding agent

1. Resolve the requested host, scope, and skill IDs. Use the repository at `https://github.com/ognistie/AI-Engineering-Skills-Toolkit`; honor a user-provided revision. If none is provided, use the default branch and report the resolved revision. Each portable skill lives at `skills/<id>/SKILL.md`.
2. If the host offers a native skill installer, use it with the requested `skills/<id>` paths. Codex's GitHub helper accepts `--repo ognistie/AI-Engineering-Skills-Toolkit --ref <revision> --path skills/process-verifier`. Supply multiple paths for a group; use the folder inventory for all 13. Check collisions before a batch. Do not change permissions, overwrite existing skills, or guess an unknown host's discovery path.
3. Otherwise clone/download the repository, inspect the local installer, and use the command below. Verify the install and report target, path, revision, and next-session invocation. A verified folder does not prove host selection.

Native installs have no AAES receipt. Manage them with the same host installer or reinstall explicitly to a different location; the AAES lifecycle command will not adopt them silently.

## Local installer

Requires Python 3.12+. No pip dependencies. Run from the cloned or extracted repository:

```powershell
.\scripts\install.ps1 -Target codex
.\scripts\install.ps1 -Target claude -Skill process-verifier
```

```sh
sh scripts/install.sh codex
sh scripts/install.sh claude process-verifier
```

Default discovery locations: `~/.agents/skills` for Codex and `~/.claude/skills` for Claude Code (or the configured Claude root). Use `-InstallPath` in PowerShell or the third positional argument in shell to override. Use `all` as the second shell argument for a full catalog at a custom location. For project installations, point to the project's `.agents/skills` (Codex) or `.claude/skills` (Claude Code). A Codex profile with legacy discovery can explicitly target `~/.codex/skills`. If Python is not on PATH, set `AAES_PYTHON` to the executable's full path.

If installation was interrupted, rerun the same command. It skips only managed skills whose receipt and files match the source. For an older managed version, use `update`. If Windows still reports an access error after the built-in retries, close the application using the destination and try again.

## Verify, update, export

```sh
python scripts/manage.py list
python scripts/manage.py verify --target codex
python scripts/manage.py update --target codex --skill process-verifier
python scripts/manage.py remove --target codex --skill process-verifier
python scripts/manage.py export --skill process-verifier
```

Use `--destination` if install used a custom location. Use `--group routing|essential|autonomy|advanced` (pick one) or repeat `--skill` with the management CLI. Managed updates and removals preserve backups; unmanaged and locally modified copies are rejected. See [recovery and filesystem policy](docs/SECURITY.md) and [host compatibility](docs/COMPATIBILITY.md).

The [published ZIPs](dist/) match the skill sources in this revision. Local exports go to `dist/generated/` by default. When changing a skill for publication, export all packages into a fresh directory, replace the 13 published files, and run `python scripts/test_installers.py --published`.
