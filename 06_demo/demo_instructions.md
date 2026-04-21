# Viva Demo Instructions (3-5 Minutes)

This folder provides a standalone viva demo that does not depend on `DL23.ipynb`.

## Why the base model may appear as a symlink

`Models/Qwen2.5-1.5B-Instruct` was initially linked to the local Hugging Face cache to avoid duplicating a large model file in the repository.

- Benefit: much smaller workspace footprint and faster setup on the same machine.
- Limitation: on a new machine, that old cache path does not exist.

The notebook is now updated to handle this automatically: if the base model path is missing or a broken symlink, it downloads `Qwen/Qwen2.5-1.5B-Instruct` directly into `06_demo/Models`.

## Folder Contents

- `sample_inputs.txt`: meaningful demo prompts (copied from ` 04_data/sample_inputs.txt`).
- `Models/`:
   - `Qwen2.5-1.5B-Instruct` (local base model directory; may start as symlink and then get materialized on new machine)
  - `phase8_adapter_grpo_pilot` (LoRA adapter used in viva demo)
- `Demo.ipynb`: self-contained demo notebook.
- `requirements.txt`: Python dependencies for the demo.
- `setup_demo_venv.sh`: one-command isolated environment setup.

## Recommended Setup (isolated venv)

1. From the `06_demo` folder run:
    - `bash setup_demo_venv.sh`
2. Open `06_demo/Demo.ipynb`.
3. Select kernel: `Demo Venv (06_demo)`.
4. Run cells in order.

## One-Time Check (before viva)

1. Confirm model artifacts exist:
   - `06_demo/Models/Qwen2.5-1.5B-Instruct`
   - `06_demo/Models/phase8_adapter_grpo_pilot/adapter_model.safetensors`
2. Ensure GPU is visible (optional but recommended):
   - `nvidia-smi`

## Run Flow During Viva

1. Open `06_demo/Demo.ipynb`.
2. Run cells in order from top to bottom.
3. The notebook will:
   - install missing Python dependencies,
   - import required libraries,
   - load base model + adapter from `06_demo/Models`,
   - read prompts from `06_demo/sample_inputs.txt`,
   - run deterministic inference and print latency + answers.
4. Demo output includes:
   - latency per prompt,
   - generated token count,
   - numeric final answer extraction,
   - raw final answer text,
   - compact summary table.

## New Machine Portability

Yes, the demo can run with only the `06_demo` folder, with these assumptions:

1. Python is available.
2. Internet access is available for first-time base model download.
3. Hugging Face access is configured if required by environment policy.

After first successful run, the base model is stored in `06_demo/Models` and later runs are local.

## Time Budget Guidance

- Keep `max_new_tokens` around `64-96` (already set near this range).
- Use first 3-5 prompts from `sample_inputs.txt` (already capped in notebook).
- Expected runtime on a ready GPU environment: about 3-5 minutes.

## If Something Fails

- Missing package: rerun the install cell.
- Model path error: verify the two `Models/` entries listed above.
- Slow generation: reduce `max_new_tokens` to `48` in the final code cell.
