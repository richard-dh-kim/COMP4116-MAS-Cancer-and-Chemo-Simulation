import numpy as np
import spatial_dynamics
import config

def initialize_natural_tumor():
    """
    Robust Tumor Generator.
    Ensures a valid tumor is created by retrying if stochastic extinction occurs.
    """
    
    while True: # RETRY LOOP: Keep trying until we get a non-zero tumor
        # print("Attempting to grow tumor...") # Optional debug print
        
        # 1. Start with all Healthy
        grid = np.ones((config.GRID_SIZE, config.GRID_SIZE), dtype=int)
        
        # 2. Seed a 3x3 BLOCK of Sensitive Cells (Protects against instant death)
        mid = config.GRID_SIZE // 2
        grid[mid-1:mid+2, mid-1:mid+2] = 2
        
        # Target size (20% of grid)
        target_size = (config.GRID_SIZE**2) * 0.20
        mutation_rate = 0.05 
        
        # Growth Loop
        for i in range(2000): 
            # No Drug
            fitness_map = spatial_dynamics.calculate_fitness_grid(grid, 0.0)
            
            # Death
            death_mask = np.random.random(grid.shape) < config.NATURAL_DEATH_RATE
            death_mask[grid == 0] = False
            grid[death_mask] = 0
            
            # Reproduction
            empty_x, empty_y = np.where(grid == 0)
            if len(empty_x) > 0:
                indices = np.arange(len(empty_x))
                np.random.shuffle(indices)
                
                for k in indices:
                    x, y = empty_x[k], empty_y[k]
                    neighbors = []
                    fits = []
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx==0 and dy==0: continue
                            nx, ny = (x+dx)%config.GRID_SIZE, (y+dy)%config.GRID_SIZE
                            nt = grid[nx, ny]
                            if nt != 0:
                                neighbors.append(nt)
                                fits.append(fitness_map[nx, ny])
                    
                    if not neighbors: continue
                    fits = np.array(fits)
                    if np.sum(fits) == 0: continue
                    winner = np.random.choice(neighbors, p=fits/np.sum(fits))
                    
                    # Mutation
                    if winner == 2 and np.random.random() < mutation_rate:
                        winner = 3 
                    grid[x, y] = winner
            
            # Check Size
            current_size = np.sum(grid > 1)
            if current_size >= target_size:
                break
        
        # Validation: Did the tumor survive?
        final_size = np.sum(grid > 1)
        if final_size > 50: # Ensure we have a decent sized tumor
            print(f"Tumor generated successfully. Size: {final_size} cells.")
            return grid
        else:
            # If failed/died out, the loop restarts automatically
            pass

def step(grid, drug_conc):
    # Standard Step (Same as before)
    fitness_map = spatial_dynamics.calculate_fitness_grid(grid, drug_conc)
    
    death_probs = np.full(grid.shape, config.NATURAL_DEATH_RATE)
    if drug_conc > 0:
        death_probs[grid == 2] += (drug_conc * 0.15) 
        
    random_roll = np.random.random(grid.shape)
    kill_mask = random_roll < death_probs
    kill_mask[grid == 0] = False
    grid[kill_mask] = 0
    
    empty_x, empty_y = np.where(grid == 0)
    if len(empty_x) > 0:
        indices = np.arange(len(empty_x))
        np.random.shuffle(indices)
        for i in indices:
            x, y = empty_x[i], empty_y[i]
            neighbors = []
            fits = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx==0 and dy==0: continue
                    nx, ny = (x+dx)%config.GRID_SIZE, (y+dy)%config.GRID_SIZE
                    nt = grid[nx, ny]
                    if nt != 0:
                        neighbors.append(nt)
                        fits.append(fitness_map[nx, ny])
            if not neighbors: continue
            fits = np.array(fits)
            if np.sum(fits) == 0: continue
            winner = np.random.choice(neighbors, p=fits/np.sum(fits))
            grid[x, y] = winner
            
    return grid

def run(policy_func):
    grid = initialize_natural_tumor()
    
    history_h, history_s, history_r = [], [], []
    history_drug, history_tox = [], []
    
    policy_state = {}
    total_tox = 0.0
    
    snapshots = []
    
    # Dynamic snapshot times
    T = config.TIME_STEPS
    snapshot_times = [0, int(T*0.33), int(T*0.66), T-1]
    
    for t in range(config.TIME_STEPS):
        drug = policy_func(grid, t, policy_state)
        total_tox += drug

        if total_tox > config.TOX_LIMIT:
            print(f"Experiment Ended Early: Patient toxicity limit reached at step {t}")
            # Optional: Record that the patient died in the history
            # You can leave the history arrays as they are (shorter than TIME_STEPS)
            # or pad them. The plotting function usually handles shorter arrays fine.
            break
        
        grid = step(grid, drug)
        
        unique, counts = np.unique(grid, return_counts=True)
        counts_dict = dict(zip(unique, counts))
        total = config.GRID_SIZE**2
        
        history_h.append(counts_dict.get(1, 0) / total)
        history_s.append(counts_dict.get(2, 0) / total)
        history_r.append(counts_dict.get(3, 0) / total)
        history_drug.append(drug)
        history_tox.append(total_tox)
        
        if t in snapshot_times:
            snapshots.append(grid.copy())
            
    actual_steps = len(history_h)
    
    return {
        'time': np.arange(actual_steps),  # Fix: Dynamic time axis
        'h': history_h, 
        's': history_s, 
        'r': history_r,
        'drug': history_drug, 
        'tox': history_tox,
        'snapshots': snapshots,
        'snap_times': snapshot_times
    }