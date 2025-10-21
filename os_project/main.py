from flask import Flask, render_template, request
from cpu_scheduling import fcfs_cpu, sjf_cpu, sjf_preemptive_cpu, round_robin_cpu
from utils import Process
from visualization import plot_gantt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    processes = []
    n = int(request.form['num_processes'])
    algo = request.form['algorithm']

    for i in range(1, n + 1):
        pid = f'P{i}'
        arrival = int(request.form[f'arrival_{i}'])
        burst = int(request.form[f'burst_{i}'])
        processes.append(Process(pid, arrival, burst))

    if algo == 'FCFS':
        gantt, avg_wait, avg_turn = fcfs_cpu(processes)
    elif algo == 'SJF (Non-Preemptive)':
        gantt, avg_wait, avg_turn = sjf_cpu(processes)
    elif algo == 'SJF (Preemptive)':
        gantt, avg_wait, avg_turn = sjf_preemptive_cpu(processes)
    elif algo == 'Round Robin':
        quantum = int(request.form['quantum'])
        gantt, avg_wait, avg_turn = round_robin_cpu(processes, quantum)
    else:
        return "Invalid algorithm selected!"

    plot_gantt(gantt, save_path='static/gantt.png')
    return render_template('result.html',
                           algo=algo,
                           gantt=gantt,
                           avg_wait=round(avg_wait, 2),
                           avg_turn=round(avg_turn, 2))

if __name__ == "__main__":
    app.run(debug=True)
