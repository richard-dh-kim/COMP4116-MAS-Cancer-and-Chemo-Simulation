import numpy as np
import scipy.signal
import config

# Kernel for Moore Neighborhood (8 neighbors)
KERNEL = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])

def get_neighbor_counts(grid):
    # Create binary masks for each type
    h_mask = (grid == 1).astype(int)
    s_mask = (grid == 2).astype(int)
    r_mask = (grid == 3).astype(int)
    
    # Convolve to count neighbors
    h_count = scipy.signal.convolve2d(h_mask, KERNEL, mode='same', boundary='wrap')
    s_count = scipy.signal.convolve2d(s_mask, KERNEL, mode='same', boundary='wrap')
    r_count = scipy.signal.convolve2d(r_mask, KERNEL, mode='same', boundary='wrap')
    
    return h_count, s_count, r_count

def calculate_fitness_grid(grid, drug_conc):
    h_n, s_n, r_n = get_neighbor_counts(grid)
    total_neighbors = h_n + s_n + r_n
    total_neighbors[total_neighbors == 0] = 1 
    
    prop_h = h_n / total_neighbors
    prop_s = s_n / total_neighbors
    prop_r = r_n / total_neighbors
    
    # Calculate Base Payoff (Ax)
    payoff_h = (prop_h * config.PAYOFF_MATRIX[0,0] + 
                prop_s * config.PAYOFF_MATRIX[0,1] + 
                prop_r * config.PAYOFF_MATRIX[0,2])
                
    payoff_s = (prop_h * config.PAYOFF_MATRIX[1,0] + 
                prop_s * config.PAYOFF_MATRIX[1,1] + 
                prop_r * config.PAYOFF_MATRIX[1,2])
                
    payoff_r = (prop_h * config.PAYOFF_MATRIX[2,0] + 
                prop_s * config.PAYOFF_MATRIX[2,1] + 
                prop_r * config.PAYOFF_MATRIX[2,2])
    
    w = config.W0
    
    fit_h = 1 - w + w * payoff_h
    fit_s = (1 - w + w * payoff_s) - (drug_conc * config.DRUG_KILL_POWER)
    fit_r = 1 - w + w * payoff_r
    
    fitness_grid = np.zeros_like(grid, dtype=float)
    fitness_grid[grid == 1] = fit_h[grid == 1]
    fitness_grid[grid == 2] = fit_s[grid == 2]
    fitness_grid[grid == 3] = fit_r[grid == 3]
    
    return np.maximum(fitness_grid, 0.0)