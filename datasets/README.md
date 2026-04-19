# Datasets for Diluted Steganography Research

This document describes datasets relevant to studying steganographic capabilities and signal dilution in LLMs. Small samples (5 examples each) are provided in `samples/`.

---

## 1. GSM8K (Grade School Math 8K)

- **Used in:** NEST paper (Karpov 2026), steganographic reasoning evaluations
- **Description:** 8,500 grade school math word problems requiring multi-step reasoning. Models must show chain-of-thought to reach a numeric answer. Used to test whether models can perform steganographic encoded reasoning while solving math.
- **Size:** 7,473 train / 1,319 test examples
- **Format:** JSONL with `question` and `answer` fields (answer contains step-by-step solution ending with `#### <numeric_answer>`)
- **Sample:** `samples/gsm8k_sample.jsonl`

### Download instructions
```python
from datasets import load_dataset
ds = load_dataset("openai/gsm8k", "main")
# ds["train"], ds["test"]
```

Or via CLI:
```bash
huggingface-cli download openai/gsm8k --repo-type dataset
```

---

## 2. AQuA-RAT (Algebra Question Answering with Rationales)

- **Used in:** Early Signs paper (Zolkowski et al.), Text-Steganography-Benchmark (Redwood Research)
- **Description:** Algebraic word problems with multiple-choice answers and human-written rationales. Used as cover tasks where models must answer math questions while also encoding hidden messages.
- **Size:** 97,467 train / 254 test examples
- **Format:** JSONL with `question`, `options` (list of A-E choices), `rationale`, and `correct` fields
- **Sample:** `samples/aqua_rat_sample.jsonl`
- **Also available locally:** `../code/steganographic-evals/datasets/encoded_reasoning/aqua_rat.json`

### Download instructions
```python
from datasets import load_dataset
ds = load_dataset("deepmind/aqua_rat", "raw")
# ds["train"], ds["test"], ds["validation"]
```

---

## 3. Anthropic HH-RLHF (Helpful and Harmless)

- **Used in:** Early Signs paper (cover tasks), steganographic message passing experiments
- **Description:** Human preference data for helpfulness and harmlessness. Contains pairs of model responses (chosen/rejected) to conversational prompts. The "helpful" subset is used as cover tasks -- models must provide helpful answers while encoding hidden information.
- **Size:** ~170k examples total (train + test)
- **Format:** JSONL with `chosen` and `rejected` fields (each a multi-turn conversation string)
- **Sample:** `samples/hh_rlhf_sample.jsonl`
- **Also available locally:** `../code/steganographic-evals/datasets/encoded_reasoning/anthropic_cover_tasks_1000.jsonl` (1000 pre-selected helpful prompts)

### Download instructions
```python
from datasets import load_dataset
# Full dataset (helpful + harmless)
ds = load_dataset("Anthropic/hh-rlhf")

# Helpful subset only
ds = load_dataset("Anthropic/hh-rlhf", data_dir="helpful-base")
```

---

## 4. GPQA-Diamond

- **Used in:** Early Signs paper (encoded reasoning experiments)
- **Description:** Graduate-level science questions (physics, chemistry, biology) in multiple-choice format. Designed to be challenging even for domain experts. Used to test encoded reasoning on harder tasks.
- **Size:** 198 questions (Diamond subset)
- **Format:** CSV with question, choices, and correct answer
- **Available locally:** `../code/steganographic-evals/datasets/encoded_reasoning/gpqa_diamond.csv`

### Download instructions
```python
from datasets import load_dataset
ds = load_dataset("Idavidrein/gpqa", "gpqa_diamond")
```

---

## 5. State-Tracking Datasets (Custom)

- **Used in:** Early Signs paper (encoded reasoning)
- **Description:** Custom-generated datasets for evaluating state-tracking abilities. Include 1D maze (track direction after sequence of moves) and 2D maze tasks. Used to test whether models can perform steganographic encoded reasoning on simpler, more structured tasks.
- **Available locally:**
  - `../code/steganographic-evals/datasets/encoded_reasoning/state_tracking_1d.json`
  - `../code/steganographic-evals/datasets/encoded_reasoning/state_tracking_2d.json`
- **Generation:** Use `../code/steganographic-evals/generate_data.ipynb`

---

## 6. NARCBench Activation Data

- **Used in:** NARCBench (Rose et al. 2026)
- **Description:** Pre-extracted neural activation data from multi-agent deliberation scenarios. Three tiers: Core (committee deliberation), Transfer (novel scenarios), Stego (steganographic card counting).
- **Size:** ~2.6 GB
- **Format:** Numpy arrays + JSON metadata

### Download instructions
```bash
huggingface-cli download aaronrose227/narcbench --repo-type dataset --local-dir data
```

---

## 7. Alpaca Dataset

- **Used in:** Text-Steganography-Benchmark (Redwood Research)
- **Description:** Instruction-following dataset. Used as cover tasks in steganography defense evaluation.
- **Size:** 52k instruction-response pairs

### Download instructions
```python
from datasets import load_dataset
ds = load_dataset("tatsu-lab/alpaca")
```

---

## 8. NEST Paper Datasets (Not Publicly Released)

- **Used in:** NEST (Karpov 2026, arxiv 2602.14095)
- **Description:** The NEST paper evaluates across 4 task types:
  1. GSM8K math problems (see above)
  2. Maze navigation tasks
  3. Counting tasks (where Claude Opus 4.5 achieved 92% accuracy at D=4)
  4. Message encoding tasks
- **Note:** The full evaluation datasets and scripts for the 28-model evaluation are not publicly released. GSM8K is available (see above). Maze and counting task generators would need to be reimplemented.

---

## Sample Files

The `samples/` directory contains 5-example JSONL files for quick inspection:

| File | Dataset | Fields |
|------|---------|--------|
| `gsm8k_sample.jsonl` | GSM8K test | `question`, `answer` |
| `aqua_rat_sample.jsonl` | AQuA-RAT test | `question`, `options`, `rationale`, `correct` |
| `hh_rlhf_sample.jsonl` | HH-RLHF test | `chosen`, `rejected` |

These are for reference only -- do not use for actual experiments. Load the full datasets using the instructions above.
