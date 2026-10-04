from src.clustering import select_cluster_heads, form_clusters
from src.simulation import simulate_clustered_round


class LiveClusterSimulation:

    def __init__(self, sensors, k):
        self.sensors = sensors
        self.k = k

        self.round = 0
        self.previous_head_ids = []

        self.cluster_heads = []
        self.clusters = {}

        self.total_energy = sum(
            sensor.energy for sensor in sensors
        )

        self.alive_nodes = len(sensors)

        self.tnd = None

    def step(self):
        """Run exactly one simulation round."""

        if self.alive_nodes == 0:
            return False

        self.round += 1

        # Select Cluster Heads
        self.cluster_heads = select_cluster_heads(
            self.sensors,
            self.k,
            self.previous_head_ids
        )

        # Form clusters
        self.clusters = form_clusters(
            self.sensors,
            self.cluster_heads
        )

        # Run actual communication
        simulate_clustered_round(
            self.sensors,
            self.cluster_heads,
            self.clusters
        )

        # Update statistics
        self.total_energy = sum(
            sensor.energy for sensor in self.sensors
        )

        self.alive_nodes = sum(
            sensor.alive for sensor in self.sensors
        )

        # Detect first node death
        if (
            self.alive_nodes < len(self.sensors)
            and self.tnd is None
        ):
            self.tnd = self.round

        # Save CHs for rotation
        self.previous_head_ids = [
            head.id
            for head in self.cluster_heads
        ]

        return True