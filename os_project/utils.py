class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.waiting_time = 0
        self.turnaround_time = 0

def reset_processes(processes):
    for p in processes:
        p.remaining = p.burst
        p.waiting_time = 0
        p.turnaround_time = 0
    return processes
