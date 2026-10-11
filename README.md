# Felipe Amorim portfolio

The portfolio source lives in [`beta/`](beta/README.md). GitHub Actions builds and deploys its public-only release to the root portfolio URL: https://felipecaroe.github.io/portfolio/.

The deployed export excludes review files, templates, build scripts, the working case index and Mi Mundo. Beta preview pages remain `noindex` and are not included in the public deployment.

## Build and verify

```sh
python3 beta/scripts/build_site.py
python3 beta/scripts/audit_site.py
python3 beta/scripts/prepare_release.py
```

The generated public package is written to `.release/public/`. Deployments run from `main` after changes under `beta/` or the deployment workflow.

Local preview: http://localhost:8766/beta/.
