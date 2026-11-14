/**
 * Guards `npm publish` (run from prepublishOnly).
 *
 *   node scripts/check-publish.mjs node   Node is a version the build supports
 *   node scripts/check-publish.mjs dist   the build produced the plugin
 *
 * 0.5.0 reached npm without dist/: it was published on Node 26, where the
 * Headlamp SDK's build fails, and the publish went ahead anyway.
 */
import fs from 'node:fs';

const SUPPORTED = [22, 24];

export function checkNode(version) {
  const major = Number(version.split('.')[0]);
  if (!SUPPORTED.includes(major)) {
    return `Node ${version} cannot build this plugin. Use Node ${SUPPORTED.join(' or ')} (see .nvmrc).`;
  }
  return null;
}

export function checkDist(dir = 'dist') {
  if (!fs.existsSync(`${dir}/main.js`)) {
    return `${dir}/main.js is missing: the build did not produce the plugin. Refusing to publish.`;
  }
  return null;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const what = process.argv[2];
  const error = what === 'node' ? checkNode(process.versions.node) : what === 'dist' ? checkDist() : 'usage: check-publish.mjs node|dist';
  if (error) {
    console.error(`✖ ${error}`);
    process.exit(1);
  }
  console.log(`✔ publish check passed: ${what}`);
}
