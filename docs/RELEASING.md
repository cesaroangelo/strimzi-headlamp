# Releasing

Releases use semantic versioning and run from `main`.

## Steps

1. Merge your work into `main` through a pull request, with all checks green.

2. Tag the release from `main`:

   ```bash
   git checkout main && git pull origin main
   npm version patch   # or minor, or major
   ```

   `npm version` updates `package.json`, commits, and creates the `vX.Y.Z` tag.

3. Push the commit and the tag:

   ```bash
   git push origin main
   git push origin vX.Y.Z
   ```

The tag starts `release.yml`, which checks that the tag matches the version
in `package.json`, runs the tests, builds and packages the plugin, works out
the SHA-256 checksum, updates `artifacthub-pkg.yml`, and creates the GitHub
release.

If the tag and `package.json` disagree, the workflow stops. Fix the version
and tag again.

## Before you tag

- Add a `CHANGELOG.md` entry for the new version.
- Run `npm run licenses` if any runtime dependency changed, so the bundled
  licence notices stay correct.

## Publishing to npm

The release workflow does not publish to npm. Do it by hand after the
GitHub release:

```bash
npm publish --access public
```
