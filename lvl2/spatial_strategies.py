import numpy as np
import config

def get_population_counts(grid):
    unique, counts = np.unique(grid, return_counts=True)
    counts_dict = dict(zip(unique, counts))
    
    n_h = counts_dict.get(1, 0)
    n_s = counts_dict.get(2, 0)
    n_r = counts_dict.get(3, 0)
    
    total_cells = n_h + n_s + n_r
    if total_cells == 0: return 0, 0, 0
    
    tumor_size = (n_s + n_r) / (config.GRID_SIZE**2) 
    return tumor_size, n_s, n_r

# POLICY A: MTD
def mtd_policy(grid, step, state):
    return 1.0

# POLICY B: METRONOMIC
def metronomic_policy(grid, step, state):
    return 0.4

# POLICY C: ADAPTIVE (NASH)
def adaptive_policy(grid, step, state):
    tumor_size, _, _ = get_population_counts(grid)
    
    if 'baseline' not in state:
        state['baseline'] = max(tumor_size, 0.01)
        state['treating'] = True
        
    if state['treating']:
        if tumor_size < 0.65 * state['baseline']:
            state['treating'] = False
            return 0.0
        return 1.0
    else:
        if tumor_size > 0.9 * state['baseline']:
            state['treating'] = True
            return 1.0
        return 0.0

# POLICY D: STACKELBERG PROBE (SMART & ROBUST)
def stackelberg_policy(grid, step, state):
    tumor_size, _, _ = get_population_counts(grid)
    
    # Initialize State
    if 'phase' not in state:
        state['phase'] = 'PROBE'
        state['timer'] = 0
        state['last_size'] = tumor_size
        state['estimated_resistance'] = 'UNKNOWN' 

    # 1. PROBE PHASE (Test the tumor)
    if state['phase'] == 'PROBE':
        state['timer'] += 1
        if state['timer'] > 5:
            # End of probe: Measure response RELATIVELY
            if state['last_size'] > 0:
                # Calculate percentage drop (e.g., 0.05 = 5% shrinkage)
                relative_response = (state['last_size'] - tumor_size) / state['last_size']
            else:
                relative_response = 0.0
            
            # INFERENCE LOGIC:
            # If tumor shrank by > 5%, it's mostly Sensitive.
            # If it shrank < 5% (or grew), it's Resistant.
            if relative_response > 0.05: 
                state['estimated_resistance'] = 'LOW'
                state['phase'] = 'CONTROL' # We can treat safely
            else:
                state['estimated_resistance'] = 'HIGH'
                state['phase'] = 'HOLIDAY' # Danger! Stop treating.
                
            state['timer'] = 0
            state['last_size'] = tumor_size
            return 0.0 # Stop probe
        return 0.7 # Probe Dose

    # 2. CONTROL PHASE (Maintain stability)
    elif state['phase'] == 'CONTROL':
        # If tumor grows too big, tap it down
        # If it gets too small, stop (to keep S alive)
        if tumor_size > 0.30: return 0.8
        if tumor_size < 0.20: return 0.0
        
        # Periodically re-probe to check if resistance evolved
        state['timer'] += 1
        if state['timer'] > 50:
            state['phase'] = 'PROBE'
            state['timer'] = 0
            state['last_size'] = tumor_size
        return 0.0

    # 3. HOLIDAY PHASE (Competitive Release)
    elif state['phase'] == 'HOLIDAY':
        # We inferred resistance is High. Stop drugs to let S regrow.
        state['timer'] += 1
        
        # Wait a long time (e.g., 40 steps) then re-probe to see if S is back
        if state['timer'] > 40:
            state['phase'] = 'PROBE'
            state['timer'] = 0
            state['last_size'] = tumor_size
        return 0.0
        
    return 0.0