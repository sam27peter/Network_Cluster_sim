import os
import matplotlib.pyplot as plt

from src.config import (
    AREA_WIDTH,
    AREA_HEIGHT,
    BS_X,
    BS_Y
)


def plot_sensor_deployment(sensors, output_path):
    """Plot the initial sensor deployment."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    x = [sensor.x for sensor in sensors]
    y = [sensor.y for sensor in sensors]

    plt.figure(figsize=(8, 7))

    plt.scatter(x, y, s=12, label="Sensors")
    plt.scatter(
        BS_X,
        BS_Y,
        marker="*",
        s=200,
        label="Base Station"
    )

    plt.xlim(0, AREA_WIDTH)
    plt.ylim(0, BS_Y + 10)

    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.title("Initial Sensor Deployment")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_energy_comparison(
    direct_energy,
    clustered_energy,
    output_path
):
    """Plot remaining network energy."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    rounds_direct = range(1, len(direct_energy) + 1)
    rounds_clustered = range(1, len(clustered_energy) + 1)

    plt.figure(figsize=(9, 6))

    plt.plot(
        rounds_direct,
        direct_energy,
        label="Direct Transmission"
    )

    plt.plot(
        rounds_clustered,
        clustered_energy,
        label="Clustered Transmission"
    )

    plt.xlabel("Round")
    plt.ylabel("Remaining Energy (J)")
    plt.title("Network Energy vs. Rounds")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_alive_nodes(
    direct_alive,
    clustered_alive,
    output_path
):
    """Plot number of alive sensors."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    rounds_direct = range(1, len(direct_alive) + 1)
    rounds_clustered = range(1, len(clustered_alive) + 1)

    plt.figure(figsize=(9, 6))

    plt.plot(
        rounds_direct,
        direct_alive,
        label="Direct Transmission"
    )

    plt.plot(
        rounds_clustered,
        clustered_alive,
        label="Clustered Transmission"
    )

    plt.xlabel("Round")
    plt.ylabel("Alive Sensors")
    plt.title("Network Lifetime Comparison")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_clusters(
    sensors,
    cluster_heads,
    clusters,
    output_path
):
    """Plot sensors and their Cluster Heads."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(8, 7))

    for head_id, members in clusters.items():

        if not members:
            continue

        x = [sensor.x for sensor in members]
        y = [sensor.y for sensor in members]

        plt.scatter(
            x,
            y,
            s=10,
            alpha=0.5
        )

    head_x = [head.x for head in cluster_heads]
    head_y = [head.y for head in cluster_heads]

    plt.scatter(
        head_x,
        head_y,
        marker="*",
        s=180,
        label="Cluster Heads"
    )

    plt.scatter(
        BS_X,
        BS_Y,
        marker="X",
        s=150,
        label="Base Station"
    )

    plt.xlim(0, AREA_WIDTH)
    plt.ylim(0, BS_Y + 10)

    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.title("Sensor Clustering")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()