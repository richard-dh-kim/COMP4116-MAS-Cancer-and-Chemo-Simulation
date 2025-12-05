import numpy as np

# ==========================================
# SPATIAL SIMULATION CONFIGURATION
# ==========================================

# 1. THE PAYOFF MATRIX (A)
# Rows: Healthy (1), Sensitive (2), Resistant (3)
# Cols: Empty(0), Healthy(1), Sensitive(2), Resistant(3)
# PAYOFF_MATRIX = np.array([
#     # H     S     R
#     [2.0, 1.5, 1.5],  # Healthy (Strong defense: 2.8)
#     [4.0, 2.0, 2.8],  # Sensitive (Dominant: 4.0 > 2.8) -> Invades Healthy
#     [2.5, 1.0, 2.0]   # Resistant (Weak: 2.5 < 2.8) -> Cannot invade Healthy alone
# ])

PAYOFF_MATRIX = np.array([
    [3.0, 1.5, 1.5],  # Healthy Row
    [4.0, 2.0, 2.8],  # Sensitive Row
    [3.0, 1.0, 2.0]   # Resistant Row
])

# 2. BIOLOGICAL CONSTANTS
W0 = 0.5
DRUG_KILL_POWER = 0.8
TOX_LIMIT = 400.0

# 3. SPATIAL SETTINGS
GRID_SIZE = 50         
NATURAL_DEATH_RATE = 0.05

# 4. TIME SETTINGS
TIME_STEPS = 5000       
DT = 1.0               

# 5. VISUALIZATION
SNAPSHOT_INTERVAL = 100 # Fallback interval