# Filesystem disappearance + history triage

Session note: a directory at `/Users/bernardchase/Documents/unordered_map/priority_queue/sum/square/y_i/transform` appeared in a tmux pane, was shown as empty with `ls -alh`, and later tested as missing. The investigation found:

- the parent directory still existed
- the target directory had already been empty in the pane output
- no explicit `rm`, `rmdir`, or `mv` mentioning that exact path appeared in the saved shell history
- a delete-like command elsewhere in history (`find ... -type d -empty -delete`) applied to a different project tree, so it was not evidence of this directory's deletion

Useful triage pattern for similar cases:
1. Capture the live tmux pane around the last known-good marker.
2. Check whether the directory was already empty before it vanished.
3. Search shell history for exact path matches first, then broad delete/move patterns (`rm -rf`, `rmdir`, `mv`, `find ... -empty -delete`, `git rm`).
4. Treat absence of a matching command as a clue: the removal may have happened in another shell, process, cleanup job, or earlier in a different history file.
5. Verify parent directory mtime/ctime to separate ordinary navigation from a real filesystem change.

This note complements the main debugging workflow when the symptom is "the directory is gone" rather than "the code is broken."