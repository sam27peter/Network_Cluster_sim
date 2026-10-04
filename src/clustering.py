import numpy as np

from src.config import BS_X, BS_Y, DEFAULT_CLUSTERS


def select_cluster_heads(
    sensors,
    k=DEFAULT_CLUSTERS,
    previous_head_ids=None
):
    """
    Select Cluster Heads using residual energy and
    distance to the Base Station.

    Previous Cluster Heads are excluded when enough
    other alive sensors are available, allowing CH rotation.
    """

    previous_head_ids = previous_head_ids or []

    alive_sensors = [
        sensor for sensor in sensors
        if sensor.alive
    ]

    if not alive_sensors:
        return []

    k = min(k, len(alive_sensors))

    # Prefer sensors that were not CHs in the previous round
    candidates = [
        sensor for sensor in alive_sensors
        if sensor.id not in previous_head_ids
    ]

    # If not enough candidates remain, use all alive sensors
    if len(candidates) < k:
        candidates = alive_sensors

    distances = np.array([
        np.sqrt(
            (sensor.x - BS_X) ** 2 +
            (sensor.y - BS_Y) ** 2
        )
        for sensor in candidates
    ])

    energies = np.array([
        sensor.energy for sensor in candidates
    ])

    max_energy = max(energies.max(), 1e-12)
    max_distance = max(distances.max(), 1e-12)

    energy_score = energies / max_energy
    distance_score = 1 - (distances / max_distance)

    scores = (
        0.7 * energy_score +
        0.3 * distance_score
    )

    indices = np.argpartition(scores, -k)[-k:]

    return [candidates[i] for i in indices]

def form_clusters(sensors, cluster_heads):
    """
    Assign every alive sensor to its nearest Cluster Head.
    """

    clusters = {head.id: [] for head in cluster_heads}

    if not cluster_heads:
        return clusters

    for sensor in sensors:
        if not sensor.alive:
            continue

        nearest_head = min(
            cluster_heads,
            key=lambda head: (
                (sensor.x - head.x) ** 2 +
                (sensor.y - head.y) ** 2
            )
        )

        clusters[nearest_head.id].append(sensor)

    return clusters