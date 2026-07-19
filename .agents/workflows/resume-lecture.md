# Resume an interrupted lecture run

Activate `lecture-orchestration`.

Read `output/run_manifest.json`, recompute input hashes and verify every recorded output hash. Mark changed or missing stages stale. Resume from the earliest stale dependency; do not trust file existence alone. Never delete valid intermediate artifacts merely to simplify the run. At completion, execute strict validation and update the manifest.
