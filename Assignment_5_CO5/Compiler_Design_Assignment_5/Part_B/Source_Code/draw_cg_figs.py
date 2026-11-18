"""Generate required graphs from actual CSV measurements."""
import csv, os
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MEAS = os.path.join(ROOT, "Measurements")
SCREEN = os.path.join(ROOT, "Screenshots")
os.makedirs(SCREEN, exist_ok=True)


def read_csv(name):
    with open(os.path.join(MEAS, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cfg_illustration():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    positions = {"B0": (0.1,0.75), "B1": (0.38,0.75), "B2": (0.66,0.75),
                 "B3": (0.66,0.35), "B4": (0.38,0.35)}
    for name, (x,y) in positions.items():
        ax.text(x,y,name,bbox=dict(boxstyle="round",fc="#dbeafe"),ha="center")
    for a,b in [(("B0","B1"),(0)), (("B1","B2"),(0)), (("B2","B3"),(0)),
                (("B3","B1"),(0)), (("B2","B4"),(0))]:
        pass
    ax.annotate("", xy=(0.38,0.75), xytext=(0.16,0.75), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.66,0.75), xytext=(0.44,0.75), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.66,0.35), xytext=(0.66,0.68), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.38,0.75), xytext=(0.60,0.40), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.38,0.35), xytext=(0.60,0.68), arrowprops=dict(arrowstyle="->"))
    fig.suptitle("Illustrative control-flow graph")
    fig.savefig(os.path.join(SCREEN, "control_flow_graph.png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


def register_comparison():
    rows = read_csv("b1_register_measurements.csv")
    subset = [r for r in rows if r["test"] == "straight_line" and r["strategy"] == "farther"]
    if subset:
        ks = [int(r["registers"]) for r in subset]
        costs = [int(r["cost"]) for r in subset]
        fig, ax = plt.subplots()
        ax.plot(ks, costs, marker="o")
        ax.set(title="Straight-line register-count effect", xlabel="Register count",
               ylabel="Estimated target cost")
        fig.savefig(os.path.join(SCREEN, "register_allocation_comparison.png"), dpi=180, bbox_inches="tight")
        plt.close(fig)


def scalability():
    rows = read_csv("b3_scalability.csv")
    fig, ax = plt.subplots()
    for order in ("program", "reverse_postorder"):
        vals = [r for r in rows if r["order"] == order]
        ax.plot([int(r["blocks"]) for r in vals],
                [int(r["set_operations"]) for r in vals],
                marker="o", label=order)
    ax.set(title="Data-flow scalability", xlabel="Blocks", ylabel="Set operations")
    ax.legend()
    fig.savefig(os.path.join(SCREEN, "b3_scalability.png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


def b4_graph():
    rows = read_csv("b4_optimisation_levels.csv")
    fig, ax = plt.subplots()
    ax.bar([f"L{r['level']}" for r in rows],
           [int(r["target_cost"]) for r in rows])
    ax.set(title="B4 target cost by optimisation level", ylabel="Estimated cost")
    fig.savefig(os.path.join(SCREEN, "b4_optimisation_levels.png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    cfg_illustration()
    register_comparison()
    scalability()
    b4_graph()
