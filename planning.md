# Research Plan: Diluted Steganography

## Motivation & Novelty Assessment

### Why This Research Matters
As LLMs become more capable, understanding their ability to encode and detect hidden messages in text is critical for AI safety. Current work (NEST, Early Signs) shows LLMs can handle acrostic-style steganography, but the key question is: what happens when the signal is diluted? If LLMs can't detect diluted steganographic patterns, this has implications for monitoring systems designed to catch covert communication between AI agents.

### Gap in Existing Work
Based on the literature review, NEST (2026) studied acrostics at varying sequence lengths and Early Signs (2025) compared `sentence_letter` vs `third_word_letter`, but:
- No systematic study varies dilution level as a continuous parameter
- Trigger-word-based encoding (word after each occurrence of a specific word) is untested
- The accuracy-detectability tradeoff as a function of dilution is uncharacterized
- No work tests LLM *extraction* ability across a dilution gradient

### Our Novel Contribution
We systematically measure how LLM performance degrades across a dilution gradient, testing both:
1. **Encoding**: Can LLMs produce text with diluted steganographic patterns?
2. **Extraction (informed)**: Can LLMs extract messages when told the encoding scheme?
3. **Detection (blind)**: Can LLMs detect hidden messages without knowing the scheme?
4. **Trigger-word encoding**: A novel, more naturalistic dilution method

### Experiment Justification
- **Experiment 1 (Encoding)**: Tests if LLMs can *produce* diluted steganography - fundamental capability
- **Experiment 2 (Informed Extraction)**: Tests if LLMs can *decode* when given the key - measures cognitive capacity for diluted patterns
- **Experiment 3 (Blind Detection)**: Tests real-world detectability - critical for AI safety monitoring

## Research Question
How does signal dilution in steganographic encoding affect LLMs' ability to (a) encode secret messages, (b) extract messages when the scheme is known, and (c) detect hidden messages without scheme knowledge?

## Hypothesis Decomposition
- **H1**: LLM encoding accuracy decreases monotonically as dilution increases
- **H2**: Informed extraction accuracy decreases with dilution but more slowly than encoding accuracy (extraction is easier than generation)
- **H3**: Blind detection rate drops sharply beyond a dilution threshold
- **H4**: Trigger-word-based encoding is harder for LLMs than positional encoding at equivalent dilution levels

## Proposed Methodology

### Encoding Schemes (ordered by increasing dilution)
1. **Acrostic**: First letter of each sentence encodes a character (baseline, concentrated)
2. **Every-3rd-word**: First letter of every 3rd word encodes a character
3. **Every-5th-word**: First letter of every 5th word
4. **Trigger-word**: Word following each occurrence of "the" starts with target letter
5. **Every-10th-word**: First letter of every 10th word
6. **Every-20th-word**: First letter of every 20th word (very diluted)

### Secret Messages
Short words: "HELLO", "SECRET", "DANGER", "ESCAPE", "FROST", "MAGIC"
(4-6 characters, using common initial letters)

### Models
- **GPT-4.1** (via OpenAI API) - strong frontier model
- **Claude Sonnet 4.5** (via OpenRouter) - strong frontier model
- **Gemini 2.5 Pro** (via OpenRouter) - strong frontier model

### Experimental Steps
1. **Programmatic text generation**: Create ground-truth texts with known hidden messages for each encoding scheme (for extraction/detection experiments)
2. **LLM encoding experiment**: Ask each model to encode messages using each scheme (20 trials per scheme × model)
3. **LLM informed extraction**: Give ground-truth texts + scheme description, ask model to extract (20 trials per scheme × model)
4. **LLM blind detection**: Give ground-truth texts without scheme info, ask if hidden message exists (20 trials per scheme × model)
5. Analysis and visualization

### Baselines
- Random chance extraction (1/26 per character ≈ 3.8%)
- Random chance detection (50% if binary yes/no)
- Acrostic performance as "concentrated" ceiling

### Evaluation Metrics
- **Per-character accuracy**: Fraction of correctly extracted characters
- **Exact match rate**: Full message correctly extracted
- **Detection rate**: True positive rate for hidden message detection
- **False positive rate**: Detection rate on texts without hidden messages

### Statistical Analysis Plan
- Bootstrap confidence intervals (95%) for all metrics
- Chi-square tests comparing accuracy across dilution levels
- Spearman rank correlation between dilution level and accuracy
- Effect sizes (Cohen's d) for pairwise comparisons

## Expected Outcomes
- Acrostic: High encoding/extraction accuracy (>80%), high detection rate
- Every-3rd-word: Moderate encoding (~50-70%), moderate extraction
- Trigger-word: Low encoding accuracy, low-moderate extraction
- Every-10th/20th-word: Very low encoding/extraction, near-chance detection
- Clear monotonic decrease in performance with dilution

## Timeline
- Phase 0-1 (Planning): 20 min ✓
- Phase 2 (Setup + Implementation): 60 min
- Phase 3-4 (Experiments): 90 min
- Phase 5 (Analysis + Documentation): 45 min

## Potential Challenges
- API rate limits → use retry with exponential backoff
- Models refusing steganography requests → frame as research/puzzle
- Programmatic text generation quality → use templates + validation
- Cost → limit to 20 trials per condition, use cheaper models for pilot

## Success Criteria
- Clear dilution-accuracy curve across at least 4 dilution levels
- Statistical significance for accuracy differences between concentrated vs diluted schemes
- Results from at least 2 frontier models
- Actionable insights for AI safety monitoring
