# stress-cpu.py
import time
import signal
import sys
import multiprocessing

# Function to simulate CPU stress
def cpu_stress():
    try:
        while True:
            for _ in range(10**6):
                pass
    except KeyboardInterrupt:
        pass  # Ignore KeyboardInterrupt in child processes

# Signal handler for graceful termination
def signal_handler(sig, frame):
    print("Received termination signal. Exiting...", file=sys.stderr)
    for process in processes:
        process.terminate()  # Terminate child processes
        process.join()  # Wait for child processes to finish
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGTERM, signal_handler)

# List to store child processes
processes = []

# Start multiple processes to stress the CPU
try:
    for _ in range(multiprocessing.cpu_count()):  # Use all CPU cores
        process = multiprocessing.Process(target=cpu_stress)
        process.start()
        processes.append(process)

    # Keep the main process alive
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping stress-cpu.py", file=sys.stderr)
    for process in processes:
        process.terminate()  # Terminate child processes
        process.join()  # Wait for child processes to finish
