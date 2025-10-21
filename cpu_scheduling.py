from utils import reset_processes

# ---------- FCFS ----------
def fcfs_cpu(processes):
    procs = reset_processes(processes)
    time = 0
    gantt = []

    for p in sorted(procs, key=lambda x: x.arrival):
        if time < p.arrival:
            time = p.arrival
        start = time
        time += p.burst
        end = time
        p.waiting_time = start - p.arrival
        p.turnaround_time = end - p.arrival
        gantt.append((p.pid, start, end))

    avg_wait = sum(p.waiting_time for p in procs) / len(procs)
    avg_turn = sum(p.turnaround_time for p in procs) / len(procs)
    return gantt, avg_wait, avg_turn


# ---------- Non-Preemptive SJF ----------
def sjf_cpu(processes):
    procs = reset_processes(processes)
    time = 0
    completed = []
    gantt = []

    while len(completed) < len(procs):
        ready = [p for p in procs if p.arrival <= time and p not in completed]
        if not ready:
            time += 1
            continue
        p = min(ready, key=lambda x: x.burst)
        start = time
        time += p.burst
        end = time
        p.waiting_time = start - p.arrival
        p.turnaround_time = end - p.arrival
        completed.append(p)
        gantt.append((p.pid, start, end))

    avg_wait = sum(p.waiting_time for p in procs) / len(procs)
    avg_turn = sum(p.turnaround_time for p in procs) / len(procs)
    return gantt, avg_wait, avg_turn


# ---------- Preemptive SJF (SRTF) ----------
def sjf_preemptive_cpu(processes):
    procs = reset_processes(processes)
    n = len(procs)
    time = 0
    completed = 0
    gantt = []
    last_pid = None

    while completed < n:
        ready = [p for p in procs if p.arrival <= time and p.remaining > 0]
        if ready:
            p = min(ready, key=lambda x: x.remaining)
            if p.pid != last_pid:
                gantt.append((p.pid, time))
                last_pid = p.pid
            p.remaining -= 1
            time += 1
            if p.remaining == 0:
                p.turnaround_time = time - p.arrival
                p.waiting_time = p.turnaround_time - p.burst
                completed += 1
        else:
            time += 1

    merged = []
    for i in range(len(gantt)):
        pid, start = gantt[i]
        end = gantt[i + 1][1] if i + 1 < len(gantt) else time
        if merged and merged[-1][0] == pid:
            merged[-1] = (pid, merged[-1][1], end)
        else:
            merged.append((pid, start, end))

    avg_wait = sum(p.waiting_time for p in procs) / n
    avg_turn = sum(p.turnaround_time for p in procs) / n
    return merged, avg_wait, avg_turn


# ---------- Round Robin ----------
def round_robin_cpu(processes, quantum):
    procs = reset_processes(processes)
    queue = []
    time = 0
    gantt = []
    completed = 0

    while completed < len(procs):
        for p in procs:
            if p.arrival <= time and p not in queue and p.remaining > 0:
                queue.append(p)

        if not queue:
            time += 1
            continue

        p = queue.pop(0)
        start = time
        exec_time = min(p.remaining, quantum)
        time += exec_time
        p.remaining -= exec_time
        gantt.append((p.pid, start, time))

        if p.remaining > 0:
            for q in procs:
                if q.arrival <= time and q not in queue and q.remaining > 0:
                    queue.append(q)
            queue.append(p)
        else:
            p.turnaround_time = time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst
            completed += 1

    avg_wait = sum(p.waiting_time for p in procs) / len(procs)
    avg_turn = sum(p.turnaround_time for p in procs) / len(procs)
    return gantt, avg_wait, avg_turn
