from src.sensor import create_sensors
from src.simulation import simulate_clustering
from src.config import NUM_ROUNDS


K_VALUES = [5, 10, 15, 20, 25]


def optimize_clusters():
    results = []

    print("Optimizing number of clusters...")
    print()

    for k in K_VALUES:

        # Fresh network for every k
        sensors = create_sensors()

        result = simulate_clustering(
            sensors,
            NUM_ROUNDS,
            k
        )

        final_energy = result["energy"][-1]
        final_alive = result["alive"][-1]
        tnd = result["tnd"]

        results.append({
            "k": k,
            "tnd": tnd,
            "final_alive": final_alive,
            "final_energy": final_energy
        })

        print(
            f"k={k:2d} | "
            f"TND={str(tnd):>4} | "
            f"Alive={final_alive:3d} | "
            f"Energy={final_energy:.2f} J"
        )

    return results


def save_results(results):
    with open("results/k_optimization.csv", "w") as file:

        file.write(
            "k,tnd,final_alive,final_energy\n"
        )

        for result in results:
            file.write(
                f"{result['k']},"
                f"{result['tnd']},"
                f"{result['final_alive']},"
                f"{result['final_energy']:.6f}\n"
            )


if __name__ == "__main__":

    results = optimize_clusters()

    save_results(results)

    print()
    print("Results saved to:")
    print("results/k_optimization.csv")