# Diluted Steganography

Systematic study of how signal dilution affects LLM steganographic capabilities across encoding, extraction, and detection tasks.

## Key Findings

- **Cliff effect**: All three frontier models (GPT-4.1, Claude Sonnet 4.5, Gemini 2.5 Pro) achieve 92-100% accuracy on acrostic steganography but collapse to 0-43% on any diluted encoding scheme (every Nth word, trigger-word-based). The transition is abrupt, not gradual.
- **Acrostics are memorized, not generalized**: The near-perfect acrostic performance reflects pattern memorization from training data, not a composable steganographic capability.
- **Extraction > Encoding**: GPT-4.1 retains 35-55% partial extraction accuracy on diluted schemes (vs 23-31% encoding accuracy), suggesting extraction is easier than generation.
- **Blind detection is non-functional**: GPT-4.1 and Gemini flag everything as steganographic (100% FP rate); Claude flags nothing (0% TP rate). No model can discriminate stego from non-stego text.
- **AI safety implication**: Current LLM-based monitoring cannot detect diluted steganography, but models also cannot reliably produce it.

## Encoding Schemes Tested

| Scheme | Dilution Level | Description |
|--------|---------------|-------------|
| Acrostic | Low (~1 char/sentence) | First letter of each sentence |
| Every 3rd word | Medium | First letter of every 3rd word |
| Every 5th word | Medium-high | First letter of every 5th word |
| Trigger word | High (~1 char/8 words) | Word after each "the" |
| Every 10th word | Very high | First letter of every 10th word |
| Every 20th word | Extreme | First letter of every 20th word |

## Reproduce

```bash
# Setup
uv venv && source .venv/bin/activate
uv add openai httpx numpy matplotlib seaborn scipy

# Set API keys
export OPENAI_API_KEY="..."
export OPENROUTER_KEY="..."

# Run experiments (~15 min with API calls)
python src/run_experiments.py

# Generate analysis and figures
python src/analyze_results.py
```

## Project Structure

```
.
├── REPORT.md               # Full research report with results
├── README.md               # This file
├── planning.md             # Experimental design and motivation
├── src/
│   ├── stego_schemes.py    # Encoding scheme implementations
│   ├── llm_api.py          # LLM API calling infrastructure
│   ├── run_experiments.py  # Main experiment runner
│   └── analyze_results.py  # Analysis and visualization
├── results/                # Raw experimental results (JSON)
├── figures/                # Generated plots
├── literature_review.md    # Pre-gathered literature review
├── resources.md            # Resource catalog
├── papers/                 # Downloaded research papers
└── code/                   # Cloned baseline repositories
```

## Full Report

See [REPORT.md](REPORT.md) for complete methodology, results tables, statistical tests, and discussion.
