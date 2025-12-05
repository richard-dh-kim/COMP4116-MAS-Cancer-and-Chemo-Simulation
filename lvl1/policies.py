import config

# ==========================================
# POLICY A: MTD (Maximum Tolerated Dose)
# ==========================================
def mtd_policy(t, x, state):
    # Logic: Hit it with everything we have, always.
    return 1.0

# ==========================================
# POLICY B: METRONOMIC (Low Continuous)
# ==========================================
def metronomic_policy(t, x, state):
    # Logic: Keep dose low but constant.
    return 0.4

# ==========================================
# POLICY C: ADAPTIVE THERAPY (Nash)
# ==========================================
def adaptive_policy(t, x, state):
    # Logic: Stop if tumor < 50% initial size. Restart if > 100%.
    
    # 1. Calculate Tumor Burden (S + R)
    tumor_size = x[1] + x[2]
    initial_burden = config.INITIAL_POP[1] + config.INITIAL_POP[2]
    
    # 2. Check Memory (Are we currently treating?)
    if 'treating' not in state:
        state['treating'] = True
        
    # 3. Hysteresis Loop
    if state['treating']:
        # STOP condition
        if tumor_size < 0.5 * initial_burden:
            state['treating'] = False
            return 0.0
        return 1.0 # Continue Max Dose
    else:
        # RESTART condition
        if tumor_size > 0.99 * initial_burden:
            state['treating'] = True
            return 1.0
        return 0.0 # Continue Holiday

# ==========================================
# POLICY D: STACKELBERG PROBE
# ==========================================
def stackelberg_policy(t, x, state):
    # Logic: Probe -> Measure Response -> Optimize
    
    tumor_size = x[1] + x[2]
    
    # Initialize State Machine
    if 'mode' not in state:
        state['mode'] = 'PROBE_START'
        state['timer'] = 0
        state['baseline_size'] = tumor_size

    mode = state['mode']
    
    if mode == 'PROBE_START':
        state['timer'] += 1
        # Apply a moderate dose for 5 steps
        if state['timer'] > 20:
            state['mode'] = 'MEASURE'
        return 0.7 # Probe Dose
        
    elif mode == 'MEASURE':
        # Did the tumor shrink?
        delta = state['baseline_size'] - tumor_size
        
        # If High Shrinkage -> Sensitive Cells Present -> Use Adaptive Strategy
        # If Low Shrinkage -> Resistant Cells Dominant -> Stop treatment (Holiday)
        if delta > 0.01:
            state['mode'] = 'ADAPTIVE_CONTROL'
        else:
            state['mode'] = 'FULL_BREAK'
        
        state['timer'] = 0
        return 0.0
        
    elif mode == 'ADAPTIVE_CONTROL':
        # Mimic Adaptive Logic but tighter bounds
        if tumor_size > 0.3: return 0.8
        if tumor_size < 0.2: return 0.0
        return 0.0
        
    elif mode == 'FULL_BREAK':
        # Force a long holiday to let Sensitive cells regrow (if any exist)
        state['timer'] += 1
        if state['timer'] > 30:
            state['mode'] = 'PROBE_START' # Reset and probe again
            state['baseline_size'] = tumor_size
            state['timer'] = 0
        return 0.0
        
    return 0.0