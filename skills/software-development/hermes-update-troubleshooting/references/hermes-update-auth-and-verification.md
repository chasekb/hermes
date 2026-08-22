# Hermes update auth and verification reference

Use this sequence after capturing the failure. Keep secrets out of output.

## Evidence sequence

1. Capture the tmux pane and isolate output after the last `hermes update`.
2. In the Hermes home checkout and installed source checkout, run:

```bash
git remote -v
git status --short --branch
git ls-remote origin HEAD
```

3. If the remote is GitHub SSH and the user is already authenticated with GitHub CLI:

```bash
gh auth status
gh auth setup-git
git remote set-url origin https://github.com/OWNER/REPO.git
git ls-remote origin HEAD
```

Apply the remote change independently in each checkout that needs it. Do not print credential-helper contents or embed a token in a URL.

4. Retry the cheap check first:

```bash
hermes update --check
```

5. Run the supported update command, preserving local work. If the user explicitly accepts skipping Hermes's pre-update backup and a recovery path exists:

```bash
hermes update --yes --no-backup
```

6. Verify:

```bash
hermes update --check
hermes doctor
```

7. For tests, confirm interpreter and package availability before running pytest:

```bash
python -c 'import sys; print(sys.executable)'
python -m pytest --version
```

Use the project's managed interpreter/test runner. A collection failure caused by an unrelated system interpreter is an environment-selection issue, not proof of a source regression.

## Report fields

- captured pane and marker used;
- failing boundary and first meaningful error;
- checkout remotes changed, without credentials;
- `git ls-remote` result;
- update result and major post-update stages;
- `hermes update --check` result;
- `hermes doctor` result;
- test interpreter, command, and whether collection reached actual tests;
- remaining warnings or blockers.
