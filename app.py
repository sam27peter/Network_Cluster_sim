import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

from src.config import (
    AREA_WIDTH,
    AREA_HEIGHT,
    BS_X,
    BS_Y,
    DEFAULT_CLUSTERS,
    NUM_ROUNDS,
    INITIAL_ENERGY,
)

from src.sensor import create_sensors
from src.clustering import select_cluster_heads, form_clusters
from src.simulation import (
    simulate_direct_transmission,
    simulate_clustered_round,
)
from src.energy import (
    transmission_energy,
    consume_energy,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="WSN Clustering Simulation",
    page_icon="📡",
    layout="wide",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 750;
        margin-bottom: 0;
    }

    .subtitle {
        color: #777;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }

    .round-box {
        padding: 15px;
        border-radius: 12px;
        background: rgba(128,128,128,0.08);
        text-align: center;
    }

    .round-number {
        font-size: 2rem;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        border-radius: 10px;
        padding: 10px;
        background: rgba(128,128,128,0.07);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">📡 Wireless Sensor Network Simulation</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "500 battery-powered temperature sensors • Direct vs clustered communication"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# BUILD DIRECT TRANSMISSION HISTORY
# ============================================================

def build_direct_history():

    sensors = create_sensors()

    history = []

    # --------------------------------------------------------
    # ROUND 0
    # --------------------------------------------------------

    history.append(
        {
            "energy": sum(sensor.energy for sensor in sensors),
            "alive": sum(sensor.alive for sensor in sensors),
            "energies": np.array(
                [sensor.energy for sensor in sensors]
            ),
            "alive_mask": np.array(
                [sensor.alive for sensor in sensors]
            ),
        }
    )

    # --------------------------------------------------------
    # SIMULATION
    # --------------------------------------------------------

    for _ in range(NUM_ROUNDS):

        for sensor in sensors:

            if not sensor.alive:
                continue

            distance = np.sqrt(
                (sensor.x - BS_X) ** 2
                + (sensor.y - BS_Y) ** 2
            )

            energy_used = transmission_energy(distance)

            consume_energy(
                sensor,
                energy_used,
            )

        history.append(
            {
                "energy": sum(
                    sensor.energy
                    for sensor in sensors
                ),

                "alive": sum(
                    sensor.alive
                    for sensor in sensors
                ),

                "energies": np.array(
                    [sensor.energy for sensor in sensors]
                ),

                "alive_mask": np.array(
                    [sensor.alive for sensor in sensors]
                ),
            }
        )

        if not any(sensor.alive for sensor in sensors):

            while len(history) <= NUM_ROUNDS:

                history.append(history[-1])

            break

    return history


# ============================================================
# BUILD CLUSTERED TRANSMISSION HISTORY
# ============================================================

def build_clustered_history(k):

    sensors = create_sensors()

    history = []

    previous_head_ids = []

    # --------------------------------------------------------
    # ROUND 0
    # --------------------------------------------------------

    history.append(
        {
            "energy": sum(sensor.energy for sensor in sensors),
            "alive": sum(sensor.alive for sensor in sensors),

            "energies": np.array(
                [sensor.energy for sensor in sensors]
            ),

            "alive_mask": np.array(
                [sensor.alive for sensor in sensors]
            ),

            "head_ids": [],
        }
    )

    # --------------------------------------------------------
    # SIMULATION
    # --------------------------------------------------------

    for round_number in range(1, NUM_ROUNDS + 1):

        cluster_heads = select_cluster_heads(
            sensors,
            k,
            previous_head_ids,
        )

        clusters = form_clusters(
            sensors,
            cluster_heads,
        )

        simulate_clustered_round(
            sensors,
            cluster_heads,
            clusters,
        )

        current_head_ids = [
            head.id
            for head in cluster_heads
        ]

        history.append(
            {
                "energy": sum(
                    sensor.energy
                    for sensor in sensors
                ),

                "alive": sum(
                    sensor.alive
                    for sensor in sensors
                ),

                "energies": np.array(
                    [sensor.energy for sensor in sensors]
                ),

                "alive_mask": np.array(
                    [sensor.alive for sensor in sensors]
                ),

                "head_ids": current_head_ids,
            }
        )

        previous_head_ids = current_head_ids

        if not any(sensor.alive for sensor in sensors):

            while len(history) <= NUM_ROUNDS:

                history.append(history[-1])

            break

    return history


# ============================================================
# CREATE SIMULATION DATA ONCE
# ============================================================

if "simulation_history" not in st.session_state:

    with st.spinner("Building simulation history..."):

        direct_history = build_direct_history()

        clustered_history = build_clustered_history(
            DEFAULT_CLUSTERS
        )

        st.session_state.simulation_history = {
            "direct": direct_history,
            "clustered": clustered_history,
        }


data = st.session_state.simulation_history

direct_history = data["direct"]
clustered_history = data["clustered"]


# ============================================================
# SIMULATION ROUND STATE
# ============================================================

if "selected_round" not in st.session_state:

    st.session_state.selected_round = 0


selected_round = st.session_state.selected_round


# ============================================================
# SIMULATION CONTROLS
# ============================================================

st.markdown("### 🎛️ Simulation Controls")

# ------------------------------------------------------------
# Round buttons
# ------------------------------------------------------------

round_values = list(
    range(
        0,
        NUM_ROUNDS + 1,
        100,
    )
)

round_columns = st.columns(len(round_values))

for column, round_number in zip(
    round_columns,
    round_values,
):

    with column:

        if st.button(
            str(round_number),
            use_container_width=True,
            type=(
                "primary"
                if selected_round == round_number
                else "secondary"
            ),
        ):

            st.session_state.selected_round = round_number

            st.rerun()


# ------------------------------------------------------------
# Current round information
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="round-box">
        <div>Currently viewing</div>
        <div class="round-number">
            Round {selected_round}
        </div>
        <div>
            Network state after {selected_round} communication rounds
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ------------------------------------------------------------
# Reset
# ------------------------------------------------------------

reset_col1, reset_col2, reset_col3 = st.columns(
    [1, 1, 1]
)

with reset_col2:

    if st.button(
        "🔄 Reset Simulation",
        use_container_width=True,
    ):

        st.session_state.pop(
            "simulation_history",
            None,
        )

        st.session_state.selected_round = 0

        st.rerun()


# ============================================================
# SELECTED STATES
# ============================================================

direct_state = direct_history[
    selected_round
]

clustered_state = clustered_history[
    selected_round
]


# ============================================================
# FIND TND
# ============================================================

def find_tnd(history):

    for i, state in enumerate(history):

        if state["alive"] < 500:

            return i

    return None


direct_tnd = find_tnd(
    direct_history
)

clustered_tnd = find_tnd(
    clustered_history
)


# ============================================================
# CURRENT NETWORK STATUS
# ============================================================

st.markdown("### 📊 Current Network Status")

left, right = st.columns(2)


# ============================================================
# DIRECT TRANSMISSION
# ============================================================

with left:

    st.subheader("🔴 Direct Transmission")

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Alive Sensors",
        direct_state["alive"],
    )

    d2.metric(
        "Energy",
        f"{direct_state['energy']:.1f} J",
    )

    if direct_tnd is None:

        d3.metric(
            "First Death",
            "Not reached",
        )

    else:

        d3.metric(
            "First Death",
            f"Round {direct_tnd}",
        )


# ============================================================
# CLUSTERED TRANSMISSION
# ============================================================

with right:

    st.subheader("🟢 Clustered Transmission")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Alive Sensors",
        clustered_state["alive"],
    )

    c2.metric(
        "Energy",
        f"{clustered_state['energy']:.1f} J",
    )

    if clustered_tnd is None:

        c3.metric(
            "First Death",
            "Not reached",
        )

    else:

        c3.metric(
            "First Death",
            f"Round {clustered_tnd}",
        )


# ============================================================
# NETWORK DRAW FUNCTION
# ============================================================

def draw_network(
    ax,
    state,
    title,
    clustered=False,
    show_links=True,
):

    sensors = create_sensors()

    alive_mask = state["alive_mask"]

    x = np.array(
        [sensor.x for sensor in sensors]
    )

    y = np.array(
        [sensor.y for sensor in sensors]
    )

    # --------------------------------------------------------
    # Alive nodes
    # --------------------------------------------------------

    alive_indices = np.where(
        alive_mask
    )[0]

    if len(alive_indices):

        ax.scatter(
            x[alive_indices],
            y[alive_indices],
            s=18,
            alpha=0.65,
            label="Alive Sensors",
        )

    # --------------------------------------------------------
    # Dead nodes
    # --------------------------------------------------------

    dead_indices = np.where(
        ~alive_mask
    )[0]

    if len(dead_indices):

        ax.scatter(
            x[dead_indices],
            y[dead_indices],
            s=28,
            marker="x",
            alpha=0.8,
            label="Dead Sensors",
        )

    # --------------------------------------------------------
    # Cluster Heads
    # --------------------------------------------------------

    heads = []

    if clustered:

        head_ids = state["head_ids"]

        for head_id in head_ids:

            if alive_mask[head_id]:

                heads.append(
                    head_id
                )

        if heads:

            ax.scatter(
                x[heads],
                y[heads],
                s=260,
                marker="*",
                edgecolors="black",
                linewidths=0.8,
                label="Cluster Heads",
                zorder=5,
            )

            # ------------------------------------------------
            # CH → BS
            # ------------------------------------------------

            if show_links:

                for head_id in heads:

                    ax.plot(
                        [x[head_id], BS_X],
                        [y[head_id], BS_Y],
                        linestyle="--",
                        linewidth=1.3,
                        alpha=0.45,
                        zorder=2,
                    )

    # --------------------------------------------------------
    # Base Station
    # --------------------------------------------------------

    ax.scatter(
        BS_X,
        BS_Y,
        s=330,
        marker="X",
        edgecolors="black",
        linewidths=1,
        label="Base Station",
        zorder=6,
    )

    # --------------------------------------------------------
    # Formatting
    # --------------------------------------------------------

    ax.set_xlim(
        -5,
        AREA_WIDTH + 5,
    )

    ax.set_ylim(
        -5,
        BS_Y + 10,
    )

    ax.set_aspect(
        "equal",
        adjustable="box",
    )

    ax.set_xlabel(
        "X Position (m)"
    )

    ax.set_ylabel(
        "Y Position (m)"
    )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
    )

    ax.grid(
        alpha=0.18
    )

    ax.legend(
        fontsize=8,
        loc="upper right",
    )


# ============================================================
# NETWORK TOPOLOGY
# ============================================================

st.markdown("### 🗺️ Network Topology")

show_links = st.checkbox(
    "Show Cluster Head → Base Station links",
    value=True,
)


network_left, network_right = st.columns(
    2
)


# ============================================================
# DIRECT NETWORK
# ============================================================

with network_left:

    fig, ax = plt.subplots(
        figsize=(7, 7)
    )

    draw_network(
        ax,
        direct_state,
        f"Direct Transmission\nRound {selected_round}",
        clustered=False,
    )

    st.pyplot(
        fig,
        use_container_width=True,
    )

    plt.close(fig)

    st.caption(
        "Every sensor sends its data directly to the Base Station."
    )


# ============================================================
# CLUSTERED NETWORK
# ============================================================

with network_right:

    fig, ax = plt.subplots(
        figsize=(7, 7)
    )

    draw_network(
        ax,
        clustered_state,
        f"Clustered Transmission\nRound {selected_round}",
        clustered=True,
        show_links=show_links,
    )

    st.pyplot(
        fig,
        use_container_width=True,
    )

    plt.close(fig)

    st.caption(
        "Sensors use dynamically rotated Cluster Heads before "
        "transmission to the Base Station."
    )


# ============================================================
# CLUSTER HEAD INFORMATION
# ============================================================

if selected_round > 0:

    st.markdown("### ⭐ Current Cluster Heads")

    head_ids = clustered_state["head_ids"]

    if head_ids:

        cols = st.columns(5)

        for i, head_id in enumerate(head_ids):

            with cols[i % 5]:

                st.code(
                    f"CH {head_id}"
                )

    st.caption(
        "Change the round to verify that the Cluster Heads rotate."
    )


# ============================================================
# ENERGY GRAPH
# ============================================================

st.markdown("### ⚡ Energy Consumption")

fig, ax = plt.subplots(
    figsize=(12, 4.5)
)

direct_energy = [
    state["energy"]
    for state in direct_history
]

clustered_energy = [
    state["energy"]
    for state in clustered_history
]

round_numbers = np.arange(
    0,
    NUM_ROUNDS + 1,
)

ax.plot(
    round_numbers,
    direct_energy,
    linewidth=2.5,
    label="Direct Transmission",
)

ax.plot(
    round_numbers,
    clustered_energy,
    linewidth=2.5,
    label="Clustered Transmission",
)

ax.axvline(
    selected_round,
    linestyle="--",
    linewidth=1.5,
    alpha=0.7,
    label=f"Current Round: {selected_round}",
)

ax.scatter(
    [selected_round],
    [direct_state["energy"]],
    s=60,
    zorder=5,
)

ax.scatter(
    [selected_round],
    [clustered_state["energy"]],
    s=60,
    zorder=5,
)

ax.set_title(
    "Remaining Network Energy",
    fontweight="bold",
)

ax.set_xlabel(
    "Simulation Round"
)

ax.set_ylabel(
    "Energy (J)"
)

ax.set_xlim(
    0,
    NUM_ROUNDS
)

ax.grid(
    alpha=0.2
)

ax.legend()

st.pyplot(
    fig,
    use_container_width=True,
)

plt.close(fig)


# ============================================================
# ALIVE NODE GRAPH
# ============================================================

st.markdown("### 🟢 Network Lifetime")

fig, ax = plt.subplots(
    figsize=(12, 4.5)
)

direct_alive = [
    state["alive"]
    for state in direct_history
]

clustered_alive = [
    state["alive"]
    for state in clustered_history
]

ax.plot(
    round_numbers,
    direct_alive,
    linewidth=2.5,
    label="Direct Transmission",
)

ax.plot(
    round_numbers,
    clustered_alive,
    linewidth=2.5,
    label="Clustered Transmission",
)

ax.axvline(
    selected_round,
    linestyle="--",
    linewidth=1.5,
    alpha=0.7,
    label=f"Current Round: {selected_round}",
)

ax.scatter(
    [selected_round],
    [direct_state["alive"]],
    s=60,
    zorder=5,
)

ax.scatter(
    [selected_round],
    [clustered_state["alive"]],
    s=60,
    zorder=5,
)

ax.set_title(
    "Number of Alive Sensors",
    fontweight="bold",
)

ax.set_xlabel(
    "Simulation Round"
)

ax.set_ylabel(
    "Alive Sensors"
)

ax.set_xlim(
    0,
    NUM_ROUNDS
)

ax.set_ylim(
    0,
    520
)

ax.grid(
    alpha=0.2
)

ax.legend()

st.pyplot(
    fig,
    use_container_width=True,
)

plt.close(fig)


# ============================================================
# SELECTED ROUND COMPARISON
# ============================================================

st.markdown("### 🔍 Round-by-Round Comparison")

energy_saved = (
    clustered_state["energy"]
    - direct_state["energy"]
)

alive_difference = (
    clustered_state["alive"]
    - direct_state["alive"]
)

compare1, compare2, compare3 = st.columns(3)

compare1.metric(
    "Energy Advantage",
    f"{energy_saved:.2f} J",
)

compare2.metric(
    "Additional Alive Sensors",
    alive_difference,
)

compare3.metric(
    "Selected Round",
    selected_round,
)


# ============================================================
# EXPLANATION
# ============================================================

st.markdown("### 💡 What is happening?")

st.info(
    f"""
    **Round {selected_round}**

    🔴 **Direct transmission:**  
    All alive sensors transmit directly to the Base Station.
    This causes distant sensors to consume significantly more energy.

    🟢 **Clustered transmission:**  
    Sensors communicate through approximately {DEFAULT_CLUSTERS}
    dynamically selected Cluster Heads. Cluster Heads aggregate the
    received data and transmit toward the Base Station.

    ⭐ **Cluster Head rotation:**  
    The Cluster Heads are changed between rounds so that the energy
    burden is distributed across the network.
    """
)


# ============================================================
# FINAL RESULTS
# ============================================================

st.markdown("### 🏁 Final Simulation Results")

result1, result2 = st.columns(2)

with result1:

    st.metric(
        "Direct Transmission TND",
        (
            f"Round {direct_tnd}"
            if direct_tnd is not None
            else "Not reached"
        ),
    )

with result2:

    st.metric(
        "Clustered Transmission TND",
        (
            f"Round {clustered_tnd}"
            if clustered_tnd is not None
            else "Not reached"
        ),
    )


st.caption(
    "The displayed network states and graphs are generated "
    "from the actual simulation model."
)