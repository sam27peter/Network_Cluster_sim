# Network Configuration

NUM_SENSORS = 500

# Deployment area (meters)
AREA_WIDTH = 100
AREA_HEIGHT = 100

# Base Station position
BS_X = 50
BS_Y = 150

# Sensor energy
INITIAL_ENERGY = 2.0  # Joules

# Data transmission
PACKET_SIZE = 4000  # bits

# Radio Energy Model
E_ELEC = 50e-9       # J/bit
E_AMP = 100e-12      # J/bit/m^2
E_DA = 5e-9          # J/bit

# Clustering
MIN_CLUSTERS = 5
MAX_CLUSTERS = 25
DEFAULT_CLUSTERS = 25

# Simulation
NUM_ROUNDS = 1000

# Random seed for reproducible results
RANDOM_SEED = 42

# Direct transmission
DIRECT_ROUNDS = 1000