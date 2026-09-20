# Contributing

Thanks for your interest in the plugin.

## Getting started

```bash
git clone https://github.com/cesaroangelo/strimzi-headlamp.git
cd strimzi-headlamp
npm install
git switch -c my-change
```

## Before you open a pull request

```bash
npm run format
npm run lint
npm run tsc
npm run test
npm run build
```

To try your change in Headlamp, see [Local testing](docs/LOCAL-TESTING.md).

## Code style

- TypeScript everywhere.
- Function components with hooks.
- Comment why, not what. Explain the non-obvious choices.
- Pure logic belongs in `src/utils/`, where it can be unit tested.

## Commit messages

- One short line in the present tense: "Add", "Fix", "Update".
- Explain the reason in the body when the change is not obvious.
- Do not add trailers such as `Co-Authored-By`. Pull request checks reject them.

## Pull requests

- Update `CHANGELOG.md` under an `Unreleased` heading.
- Update the docs if behaviour changes.
- Link the related issue.

## Questions

Open an issue.
