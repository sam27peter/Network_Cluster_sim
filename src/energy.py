from src.config import PACKET_SIZE, E_ELEC, E_AMP, E_DA


def transmission_energy(distance):
    """Energy required to transmit one packet."""
    return PACKET_SIZE * (
        E_ELEC + E_AMP * distance ** 2
    )


def reception_energy():
    """Energy required to receive one packet."""
    return PACKET_SIZE * E_ELEC


def aggregation_energy():
    """Energy required to aggregate one received packet."""
    return PACKET_SIZE * E_DA


def consume_energy(sensor, energy_used):
    """Deduct energy from a sensor."""
    sensor.energy -= energy_used

    if sensor.energy <= 0:
        sensor.energy = 0
        sensor.alive = False