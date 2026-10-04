import numpy as np
from src.config import (
    NUM_SENSORS,
    AREA_WIDTH,
    AREA_HEIGHT,
    INITIAL_ENERGY,
    RANDOM_SEED
)


class Sensor:
    def __init__(self, sensor_id, x, y, energy=INITIAL_ENERGY):
        self.id = sensor_id
        self.x = x
        self.y = y
        self.energy = energy
        self.alive = True

    def position(self):
        return np.array([self.x, self.y])


def create_sensors():
    np.random.seed(RANDOM_SEED)

    sensors = []

    x_positions = np.random.uniform(0, AREA_WIDTH, NUM_SENSORS)
    y_positions = np.random.uniform(0, AREA_HEIGHT, NUM_SENSORS)

    for i in range(NUM_SENSORS):
        sensor = Sensor(
            sensor_id=i,
            x=x_positions[i],
            y=y_positions[i]
        )
        sensors.append(sensor)

    return sensors