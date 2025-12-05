import spatial_simulation
import spatial_strategies
import spatial_plotting

def main():
    print("Running Level 2: Spatial Evolutionary Game...")
    
    experiments = {
        "Policy A: MTD": spatial_simulation.run(spatial_strategies.mtd_policy),
        "Policy B: Metronomic": spatial_simulation.run(spatial_strategies.metronomic_policy),
        "Policy C: Adaptive (Nash)": spatial_simulation.run(spatial_strategies.adaptive_policy),
        "Policy D: Stackelberg": spatial_simulation.run(spatial_strategies.stackelberg_policy)
    }
    
    print("Generating Plots...")
    spatial_plotting.plot_stats(experiments)
    spatial_plotting.plot_grids(experiments)
    print("Done!")

if __name__ == "__main__":
    main()