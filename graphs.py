import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import statistics
import os

os.makedirs("graphs", exist_ok=True)

experiments = {
    "Эксп. 1: скан с фильтром": {
        "Hive-on-Tez": {"small": [79.602, 11.065, 9.309, 8.183, 10.093],
                        "medium": [99.29, 14.21, 64.58, 15.21, 14.00],
                        "large": [89.961, 19.50, 17.24, 15.636, 15.252]},
        "Spark NoAQE": {"small": [1.299, 1.388, 1.037, 1.175, 1.113],
                        "medium": [6.895, 6.732, 6.203, 6.552, 6.333],
                        "large": [18.643, 13.876, 94.116, 12.674, 12.433]},
        "Spark AQE":   {"small": [1.036, 1.195, 1.073, 1.16, 1.988],
                        "medium": [26.073, 5.395, 5.745, 5.633, 6.097],
                        "large": [95.644, 16.547, 19.915, 16.027, 12.909]},
    },
    "Эксп. 2: broadcast join": {
        "Hive-on-Tez": {"small": [20.678, 19.52, 18.48, 23.339, 25.216],
                        "medium": [69.442, 47.789, 59.616, 77.44, 76.559],
                        "large": [130, 88.9, 122.296, 98.712, 75.572]},
        "Spark NoAQE": {"small": [0.952, 1.577, 0.939, 0.886, 0.965],
                        "medium": [5.507, 5.295, 5.284, 64.745, 41.507],
                        "large": [17.077, 12.535, 9.335, 8.374, 8.679]},
        "Spark AQE":   {"small": [1.179, 1.188, 1.116, 0.97, 1.217],
                        "medium": [5.774, 5.135, 4.979, 5.062, 5.561],
                        "large": [85.254, 8.099, 9.1, 8.297, 8.243]},
    },
    "Эксп. 3: shuffle join (stages)": {
        "Hive-on-Tez": {"small": [112.400, 112.800, 112.600, 112.500, 112.700],
                        "medium": [145.000, 138.000, 142.000, 135.000, 140.000],
                        "large": [173.000, 189.349, 191.000, 180.000, 185.000]},
        "Spark NoAQE": {"small": [11.976, 112.365, 8.384, 7.675, 9.112],
                        "medium": [37.263, 29.766, 29.168, 30.296, 29.423],
                        "large": [72.951, 69.577, 53.893, 53.815, 54.289]},
        "Spark AQE":   {"small": [5.598, 5.005, 4.699, 6.379, 6.016],
                        "medium": [37.881, 31.995, 23.245, 26.763, 21.981],
                        "large": [160.846, 87.973, 44.15, 44.438]},
    },
    "Эксп. 4: regexp_extract": {
        "Hive-on-Tez": {"small": [4.567, 4.219, 4.873, 4.341, 4.608],
                        "medium": [13.298, 12.865, 13.711, 13.054, 13.430],
                        "large": [22.473, 23.182, 21.937, 22.541, 22.806]},
        "Spark NoAQE": {"small": [1.199, 1.012, 0.818, 0.755, 0.940],
                        "medium": [5.266, 5.287, 5.386, 7.878, 5.142],
                        "large": [15.914, 12.644, 9.296, 9.515, 8.904]},
        "Spark AQE":   {"small": [1.088, 0.976, 0.853, 0.762, 0.915],
                        "medium": [5.347, 5.192, 5.439, 7.814, 5.081],
                        "large": [15.823, 12.517, 9.381, 9.674, 8.729]},
    },
    "Эксп. 5: конвертация в date": {
        "Hive-on-Tez": {"small": [8.146, 2.387, 3.219, 2.305, 4.178],
                        "medium": [17.374, 19.129, 8.567, 8.291, 10.443],
                        "large": [65.237, 69.819, 60.402, 55.958, 65.183]},
        "Spark NoAQE": {"small": [0.499, 0.447, 0.442, 0.592, 0.465],
                        "medium": [2.268, 2.300, 2.482, 1.999, 2.206],
                        "large": [56.116, 4.333, 3.991, 3.850, 46.496]},
        "Spark AQE":   {"small": [0.498, 0.456, 0.448, 0.591, 0.462],
                        "medium": [2.481, 2.299, 2.270, 2.025, 2.188],
                        "large": [47.873, 12.291, 4.178, 3.962, 3.814]},
    },
}


tiers = ["small", "medium", "large"]

style = {
    "Hive-on-Tez": {"color": "#E07A5F", "marker": "o", "dx": 0, "dy": 14},
    "Spark NoAQE": {"color": "#3D5A80", "marker": "s", "dx":  32, "dy": 14},
    "Spark AQE":   {"color": "#81B29A", "marker": "^", "dx":   0, "dy": -24},
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
})


def cold_hot(runs):
    return runs[0], statistics.median(runs[1:])


for exp_name, configs in experiments.items():
    fig, ax = plt.subplots(figsize=(8, 5.5))

    for cfg, data in configs.items():
        ys = [cold_hot(data[t])[1] for t in tiers]
        colds = [cold_hot(data[t])[0] for t in tiers]
        st = style[cfg]
        ax.plot(tiers, ys, marker=st["marker"], label=cfg, color=st["color"],
                linewidth=2.4, markersize=9, markeredgecolor="white",
                markeredgewidth=1.5, zorder=3)
        va = "bottom" if st["dy"] > 0 else "top"
        ha = "center" if st["dx"] == 0 else (
            "right" if st["dx"] < 0 else "left")
        for x, y, c in zip(tiers, ys, colds):
            ax.annotate(f"{y:.3f}\n({c:.3f})", (x, y),
                        textcoords="offset points", xytext=(st["dx"], st["dy"]),
                        ha=ha, va=va, fontsize=8.5,
                        color=st["color"], fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.25", fc="white",
                                  ec=st["color"], lw=0.8, alpha=0.9), zorder=4)

    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("Набор данных", fontsize=11)
    ax.set_ylabel("Время выполнения, с (лог. шкала)", fontsize=11)
    ax.set_title(exp_name, fontsize=13, fontweight="bold", pad=14)
    ax.margins(y=0.22)
    ax.legend(frameon=True, framealpha=0.95, edgecolor="#cccccc",
              loc="lower right", fontsize=10)
    ax.tick_params(length=0)

    plt.tight_layout()
    fname = exp_name.split(":")[0].replace(
        ". ", "").replace("Эксп", "exp").strip() + ".png"
    path = os.path.join("graphs", fname)
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"saved {path}")
