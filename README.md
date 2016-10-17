# git-notifyme

A python script to watch and notify you of commits on various branches of your git repositories.

# Usage

```bash
python notifyme.py repo1, repo2 --interval 00:00:10
```

If the interval is left out, it defaults to 1 minute

You can also set the remote and branch to watch by specifying `--remote` and `--branch` respectively

git-notify doesn't get in your way when watching for updates (it only does a `fetch` it's up to you to `merge`)

# Notes

For now there is no support to watch two or more branches at the same time, but this is a feature i'm actively working on.

# Found it interesting or useful?

Give it a star :)
