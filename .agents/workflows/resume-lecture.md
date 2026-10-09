# Resume an interrupted lecture run

Read lecture-orchestration and .agents/references/integrity-contract.md.
Run python scripts/manifest.py next. It checks current inputs, canonical instruction/code hashes, output existence/hashes and JSON/schema validity, then invalidates dependent stages. Before reuse also run the appropriate semantic/content validator; hash equality alone is not scientific approval. Continue only ready stages with validated prerequisites. Missing inputs in legacy records requires rerunning the stage. Never fill in missing evidence or review hashes from model memory. Do not delete valid intermediates. Finish with DOCX and strict validation.
