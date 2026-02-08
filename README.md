# alembic-version-tool

A simple tool for assiting with managing Alembic migrations files.

At the moment there is only one function implelented: `alembic-versions
branch`, which will search all of the commits in the current branch for newly
added Alembic migration files, and print out a list of version hashes and
their Alembic commit message.

This information can be used to decide if any migrations should be squashed
before sending a PR for the branch.

```bash
alembic-versions branch -g "$(which git)" -v ./alembic/versions -b origin/main
``` 

This will look through all the commits from `origin/main` up to `HEAD`.
