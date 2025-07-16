import matplotlib.pyplot as plt
import json
import sys

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <benchmark_data.json>")
        sys.exit(1)

    json_file = sys.argv[1]

    # Load JSON data from file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Plotting
    plt.figure(figsize=(12, 6))
    for entry in data:
        name = entry.get("name", "Unnamed")
        values = entry.get("values", [])
        color = entry.get("color", None)
        x = list(range(1, len(values) + 1))
        plt.plot(x, values, label=name, color=color)

    plt.xlabel("Time (seconds)")
    plt.ylabel("QPS")
    plt.title("Benchmark TPCC-like SF=250")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()