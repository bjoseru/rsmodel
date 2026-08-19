# Changelog

All notable changes to `rsmodel` and to this repository are recorded here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [semantic versioning](https://semver.org/).

The version in `rsmodel/rsmodel/__init__.py` is the single source of truth. A
release is a git tag `vX.Y.Z` matching it — the release workflow refuses to run
if the two disagree.

## [Unreleased]

## [0.1.1] — 2026-08-19

### Changed

- _describe this release_

## [0.1.0] — 2026-08-19

First public release.

### Added

- `rsmodel` package: `RSModel`, `RS2Model`, `Patient`, symbolic analysis helpers
  (Jacobians, corner and interior equilibria, Lyapunov verification) and
  predefined adversity scenarios.
- Three marimo notebooks: interactive playground, symbolic analysis behind the
  manuscript, and a regenerator for every figure in the paper.
- `tools/export_playground.py`: vendors the package into the notebook and
  exports a self-contained WebAssembly site.
- Continuous deployment of the playground to <https://rsmodel.org>.
- Publication to PyPI via trusted publishing; archival on Zenodo per release.

[Unreleased]: https://github.com/bjoseru/rsmodel/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/bjoseru/rsmodel/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/bjoseru/rsmodel/releases/tag/v0.1.0
