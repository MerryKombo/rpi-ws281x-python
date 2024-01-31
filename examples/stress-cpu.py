import multiprocessing

def worker():
    # Worker function, runs in an infinite loop
    while True:
        # Perform a heavy computation
        for _ in range(10**6):
            pass

if __name__ == '__main__':
    # Start as many processes as there are CPUs
    for _ in range(multiprocessing.cpu_count()):
        multiprocessing.Process(target=worker).start()