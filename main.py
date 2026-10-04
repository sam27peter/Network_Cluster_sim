from src.sensor import create_sensors
from src.clustering import select_cluster_heads, form_clusters
from src.simulation import compare_transmission_methods
from src.visualization import (
    plot_sensor_deployment,
    plot_energy_comparison,
    plot_alive_nodes,
    plot_clusters
)

from src.config import DEFAULT_CLUSTERS


def main():

    print("Running WSN clustering simulation...")

    # --------------------------------
    # Initial sensor deployment
    # --------------------------------

    sensors = create_sensors()

    plot_sensor_deployment(
        sensors,
        "results/initial_deployment.png"
    )

    # --------------------------------
    # Initial clustering visualization
    # --------------------------------

    cluster_heads = select_cluster_heads(
        sensors,
        DEFAULT_CLUSTERS
    )

    clusters = form_clusters(
        sensors,
        cluster_heads
    )

    plot_clusters(
        sensors,
        cluster_heads,
        clusters,
        "results/clustering.png"
    )

    # --------------------------------
    # Direct vs Clustered simulation
    # --------------------------------

    result = compare_transmission_methods(
        rounds=1000,
        k=DEFAULT_CLUSTERS
    )

    # --------------------------------
    # Generate comparison graphs
    # --------------------------------

    plot_energy_comparison(
        result["direct"]["energy"],
        result["clustered"]["energy"],
        "results/energy_comparison.png"
    )

    plot_alive_nodes(
        result["direct"]["alive"],
        result["clustered"]["alive"],
        "results/alive_nodes.png"
    )

    print()
    print("Simulation completed.")
    print()
    print("Direct Transmission")
    print("TND:", result["direct"]["tnd"])
    print("Final alive nodes:", result["direct"]["alive"][-1])
    print("Final energy:", result["direct"]["energy"][-1])

    print()
    print("Clustered Transmission")
    print("TND:", result["clustered"]["tnd"])
    print("Final alive nodes:", result["clustered"]["alive"][-1])
    print("Final energy:", result["clustered"]["energy"][-1])

    print()
    print("Graphs saved in results/")


if __name__ == "__main__":
    main()