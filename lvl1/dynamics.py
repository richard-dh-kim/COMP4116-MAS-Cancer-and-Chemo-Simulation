import numpy as np
import config

def calculate_fitness(x, drug_conc):
    """
    Calculates fitness vector f according to Li et al. Eq 2.
    f_i = 1 - w_i + w_i * (Ax)_i
    """
    # 1. Base Game Payoff (Ax)
    # The matrix multiplication represents the average payoff from interactions
    payoff = np.dot(config.PAYOFF_MATRIX, x)
    
    # 2. Selection Pressure (w)
    # In the absence of drug, w = W0 for everyone.
    # Drug reduces the fitness of Sensitive cells (S).
    w_base = config.W0
    
    # Calculate raw fitness for each type
    # Healthy (Index 0)
    f_h = 1 - w_base + w_base * payoff[0]
    
    # Sensitive (Index 1) - Affected by Drug
    # We model drug as a direct reduction in the fitness outcome
    drug_penalty = drug_conc * config.DRUG_KILL_POWER
    f_s = (1 - w_base + w_base * payoff[1]) - drug_penalty
    
    # Resistant (Index 2) - Unaffected by Drug
    f_r = 1 - w_base + w_base * payoff[2]
    
    # Ensure fitness doesn't go negative (biology breaks if fitness < 0)
    return np.maximum([f_h, f_s, f_r], 0.0)

def replicator_dynamics(x, t, drug_conc):
    """
    The Differential Equation: dx_i/dt = x_i * (f_i - average_f)
    Li et al. Eq 1.
    """
    f = calculate_fitness(x, drug_conc)
    avg_fitness = np.dot(x, f)
    
    # Change in population
    dxdt = x * (f - avg_fitness)
    return dxdt