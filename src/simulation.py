import numpy as np

from src.config import BS_X, BS_Y
from src.energy import (
    transmission_energy,
    reception_energy,
    aggregation_energy,
    consume_energy
)


def distance_to_bs(sensor):
    """Calculate distance from sensor to Base Station."""
    return np.sqrt(
        (sensor.x - BS_X) ** 2 +
        (sensor.y - BS_Y) ** 2
    )


def distance_between(sensor_a, sensor_b):
    """Calculate distance between two sensors."""
    return np.sqrt(
        (sensor_a.x - sensor_b.x) ** 2 +
        (sensor_a.y - sensor_b.y) ** 2
    )


def simulate_direct_transmission(sensors, rounds):
    """Every sensor transmits directly to the Base Station."""

    energy_history = []
    alive_history = []

    for _ in range(rounds):

        for sensor in sensors:
            if sensor.alive:
                distance = distance_to_bs(sensor)
                energy_used = transmission_energy(distance)
                consume_energy(sensor, energy_used)

        total_energy = sum(sensor.energy for sensor in sensors)
        alive_nodes = sum(sensor.alive for sensor in sensors)

        energy_history.append(total_energy)
        alive_history.append(alive_nodes)

        if alive_nodes == 0:
            break

    return energy_history, alive_history


def simulate_clustered_round(sensors, cluster_heads, clusters):
    """Simulate one round of clustered communication."""

    total_energy_used = 0.0

    # Sensors → Cluster Head
    for head in cluster_heads:

        if not head.alive:
            continue

        for sensor in clusters[head.id]:

            if sensor.id == head.id or not sensor.alive:
                continue

            distance = distance_between(sensor, head)

            tx_energy = transmission_energy(distance)
            rx_energy = reception_energy()
            da_energy = aggregation_energy()

            consume_energy(sensor, tx_energy)
            consume_energy(head, rx_energy + da_energy)

            total_energy_used += (
                tx_energy +
                rx_energy +
                da_energy
            )

    # Cluster Head → Base Station
    for head in cluster_heads:

        if not head.alive:
            continue

        distance = distance_to_bs(head)
        tx_energy = transmission_energy(distance)

        consume_energy(head, tx_energy)

        total_energy_used += tx_energy

    return total_energy_used
from src.clustering import select_cluster_heads, form_clusters


def simulate_clustering(sensors, rounds, k):
    """
    Run the complete clustered WSN simulation.
    """

    energy_history = []
    alive_history = []
    cluster_heads_history = []

    previous_head_ids = []
    first_node_death = None

    for round_number in range(rounds):

        # Select new Cluster Heads
        cluster_heads = select_cluster_heads(
            sensors,
            k,
            previous_head_ids
        )

        # Form clusters
        clusters = form_clusters(
            sensors,
            cluster_heads
        )

        # Simulate communication
        simulate_clustered_round(
            sensors,
            cluster_heads,
            clusters
        )

        # Record results
        total_energy = sum(
            sensor.energy for sensor in sensors
        )

        alive_nodes = sum(
            sensor.alive for sensor in sensors
        )

        energy_history.append(total_energy)
        alive_history.append(alive_nodes)

        cluster_heads_history.append(
            [head.id for head in cluster_heads]
        )

        # Detect first node death
        if alive_nodes < len(sensors) and first_node_death is None:
            first_node_death = round_number + 1

        # Prepare CH rotation
        previous_head_ids = [
            head.id for head in cluster_heads
        ]

        if alive_nodes == 0:
            break

    return {
        "energy": energy_history,
        "alive": alive_history,
        "cluster_heads": cluster_heads_history,
        "tnd": first_node_death
    }

from src.sensor import create_sensors
from src.config import NUM_ROUNDS, DEFAULT_CLUSTERS


def compare_transmission_methods(
    rounds=NUM_ROUNDS,
    k=DEFAULT_CLUSTERS
):
    """
    Compare direct transmission with clustered transmission.
    """

    # -----------------------------
    # Direct Transmission
    # -----------------------------
    direct_sensors = create_sensors()

    direct_energy, direct_alive = simulate_direct_transmission(
        direct_sensors,
        rounds
    )

    # -----------------------------
    # Clustered Transmission
    # -----------------------------
    clustered_sensors = create_sensors()

    clustered_result = simulate_clustering(
        clustered_sensors,
        rounds,
        k
    )

    # -----------------------------
    # Return comparison
    # -----------------------------
    return {
        "direct": {
            "energy": direct_energy,
            "alive": direct_alive,
            "tnd": next(
                (
                    i + 1
                    for i, alive in enumerate(direct_alive)
                    if alive < len(direct_sensors)
                ),
                None
            )
        },
        "clustered": clustered_result
    }