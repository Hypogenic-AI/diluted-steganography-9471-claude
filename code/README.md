# Cloned Repositories for Diluted Steganography Research

This directory contains cloned repositories relevant to studying steganographic capabilities in LLMs, with a focus on signal dilution, encoding schemes, and evaluation frameworks.

---

## 1. steganographic-evals (Early Signs paper)

- **Source:** https://github.com/arturzolkowski/steganographic-evals
- **Paper:** "Early Signs of Steganographic Capabilities in Frontier LLMs" (Zolkowski et al., arxiv 2507.02737)
- **Description:** Evaluates two types of steganography in frontier LLMs: (1) passing encoded messages and (2) performing encoded reasoning. Tests whether current models can embed hidden information in outputs without a monitor noticing.

### Encoding schemes implemented
- Acrostics (first-letter encoding)
- Hexadecimal encoding
- Custom encoding schemes (model-defined)
- State-tracking encoded reasoning (1D/2D mazes)
- Encoded message passing with cover tasks

### Datasets included
- `datasets/encoded_reasoning/aqua_rat.json` -- AQuA-RAT algebraic word problems
- `datasets/encoded_reasoning/gpqa_diamond.csv` -- GPQA-Diamond challenging MCQ
- `datasets/encoded_reasoning/anthropic_cover_tasks_1000.jsonl` -- Anthropic Helpful cover tasks
- `datasets/encoded_reasoning/state_tracking_1d.json` -- 1D maze state tracking
- `datasets/encoded_reasoning/state_tracking_2d.json` -- 2D maze state tracking

### Key entry points
- `stego_benchmark/main.py` -- Run single experiment with config
- `stego_benchmark/run_message_passing_experiments.py` -- All message passing experiments
- `stego_benchmark/run_encoded_reasoning_experiments.py` -- All encoded reasoning experiments
- `stego_benchmark/run_steering_experiments.py` -- Steering experiments
- `stego_benchmark/encoding_methods.py` -- Encoding scheme implementations

---

## 2. Text-Steganography-Benchmark (Redwood Research)

- **Source:** https://github.com/redwoodresearch/Text-Steganography-Benchmark
- **Paper:** "Preventing Language Models From Hiding Their Reasoning" (Roger et al., arxiv 2310.18512)
- **Description:** Evaluates defenses (paraphrasers) against LLM steganography schemes. Includes fine-tuning steganography demos and a framework for attack/defense evaluation.

### Encoding schemes implemented (attackers)
- `aqua_attackers.py` -- AQuA-specific steganography attacks
- `arithmetic_coding_attackers.py` -- Arithmetic coding based stego
- `instruction_attackers.py` -- Instruction-following based encoding
- `scratchpad_attackers.py` -- Scratchpad-based hidden reasoning
- `simple_attackers.py` -- Simple encoding baselines
- `codable_wm/` -- Codable watermarking
- `wm/` -- Watermarking methods

### Datasets
- `textsteg/datasets/aqua.py` -- AQuA-RAT dataset loader
- `textsteg/datasets/code_problems.py` -- Code problem datasets
- `textsteg/datasets/instructions.py` -- Instruction-following datasets
- `textsteg/datasets/simple_qa.py` -- Simple QA datasets

### Key entry points
- `textsteg/main.py` -- Main evaluation pipeline (attacker vs defender)
- `textsteg/exploration/ft_experiments.py` -- Fine-tuning steganography demo
- `textsteg/exploration/sweep_aqua.py` -- AQuA experiment sweep
- `textsteg/exploration/sweep_alpaca.py` -- Alpaca experiment sweep
- `textsteg/interface.py` -- Core interfaces (Attacker, Defender, Dataset, Evaluator)

---

## 3. narcbench (Hidden in Plain Text / Multi-Agent Collusion)

- **Source:** https://github.com/aaronrose227/narcbench
- **Paper:** "Detecting Multi-Agent Collusion Through Multi-Agent Interpretability" (Rose et al., 2026, arxiv 2604.01151). Related to "Hidden in Plain Text" (Mathew et al., 2024, arxiv 2410.03768) -- same research group (Christian Schroeder de Witt).
- **Description:** Three-tier benchmark (Core, Transfer, Stego) for evaluating multi-agent collusion detection. Trains deception probes on committee-deliberation activations and evaluates on steganographic signalling.

### Encoding schemes
- Steganographic card-counting signalling (NARCBench-Stego tier)
- Multi-agent deliberation collusion patterns

### Datasets
- HuggingFace: `aaronrose227/narcbench` (~2.6GB activation data)
- Committee deliberation scenarios (Core tier)
- Structurally distinct transfer scenarios (Transfer tier)

### Key entry points
- `reproduce.py` -- Reproduces Table 1 and Figure 2
- `generation/core.py` -- Core scenario generation
- `generation/stego.py` -- Stego scenario generation
- `extraction/extract_stego.py` -- Stego activation extraction

---

## 4. arithmetic-coding-steganography (NEST paper companion)

- **Source:** https://github.com/artkpv/arithmetic-coding-steganography
- **Paper:** Companion tool for "NEST: Nascent Encoded Steganographic Thoughts" (Karpov, 2026, arxiv 2602.14095)
- **Description:** Arithmetic coding steganography library that hides secret messages within LLM-generated text by influencing token selection based on probability distributions.

### Encoding schemes implemented
- Arithmetic coding steganography (core method)
- Token probability-based interval division
- ETX EOF marker encoding

### Datasets
- No bundled datasets (tool-focused, not benchmark-focused)
- NEST paper itself uses GSM8K, maze tasks, counting tasks across 28 models

### Key entry points
- Python API: `from stego_arith_coding import ArithmeticSteganography`
- CLI: `stego-arith encode`, `stego-arith decode`
- `tests/test_core.py` -- Core functionality tests

---

## 5. LLM-Steganography

- **Source:** https://github.com/HighDoping/LLM-Steganography
- **Description:** Practical steganography tool using LLMs to hide information in text. Supports both API mode (OpenAI-compatible) and native mode (HuggingFace Transformers).

### Encoding schemes implemented
- Character-level steganographic encoding using LLM token selection
- Configurable number base (2, 4, 8, 16, 32, 64, 85)
- Optional password-based encryption layer

### Datasets
- No bundled datasets (tool-focused)

### Key entry points
- `python -m llm_steganography encode` -- Encode hidden text
- `python -m llm_steganography decode` -- Decode hidden text

---

## Repos Not Found (No Public Code Available)

### Secret Collusion (Motwani et al., NeurIPS 2024)
- **Paper:** "Secret Collusion among AI Agents: Multi-Agent Deception via Steganography" (arxiv 2402.07510)
- **CASE Framework:** Described in paper but no public GitHub repository found
- **Relevance:** Formalizes secret collusion threat model; evaluates component abilities for steganography (self-sampling, symmetric key encryption, logit simulation, one-time pads)

### Hidden in Plain Text (Mathew et al., 2024)
- **Paper:** arxiv 2410.03768
- **Note:** No standalone repo found. The narcbench repo above is from the same research group. The paper describes GBRL and ICRL methods for eliciting steganographic collusion.

### NEST Full Evaluation Code (Karpov, 2026)
- **Paper:** arxiv 2602.14095
- **Note:** Only the arithmetic-coding tool repo was found. The full evaluation code testing 28 models across GSM8K/maze/counting tasks does not appear to be publicly released.

### The Steganographic Potentials of Language Models (Karpov et al., ICLR 2025 Workshop)
- **Paper:** arxiv 2505.03439
- **Note:** No public repo found. Studies RL-finetuned LLMs developing covert encoding schemes.
