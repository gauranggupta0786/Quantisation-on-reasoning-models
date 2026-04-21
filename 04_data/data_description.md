# Data Description

## Datasets Used

1. openai/gsm8k (main)
- Type: Grade-school math word problems.
- Typical target: A final numeric answer.

2. Idavidrein/gpqa (gpqa_diamond)
- Type: Graduate-level multiple-choice science reasoning.
- Typical target: Option selection (A/B/C/D) with reasoning.

## Splits Used in This Notebook

### GSM8K
- Training split: gsm8k[train]
- Evaluation split: gsm8k[test]

### GPQA
- Training split: gpqa[train]
- Evaluation split: gpqa[train] subset
- Note: In this workflow, GPQA train is used for evaluation subsets as well (practical course setup), not a separate official test split.

## Preprocessing Pipeline

1. Rows are mapped into a unified reasoning format with fields like:
- prompt
- ground_truth
- dataset_name

2. Prompts are rewritten to enforce reasoning structure:
- model is instructed to reason inside <think> ... </think>
- then provide a final answer after the reasoning block

3. Original raw columns are dropped after mapping (remove_columns) so downstream training/evaluation uses standardized fields.

4. For GPQA, options/order handling is stabilized via deterministic seeding logic in the notebook.

## Subset / Reduced Setup Used

The notebook uses reduced subsets to keep experiments practical.

### Phase 8 caps (current)
- PHASE8_TRAIN_LIMIT_GSM8K = 2000
- PHASE8_TRAIN_LIMIT_GPQA = 200
- PHASE8_EVAL_LIMIT_GSM8K = 20
- PHASE8_EVAL_LIMIT_GPQA = 20

### Phase 8 RL pilot subset
- phase8_train_dataset_pilot: 30 samples (GSM8K-only) for faster GRPO iteration.

### Earlier quick checks in notebook
- Several intermediate phases run 30-sample evaluations for speed and debugging.

## Why These Reductions Were Used

1. To fit GPU memory and runtime constraints.
2. To enable rapid iteration during quantization and adaptation studies.
3. To support live demonstration cells that finish in a few minutes.
