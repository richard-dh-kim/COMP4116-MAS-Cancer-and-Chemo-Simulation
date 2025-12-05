import matplotlib.pyplot as plt
import numpy as np

def generate_charts(results):
    num_pols = len(results)
    # Wider figure for 3 columns
    fig, axes = plt.subplots(num_pols, 3, figsize=(18, 3 * num_pols))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    
    row = 0
    for name, data in results.items():
        t, x, drug, tox = data
        
        # Col 1: Populations
        ax1 = axes[row, 0]
        ax1.plot(t, x[:,0], 'g', label="Healthy", alpha=0.3)
        ax1.plot(t, x[:,1], 'b', label="Sensitive", linewidth=2)
        ax1.plot(t, x[:,2], 'r', label="Resistant", linewidth=2)
        ax1.set_title(f"{name}: Populations")
        ax1.set_ylim(0, 1.05)
        ax1.set_ylabel("Population %")
        # FIX: Only put legend on the top row
        if row == 0: ax1.legend(loc='right') 
        ax1.grid(alpha=0.3)
        
        # Col 2: Tumor Load
        ax2 = axes[row, 1]
        tumor_load = x[:,1] + x[:,2]
        ax2.fill_between(t, drug, color='purple', alpha=0.15, label="Dose")
        ax2.plot(t, tumor_load, 'k', linewidth=2, label="Tumor Burden")
        ax2.set_title(f"{name}: Treatment")
        ax2.set_ylim(0, 1.05)
        
        if row == 0: ax2.legend(loc='right') 
        ax2.set_ylabel("Tumor Load / Drug")
        ax2.grid(alpha=0.3)
        
        # Col 3: Toxicity (NEW)
        ax3 = axes[row, 2]
        ax3.plot(t, tox, 'r--', linewidth=2)
        ax3.fill_between(t, tox, color='red', alpha=0.1)
        ax3.set_title(f"{name}: Cumulative Toxicity")
        ax3.set_ylabel("Total Drug Exposure")
        ax3.grid(alpha=0.3)
        
        final_val = tox[-1]
        # Use transform=ax3.transAxes to place text based on the box percentage (0.95 = 95% across)
        ax3.text(0.95, 0.05, f"Total Toxicity: {final_val:.1f}", 
                 transform=ax3.transAxes, 
                 ha='right', va='bottom', 
                 fontsize=12, fontweight='bold', color='darkred',
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        row += 1
        
    print("Saving to 'level1_results.png'...")
    plt.savefig("level1_results.png")
    plt.show()