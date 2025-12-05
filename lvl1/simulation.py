import numpy as np
import dynamics
import config

def run(policy_func):
    # Setup Time
    time_points = np.arange(0, config.TIME_STEPS, config.DT)
    
    # Setup State
    x = np.array(config.INITIAL_POP)
    history_x = [x]
    history_drug = [0.0]
    history_tox = [0.0]
    
    # Policy Memory (State Dictionary)
    policy_state = {}
    current_toxicity = 0.0
    
    # Integration Loop (Manual Euler/RK1 for transparency with stateful policies)
    for t in time_points[1:]:
        
        # 1. Get Drug Decision
        drug = policy_func(t, x, policy_state)

        # 2. Accumulate Toxicity
        current_toxicity += drug * config.DT
        
        # 3. Calculate Gradient (dx/dt)
        # Using RK4 for stability
        k1 = dynamics.replicator_dynamics(x, t, drug)
        k2 = dynamics.replicator_dynamics(x + 0.5*config.DT*k1, t, drug)
        k3 = dynamics.replicator_dynamics(x + 0.5*config.DT*k2, t, drug)
        k4 = dynamics.replicator_dynamics(x + config.DT*k3, t, drug)
        
        # 3. Update Population
        x = x + (config.DT / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        
        # 4. Normalize (Ensure sum = 1.0 to prevent drift)
        x = np.maximum(x, 0) # No negative populations
        x = x / np.sum(x)
        
        # Save
        history_x.append(x)
        history_drug.append(drug)
        history_tox.append(current_toxicity)
        
    return time_points, np.array(history_x), np.array(history_drug), np.array(history_tox)