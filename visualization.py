import matplotlib.pyplot as plt

def plot_gantt(gantt, save_path=None):
    fig, ax = plt.subplots(figsize=(7, 3))

    if not gantt:
        ax.text(0.5, 0.5, "No schedule to display", ha='center', va='center')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            plt.close(fig)
        else:
            plt.show()
        return

    pids = []
    for pid, start, end in gantt:
        if pid not in pids:
            pids.append(pid)

    y_positions = {pid: i for i, pid in enumerate(reversed(pids), start=1)}
    bar_height = 0.6

    for pid, start, end in gantt:
        y = y_positions[pid]
        ax.barh(y, end - start, left=start, height=bar_height, edgecolor='black', color='#007bff')
        ax.text((start + end) / 2, y, pid, ha='center', va='center', color='white', fontsize=9, fontweight='bold')

    ax.set_xlabel("Time")
    ax.set_ylabel("Process")
    ax.set_title("CPU Scheduling Gantt Chart", fontweight='bold')
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(list(reversed(pids)))
    ax.set_xlim(left=0)
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close(fig)
    else:
        plt.show()
