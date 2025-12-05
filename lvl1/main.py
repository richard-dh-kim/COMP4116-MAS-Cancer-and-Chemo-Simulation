import simulation
import policies
import plotting

def main():
    print("Running Level 1: Mean-Field Evolutionary Game...")
    
    # Define the experiment list
    experiments = {
        "Policy A: MTD": simulation.run(policies.mtd_policy),
        "Policy B: Metronomic": simulation.run(policies.metronomic_policy),
        "Policy C: Adaptive (Nash)": simulation.run(policies.adaptive_policy),
        "Policy D: Stackelberg Probe": simulation.run(policies.stackelberg_policy)
    }
    
    # Visualize
    plotting.generate_charts(experiments)
    print("Done.")

if __name__ == "__main__":
    main()