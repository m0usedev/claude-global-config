---
name: generate-claude-md-code-project
description: Analyze the current code project and generate (or refresh) its CLAUDE.md using a fixed template — overview, drift rule, tech stack with versions, annotated structure, where new code goes, commands, conventions, testing expectations, Do NOT, useful context. Use when asked to create, generate, bootstrap or update a CLAUDE.md for a codebase.
---

# Generate a CLAUDE.md for this code project

Goal: produce a CLAUDE.md that tells a future Claude Code session how this project *actually* works, so it can write code that fits in on the first try. Every statement must be backed by something you read in the repo. Wrong context is worse than missing context.

## 1. Check what already exists
- Look for `CLAUDE.md` at the repo root and at `.claude/CLAUDE.md`, plus any `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md` or `CONTRIBUTING.md`.
- If a CLAUDE.md exists, read it and treat it as input. Keep anything that is still true. For anything that contradicts the code, flag it to the user; do not silently overwrite it.
- Target path: update the existing file wherever it is. If none exists, use `.claude/CLAUDE.md`.

## 2. Analyze the project (read-only)
Read the evidence first and write afterwards. For large repos, use an Explore agent to sweep the directories.
- **Manifests and lockfiles**: package.json, pyproject.toml, Pipfile/Pipfile.lock, requirements*.txt, go.mod, Cargo.toml, pom.xml, build.gradle, composer.json, Gemfile, *.csproj. Take exact versions from the lockfile or the pinned manifest entry.
- **Runtime and environment**: language version files (.python-version, .nvmrc, .tool-versions), the virtualenv/node_modules location, Dockerfile, docker-compose.
- **Entry points**: app factory, main, server bootstrap, router registration, middleware, DI setup.
- **Layout**: the top two levels of the source tree. Open one or two representative files per directory so you know what the directory is really for, not just what its name suggests.
- **Patterns**: base classes and generics that others subclass, how layers call each other (endpoint → service → repository), error/exception flow, response wrapping, config split (static constants vs. env/runtime config), logging, auth.
- **Data**: ORM/DB drivers, migrations (or the absence of migrations and what is used instead), models location.
- **Commands**: scripts in package.json, Makefile, tox.ini, noxfile, justfile, CI workflows (.github/workflows, .gitlab-ci.yml) for install, dev server, tests, lint, build.
- **Tests**: test dirs, config (pytest.ini, conftest.py, jest/vitest config), fixtures, and how real or thin the suite is.
- **Legacy/frozen code**: versioned modules (v1/v2), deprecated folders, generated code, vendored code. Check `git log` on them to see which version is active.
- **Recent activity**: `git log --oneline -20` to see what is being worked on.

If a file can't be read (permission deny, missing, or encrypted), don't guess its contents. Record the gap in the CLAUDE.md, say why the file couldn't be read, and say what would unblock it.

## 3. Write the file using this template
Keep the headings and order exactly. Fill every section from evidence. Delete placeholder text. Use repo-relative paths. Be concise: bullets over prose, and no generic advice like "write clean code" or "follow best practices".

```markdown
# CLAUDE.md

## Project overview
<2–4 sentences: what the system does in business terms, who/what calls it, its main input → output.>

## When something doesn't add up

This file, what you've told me earlier in a conversation, and what the code actually does can drift out of sync — you're human, and you may contradict a rule here by accident or on purpose, the codebase changes, or my own notes here may just be wrong or outdated. When I notice one of these mismatches, I should not silently pick one and proceed, and I should not silently overwrite this file to match whatever just happened. Instead, stop and ask, stating plainly what I observed on each side (e.g. "CLAUDE.md says X, but you just asked for Y — which should I follow here, and should this file be updated?"). Once you clarify, I'll ask whether the resolution should also be written back into this file so it doesn't need to be re-asked next time.

## Tech stack
- Language/runtime: <language + exact version>
- Environment: <package manager, manifest/lock paths, venv/node_modules location>
- Framework: <framework + version, server/runner>
- Database: <engines + drivers/ORM + versions; how schema changes are applied (migrations tool or alternative)>
- Key libraries:
  - <lib version — what it's used for here>

## Project structure

<Where app code lives, if not the root.>

```
<annotated tree, top 1–2 levels; one comment per entry saying what it holds and the pattern inside,
 e.g. "one class per integration, subclassing BaseAPIService (base_api_service.py)">
```

### Where new code goes
- New <kind of thing> → `<path pattern>`, <base class / registration step>
- ...

## Commands
- Install: `<cmd>`
- Dev server: `<cmd>` (from `<dir>`)
- Run tests / lint: `<cmd>`
- Build: `<cmd>`
<Mark any command you could not confirm as "not yet confirmed" and say why.>

## Conventions
- <Pattern actually followed across the codebase, with the file that defines it>
- ...

## Testing expectations
<What exists (framework, fixtures, coverage). If the suite is thin or a placeholder, say so plainly and call it a known gap, not a pattern to mimic.>

## Do NOT
- <Frozen/legacy code not to edit, and what to target instead>
- <Things the framework does automatically that must not be duplicated>
- <Accepted deviations from "best practice" that must not be "fixed" unprompted>

## Useful context
- <Auth, response formats, core domain state machines/enums, non-obvious coupling, unreadable files and how to unblock them>
```

Rules while filling:
- Copy the "When something doesn't add up" section verbatim. It is project-independent.
- Every convention must be visible in at least two places in the code, or defined in a base class. Otherwise it's an observation, not a convention.
- Distinguish "this is how it is done" from "this is a gap". Never present a gap as a pattern to follow.
- Give versions only when you read them. Write "version not pinned" rather than guessing.
- Leave a section out only if it truly doesn't apply (e.g. no database). Do not pad.

## 4. Confirm before writing
Only the team can answer some things: which code is frozen, which deviations are intentional, and which domain terms matter. Before writing the file:
1. Show the user a short summary of the draft. List the items you inferred but couldn't verify, and ask about them with AskUserQuestion (max 4 questions; most important first).
2. If a CLAUDE.md already exists, show what will change and get confirmation before overwriting.
3. Write the file and report its path, plus any gaps left marked as "not yet confirmed".
