# Local testing

How to run the plugin against a real cluster. Build it first:

```bash
npm install
npm run build
```

The build writes `dist/main.js` and `dist/THIRD-PARTY-LICENSES.md`.

## Headlamp desktop app

Copy the build into Headlamp's plugin directory and add a `package.json`
next to it. Headlamp needs both files.

**macOS**

```bash
PLUGIN_DIR=~/Library/Application\ Support/Headlamp/plugins/strimzi
```

**Linux**

```bash
PLUGIN_DIR=~/.config/Headlamp/plugins/strimzi
```

Then:

```bash
mkdir -p "$PLUGIN_DIR"
cp -r dist/* "$PLUGIN_DIR"/
cat > "$PLUGIN_DIR/package.json" <<'JSON'
{ "name": "strimzi-headlamp", "version": "0.5.0", "main": "main.js" }
JSON
```

Quit Headlamp and open it again. A restart is not enough on some systems,
so close the app fully.

## Headlamp server

```bash
headlamp-server -plugins-dir=/path/to/strimzi-headlamp/dist
```

## Headlamp from source

```bash
cd /path/to/headlamp
export HEADLAMP_PLUGINS_DIR=/path/to/strimzi-headlamp/dist
make run-frontend
```

## Headlamp on Kubernetes

Useful to test in-cluster RBAC. Build and unpack the plugin first:

```bash
npm run build && npm run package
mkdir -p plugins
tar -xzf *strimzi-headlamp-*.tar.gz -C plugins/
```

Set the `hostPath` in `deploy/headlamp.yaml` to that `plugins` directory,
then deploy:

```bash
kubectl apply -f deploy/headlamp.yaml
kubectl -n headlamp create token headlamp --duration=24h
```

Open http://localhost:30080 and sign in with the token. To use a port
instead of the node port:

```bash
kubectl port-forward -n headlamp svc/headlamp 8080:80
```

To install a new build:

```bash
npm run build && npm run package
rm -rf plugins/strimzi-headlamp
tar -xzf *strimzi-headlamp-*.tar.gz -C plugins/
kubectl rollout restart deployment/headlamp -n headlamp
```

Reload the browser with a hard refresh (`Cmd+Shift+R` or `Ctrl+Shift+R`),
or you may still see the old bundle.

To remove it: `kubectl delete -f deploy/headlamp.yaml`.

## Sample resources

`test-files/` holds Kafka, KafkaTopic and KafkaUser manifests to try the
plugin against a cluster. See [`test-files/README.md`](../test-files/README.md)
for the apply order and cleanup steps.
