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
the SHA-256 checksum, creates the GitHub release, and publishes the Artifact
Hub metadata.

## Artifact Hub metadata

Each release has its own directory, `<version>/artifacthub-pkg.yml`. The
release workflow writes a new one after the build, when it knows both the
archive URL and its checksum, then opens and merges that pull request itself.

Never edit these files by hand, and never bump a version in one. A file that
names one version while still pointing at the previous archive is a state
Artifact Hub can index, and it will keep serving the wrong archive until the
next version appears. That is what happened to 0.5.0: the catalog offered
0.5.0 and installed 0.3.9 for six weeks.

Two checks guard this. Pull request validation rejects a metadata file whose
version, directory and archive URL disagree. `artifacthub-drift.yml` runs
daily, compares what Artifact Hub serves against the latest release, and
opens an issue when they differ.

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
