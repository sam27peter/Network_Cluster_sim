# WSN Clustering Simulation

A simulation of a wireless sensor network with **500 battery-powered temperature sensors** deployed across an industrial area.

## Objective

Reduce energy consumption and improve network lifetime by using **Cluster Heads (CHs)** instead of direct sensor-to-Base-Station communication.

## Features

- 500 sensor nodes
- Direct transmission baseline
- Energy-based and distance-based Cluster Head selection
- Dynamic Cluster Head rotation
- Sensor-to-CH and CH-to-BS communication
- Energy consumption simulation
- Time-to-First-Node-Death (TND)
- Network lifetime comparison
- Cluster-count optimization
- Optimized `k = 25` for the tested configurations
- Visualization of network energy and alive nodes

## Project Structure

```text
n_cluster/
├── src/
│   ├── clustering.py
│   ├── config.py
│   ├── energy.py
│   ├── sensor.py
│   ├── simulation.py
│   └── visualization.py
├── results/
├── main.py
├── optimize_k.py
├── requirements.txt
└── README.md
```

## Results

For the tested 500-node network:
Method TND Alive Nodes @ 1000 Remaining Energy
Direct Transmission 203 42 12.95 J
Clustered Transmission (k=25) None 500 521.27 J

The results show that clustering significantly improves energy efficiency and network lifetime compared with direct transmission.
Running the Project
Install dependencies:
pip install -r requirements.txt

Run the main simulation:
python main.py

Optimize the number of clusters:
python optimize_k.py

Results and graphs are saved in the results/ directory.
