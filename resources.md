# Resources Catalog

## Summary
This document catalogs all resources gathered for the "Diluted Steganography" research project investigating how LLMs handle signal dilution in steganographic contexts. Resources include 14 downloaded papers, 8 documented datasets, and 5 cloned code repositories.

---

## Papers
Total papers downloaded: 14

| # | Title | Authors | Year | File | Key Info |
|---|-------|---------|------|------|----------|
| 1 | NEST: Nascent Encoded Steganographic Thoughts | Karpov | 2026 | papers/2602.14095_nest_stego_thoughts.pdf | Acrostic evaluation across 28 models, D-parameter dilution |
| 2 | Early Signs of Steganographic Capabilities | Zolkowski et al. | 2025 | papers/2507.02737_early_signs_stego_capabilities.pdf | sentence_letter vs third_word_letter comparison, open-source evals |
| 3 | Steganographic Potentials of Language Models | Karpov et al. | 2025 | papers/2505.03439_steganographic_potentials_lm.pdf | RL fine-tuning for stego, prompted evaluations |
| 4 | Preventing LMs From Hiding Reasoning | Roger, Greenblatt | 2023 | papers/2310.01405_preventing_hiding_reasoning.pdf | Paraphrasing defense, ~3 bits/KB limit |
| 5 | Secret Collusion among AI Agents | Motwani et al. | 2024 | papers/2402.07871_secret_collusion_ai_agents.pdf | Multi-agent collusion formalization |
| 6 | Hidden in Plain Text | Mathew et al. | 2024 | papers/2410.03054_hidden_plain_text.pdf | Steganographic collusion emergence via training |
| 7 | LLMs as Carriers of Hidden Messages | Hoscilowicz et al. | 2024 | papers/2406.02481_llm_carriers_hidden_messages.pdf | Hidden text via fine-tuning, extraction attacks |
| 8 | Generative Text Stego with LLM | Wu et al. | 2024 | papers/2404.10229_generative_text_stego_llm.pdf | LLM-Stega black-box method |
| 9 | Neural Linguistic Steganography | Ziegler et al. | 2019 | papers/1909.01496_neural_linguistic_stego.pdf | Foundational arithmetic coding approach |
| 10 | Undetectable Stego for Language Models | Christ et al. | 2023 | papers/2306.06078_undetectable_stego_lm.pdf | Cryptographic stego framework |
| 11 | Next-Gen Steganalysis with LLMs | Various | 2024 | papers/2405.09090_next_gen_steganalysis_llm.pdf | LLM-based detection methods |
| 12 | S2LM: Semantic Stego via LLMs | Wu et al. | 2025 | papers/2511.05319_s2lm_semantic_stego.pdf | Sentence-level semantic stego |
| 13 | TrojanStego | Meier et al. | 2025 | papers/trojanstego_2025.pdf | Vocabulary partitioning for stego exfiltration |
| 14 | Implicit Memory as Hidden Channel | Salem et al. | 2026 | papers/implicit_memory_2026.pdf | Temporal backdoors via implicit memory |

See papers/README.md for detailed descriptions.

---

## Datasets
Total datasets documented: 8

| # | Name | Source | Size | Task | Notes |
|---|------|--------|------|------|-------|
| 1 | GSM8K | HuggingFace openai/gsm8k | 8.5K | Math reasoning (hidden task) | Standard in NEST |
| 2 | AQuA-RAT | HuggingFace deepmind/aqua_rat | 97K | Algebraic problems (hidden task) | Used in Early Signs |
| 3 | Anthropic HH-RLHF | HuggingFace Anthropic/hh-rlhf | 170K | Cover questions | Standard cover task source |
| 4 | GPQA-Diamond | HuggingFace Idavidrein/gpqa | 198 | PhD-level science | Hard hidden task |
| 5 | State-Tracking (1D/2D) | Generated / steganographic-evals | Custom | State tracking | Simple encoded reasoning |
| 6 | NARCBench | HuggingFace aaronrose227/narcbench | 2.6GB | Multi-agent collusion | Activation data |
| 7 | Alpaca | HuggingFace tatsu-lab/alpaca | 52K | Cover tasks | Instruction-following |
| 8 | Custom Counting Tasks | Generate programmatically | Custom | Diluted steganography | Our novel contribution |

See datasets/README.md for download instructions. Sample files in datasets/samples/.

---

## Code Repositories
Total repositories cloned: 5

| # | Name | URL | Purpose | Location |
|---|------|-----|---------|----------|
| 1 | steganographic-evals | github.com/arturzolkowski/steganographic-evals | Early Signs evaluation suite | code/steganographic-evals/ |
| 2 | Text-Steganography-Benchmark | github.com/redwoodresearch/Text-Steganography-Benchmark | Attack/defense framework | code/Text-Steganography-Benchmark/ |
| 3 | narcbench | github.com/aaronrose227/NARCBench | Multi-agent collusion detection | code/narcbench/ |
| 4 | arithmetic-coding-steganography | github.com/artyomkarpov/arithmetic-coding-steganography | Arithmetic coding stego tool | code/arithmetic-coding-steganography/ |
| 5 | LLM-Steganography | github.com/jkranabetter/LLM-Steganography | Practical LLM stego tool | code/LLM-Steganography/ |

See code/README.md for detailed descriptions.

---

## Resource Gathering Notes

### Search Strategy
1. Used paper-finder service (111 results from Semantic Scholar)
2. Web searches for steganography + LLM + acrostic + signal dilution
3. ArXiv searches for specific paper IDs from citations
4. GitHub searches for implementations linked from papers

### Selection Criteria
- **Papers**: Prioritized work on LLM steganographic *capabilities* (not tools), especially those studying encoding pattern effects, acrostics, and signal density
- **Datasets**: Selected standard benchmarks used across multiple papers in this area
- **Code**: Focused on evaluation frameworks with reusable encoding scheme implementations

### Challenges Encountered
- NEST paper (Karpov 2026) code not publicly available - methodology must be reimplemented
- No existing work directly studies the full dilution spectrum (our gap to fill)
- The "Steganographic Potentials" paper code also not released
- Some repos (CASE framework from Motwani et al.) not publicly available

### Gaps and Workarounds
- No dataset specifically for diluted steganography exists -> will generate programmatically following NEST methodology
- No benchmark for trigger-word-based patterns -> will design custom evaluation
- Limited standardization of metrics across papers -> will use NEST's metrics (per-number accuracy, exact match, CER)

---

## Recommendations for Experiment Design

### 1. Primary Dataset(s)
- **Custom counting tasks** with dilution parameter (extending NEST methodology)
- **Anthropic HH-RLHF** for cover questions (standard in field)
- **GSM8K** for steganographic reasoning experiments (standard in field)

### 2. Baseline Methods
- **Acrostic (sentence_letter)**: Dense signal, D=4,8,16 (from NEST)
- **third_word_letter**: Slightly diluted (from Early Signs)
- **Every-Nth-sentence**: Our novel dilution gradient
- **Trigger-word-based**: Our novel encoding method
- **No encoding / plain CoT**: Control baselines

### 3. Evaluation Metrics
- Per-element accuracy (partial credit)
- Exact match rate
- Monitor evasion rate (GPT-4.1-mini at 1% FPR threshold)
- Combined success rate = correct AND undetected
- **Dilution-accuracy curve**: Plot accuracy as function of dilution factor (our key contribution)

### 4. Code to Adapt/Reuse
- **steganographic-evals** (Early Signs): Most directly useful - has encoding scheme implementations, monitor setup, and evaluation pipeline. Extend with diluted encoding schemes.
- **Text-Steganography-Benchmark** (Redwood): Useful for defense evaluation (paraphrasing).
- **NEST methodology**: Reimplement counting task with dilution parameter.

### 5. Models to Test
- Claude Opus 4.5, 4.1, 4 (highest acrostic capability per NEST)
- GPT-4.1, GPT-5.x (test safety training effects)
- Grok Code Fast (strong performer in NEST)
- At least one smaller model for scaling analysis
