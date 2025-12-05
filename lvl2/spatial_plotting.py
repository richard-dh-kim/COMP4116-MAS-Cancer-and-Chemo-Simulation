import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import config

# Define colors: White (Empty), Green (Healthy), Blue (Sensitive), Red (Resistant)
CMAP = mcolors.ListedColormap(['white', '#90EE90', '#1E90FF', '#FF4500'])
BOUNDS = [0, 1, 2, 3, 4]
NORM = mcolors.BoundaryNorm(BOUNDS, CMAP.N)

def plot_stats(experiments):
    """
    Plots the population and toxicity history for all policies.
    """
    num = len(experiments)
    fig, axes = plt.subplots(num, 3, figsize=(18, 3*num))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    
    # Ensure axes is always 2D (even if only 1 experiment)
    if num == 1: axes = np.array([axes])
    
    row = 0
    for name, data in experiments.items():
        t = data['time']
        
        # 1. Populations
        ax1 = axes[row, 0]
        ax1.plot(t, data['h'], 'g', label='Healthy', alpha=0.4)
        ax1.plot(t, data['s'], 'b', label='Sensitive', linewidth=2)
        ax1.plot(t, data['r'], 'r', label='Resistant', linewidth=2)
        ax1.set_ylim(0, 1.0)
        ax1.set_title(f"{name}: Populations")
        if row == 0: ax1.legend(loc='right')
        ax1.grid(alpha=0.3)
        ax1.set_ylabel("Fraction of Grid")
        
        # 2. Tumor vs Drug
        ax2 = axes[row, 1]
        tumor = np.array(data['s']) + np.array(data['r'])
        # Scale drug for visualization (so it fits on 0-1 axis)
        scaled_drug = np.array(data['drug']) 
        ax2.fill_between(t, scaled_drug, color='purple', alpha=0.15, label='Drug Dose')
        ax2.plot(t, tumor, 'k', linewidth=2, label='Tumor Size')
        ax2.set_ylim(0, 1.0)
        ax2.set_title(f"{name}: Treatment")
        if row == 0: ax2.legend(loc='upper right')
        ax2.grid(alpha=0.3)
        
        # 3. Toxicity
        ax3 = axes[row, 2]
        ax3.plot(t, data['tox'], 'r--', label='Cumulative Tox')
        ax3.fill_between(t, data['tox'], color='red', alpha=0.1)
        
        # Add a Limit Line for context
        ax3.axhline(y=config.TOX_LIMIT, color='k', linestyle=':', label='Death Limit')
        
        ax3.set_title("Cumulative Toxicity")
        final_tox = data['tox'][-1]
        
        # Label if patient died
        if final_tox > config.TOX_LIMIT:
            ax3.text(0.5, 0.5, "PATIENT DIED", transform=ax3.transAxes, 
                     ha='center', va='center', color='red', fontweight='bold', fontsize=14, rotation=30)
        
        ax3.text(0.95, 0.05, f"{final_tox:.1f}", transform=ax3.transAxes, 
                 ha='right', va='bottom', color='darkred', fontweight='bold', fontsize=12)
        
        row += 1
        
    plt.savefig("spatial_stats.png")
    print("Saved spatial_stats.png")

def plot_grids(experiments):
    """
    Plots snapshots of the grid at different time steps.
    Handles cases where some experiments end early (death).
    """
    targets = list(experiments.keys())
    
    # 1. Find the maximum number of snapshots across ALL experiments
    # (Because Stackelberg survived, it has more snaps than MTD)
    max_snaps = 0
    for name in targets:
        max_snaps = max(max_snaps, len(experiments[name]['snapshots']))
    
    # 2. Setup Subplots with squeeze=False to force 2D array behavior
    fig, axes = plt.subplots(len(targets), max_snaps, figsize=(3 * max_snaps, 16), squeeze=False)
    
    for i, name in enumerate(targets):
        snaps = experiments[name]['snapshots']
        times = experiments[name]['snap_times']
        
        for j in range(max_snaps):
            ax = axes[i, j]
            
            # If this experiment has a snapshot for this column, plot it
            if j < len(snaps):
                grid = snaps[j]
                ax.imshow(grid, cmap=CMAP, norm=NORM)
                if i == 0: ax.set_title(f"Time: {times[j]}")
            else:
                # If the patient died early, show a "Dead" placeholder
                ax.text(0.5, 0.5, "PATIENT\nDIED", ha='center', va='center', color='red', fontweight='bold')
                ax.set_facecolor('#ffeeee') # Light red background
                
            ax.set_xticks([])
            ax.set_yticks([])
            if j == 0: ax.set_ylabel(name, fontsize=10, rotation=90)
            
    plt.tight_layout()
    plt.savefig("spatial_grids.png")
    print("Saved spatial_grids.png")