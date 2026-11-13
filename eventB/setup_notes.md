# Event B – Z1: Code2DFD setup notes

Recorded 2026-11-12 by Zexu (Nujs-0927), updated 2026-11-13.

Paths below are on the local working folder, which is not in this repo:

| Local | Contents | In this repo |
|---|---|---|
| `tools/code2DFD/` | Code2DFD fork clone, plus `analysed_repositories/` (App 6 copy, config repo) and `output/` | outputs copied to `eventB/runs/` |
| `tools/venv/` | Windows virtual environment (import smoke test only) | – |
| `tools/Dockerfile.code2dfd` | Linux runtime actually used for the runs | `eventB/tools/Dockerfile.code2dfd` |
| `run_before_windows_FAILED.log` | failed native Windows run | `eventB/runs/discarded/windows_native_FAILED.log` |
| `discarded_runs/before_without_config_repo/` | container run without the config repo | `eventB/runs/discarded/no_config_repo/` |

To rebuild App 6 before/after: export `tool_comparison/analyzed_applications/spring-netflix-oss-microservices` from the replication repo @ `1b89944` (see "Z2 copy" below), then apply `eventB/runs/after/app.diff`.

## Tool version

- Code2DFD, the study's own fork: https://github.com/M3SOulu/EMSE2025SAR-code2DFD
- Commit: `39763f4798b4d779d97656ec7135c98da440a7d7` (2024-11-04, "fix: add init file")
- This is the commit pinned as the `EMSE2025SAR-code2DFD` submodule in https://github.com/M3SOulu/EMSE2025SAR-Tools, i.e. the version the study used.

## Environment

- Windows 11 Pro, Python 3.12.10, fresh virtual environment (`tools/venv`)
- OpenJDK 21.0.12.1 present (not needed: PNG rendering uses the PlantUML web server, see below)

## Dependencies (deviation from the fork's requirements.txt)

`requirements.txt` pins: Flask==2.1.2, plantuml==0.3.0, PyYAML==6.0, requests==2.26.0, ruamel.base==1.0.0.

Following the group plan, these were installed **unpinned**, plus `ruamel.yaml`, because the code imports `ruamel.yaml` (`core/parse_files.py`) while requirements.txt only lists `ruamel.base`. The pinned set was not attempted.

Installed versions (`pip freeze`):

```
blinker==1.9.0
certifi==2026.10.23
charset-normalizer==3.5.2
click==8.5.1
Flask==3.1.3
httplib2==0.32.1
idna==3.20
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.4
plantuml==0.3.0
pyparsing==3.3.3
PyYAML==6.0.3
requests==2.34.2
ruamel.yaml==0.19.1
six==1.17.0
urllib3==2.8.0
Werkzeug==3.1.9
```

`six` was added after the first import test failed with `ModuleNotFoundError: No module named 'six'`: `plantuml==0.3.0` imports `six` but does not declare it as a dependency.

On Python 3.12 the import also prints `SyntaxWarning: invalid escape sequence '\$'` for `technology_specific_extractors/docker_compose/dcm_parser.py` (lines 524, 546, 556). These are warnings only: the strings still contain a literal backslash, so behaviour is unchanged.

Compatibility check: `core/parse_files.py` uses `ruamel.yaml.scalarstring.PreservedScalarString`; ruamel.yaml 0.19.1 still provides it as an alias of `LiteralScalarString` (`scalarstring.py` line 63).

## How this fork is run

- There is no `--config_path` option in this fork. `main()` in `code2DFD.py` always reads `config/config.ini` relative to the working directory, so it must be run from the `code2DFD` folder.
- The app to analyse is set by `[Repository] path = <org>/<repo>` in `config/config.ini` (or as the single command-line argument).
- If `./analysed_repositories/<repo>` already exists, that local copy is analysed; otherwise the tool runs `git clone https://github.com/<org>/<repo>.git`. For Event B the local App 6 copy is placed there so nothing is downloaded.
- Command (from `tools/code2DFD`): `..\venv\Scripts\python.exe code2DFD.py`
- PNG output sends the generated PlantUML source to http://www.plantuml.com, so it needs internet access.
- Output goes to `./output/{results,architecture,traceability,codeable_models,png,logs}/`. Only `logs/` is created by the code; the others are git-ignored and missing in a fresh clone, so they were created by hand (`mkdir`) before the first run, otherwise writing the results fails.
- Config change for Event B (only change to the tool clone): in `config/config.ini`, `path = apssouza22/java-microservice` commented out and `path = fernandoabcampos/spring-netflix-oss-microservices` un-commented.

## Runtime used for the Event B runs: Linux container (Windows native run fails)

- First native Windows run (2026-11-13 03:03) crashed before any output: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb2` in `core/file_interaction.py:get_file_as_lines` (log: `run_before_windows_FAILED.log`).
- Cause: Code2DFD calls the Unix tools `find` and `grep` through `subprocess.Popen` (`core/file_interaction.py` lines 124, 495, 523). On Windows, `find` resolves to `C:\Windows\System32\find.exe`, a different program, whose (GBK-encoded) error message cannot be decoded as UTF-8. Windows' process search checks System32 before PATH, so running from Git Bash would not fix it.
- Response: no change to Code2DFD's code. The tool is run in a Linux container instead (`tools/Dockerfile.code2dfd`): `python:3.12-slim`, Python 3.12.16, the same package versions as above (verified with `pip freeze` in the image), GNU `find`/`grep` in `/usr/bin`. The `code2DFD` folder (tool, config, `analysed_repositories/`, `output/`) is bind-mounted at `/work`.
- Image: `code2dfd-g15:py312`, built with `docker build -t code2dfd-g15:py312 -f Dockerfile.code2dfd .` from `tools/`.
- Run command (from PowerShell): `docker run --rm -v "<path>\tools\code2DFD:/work" code2dfd-g15:py312`

## App 6 source

- Replication package https://github.com/M3SOulu/EMSE2025SAR-Replication at commit `1b8994471e9df0d32e22b31415eead8511078125` (same commit as Event A)
- Folder `tool_comparison/analyzed_applications/spring-netflix-oss-microservices` (a copy stored in the replication repo; upstream project `fernandoabcampos/spring-netflix-oss-microservices`)

### External config repository (needed by Code2DFD's Spring Config extractor)

- App 6's `config-server/src/main/resources/application.yml` points to `https://github.com/fernandoabcampos/microservices-config.git`. Code2DFD (`technology_specific_extractors/spring_config/cnf_entry.py`) clones that repo into `analysed_repositories/microservices-config` and reads the service configs from it.
- The first container run (03:11) had no `git` in the image, so that clone failed (`sh: 1: git: not found`) and the config data was missing. That run was discarded (kept in `discarded_runs/before_without_config_repo/`).
- Fix: the config repo was cloned beforehand at its latest commit `bb5da241f20537049f0c1cb569535a0b6ca4666a` (2016-06-18, unchanged since then, so the same content the study would have cloned), with `core.autocrlf=false`. Code2DFD finds the folder and does not try to clone.

### Z2 copy (byte-exact)

- Exported with `git -c core.autocrlf=false archive 1b89944:<folder> | tar -x` into `tools/code2DFD/analysed_repositories/spring-netflix-oss-microservices`, then `git init` with `core.autocrlf=false`, `mvnw` files marked executable, one commit.
- App repo commit: `09baaa594d9881be85eb28409ab64514b91d44e1` ("App 6 unchanged …")
- Root tree hash `684425cbf5f886dd78ced20efb6916c2015e4148` is identical to the replication repo's tree for that folder, so the copy is byte-identical to what the study analysed.
- Why the care: a first plain copy on Windows (Git's default `autocrlf=true`) turned LF into CRLF in the working files and changed 3 Dockerfiles + `pom.xml` and the `mvnw` mode on commit (tree `305cdcc…` ≠ source). That copy was discarded.

## Smoke test

- [x] `..\venv\Scripts\python.exe -c "import code2DFD; print('import OK')"` from `tools/code2DFD`: prints `import OK` (2026-11-12), after adding `six`. Only the SyntaxWarnings above are shown.
