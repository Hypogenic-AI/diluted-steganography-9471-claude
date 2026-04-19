"""Resume experiments from Experiment 2 onwards (Experiment 1 already complete)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from run_experiments import run_experiment_2_informed_extraction, run_experiment_3_blind_detection
from llm_api import get_usage_summary

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")

print("Resuming from Experiment 2...")
r2 = run_experiment_2_informed_extraction()
r3 = run_experiment_3_blind_detection()

usage = get_usage_summary()
print("\n" + "="*70)
print("API USAGE SUMMARY")
print("="*70)
print(json.dumps(usage, indent=2))

with open(os.path.join(RESULTS_DIR, "api_usage.json"), "w") as f:
    json.dump(usage, f, indent=2)

print("\nAll experiments complete!")
