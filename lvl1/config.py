import numpy as np

# ==========================================
# SIMULATION CONFIGURATION
# ==========================================

# 1. THE PAYOFF MATRIX (A)
# Source: Li et al. (2025), Table 1 
# Rows = Cell Type Receiving Payoff (H, S, R)
# Cols = Cell Type Interaction Partner (H, S, R)
# Values:
# H vs H (a=2.9), H vs S (b=1.5), H vs R (d=1.5)
# S vs H (e=4.0), S vs S (g=2.0), S vs R (h=2.8)
# R vs H (k=3.0), R vs S (l=1.0), R vs R (o=2.2)

PAYOFF_MATRIX = np.array([
    [2.5, 1.5, 1.5],  # Healthy Row
    [4.0, 2.0, 2.8],  # Sensitive Row
    [3.0, 1.0, 2.0]   # Resistant Row
])

# CRITICAL CHECK:
# S vs H (4.0) > R vs H (3.7) -> S grows faster than R initially.
# S vs R (2.8) > R vs S (2.2) -> S beats R in direct competition.
# This ensures "Cost of Resistance" is active.

# 2. BIOLOGICAL CONSTANTS
W0 = 0.5                # Selection pressure intensity (Scale 0.0-1.0)
DRUG_KILL_POWER = 2.5   # How strictly the drug reduces Sensitive fitness
INITIAL_POP = [0.6, 0.38, 0.02] # [Healthy, Sensitive, Resistant] - 1% Resistance start

# 3. TIME SETTINGS
TIME_STEPS = 200        # How long to run the simulation
DT = 0.1                # Step size