import os

load_1, load_5, load_15 = os.getloadavg()

print(f"1 minute load: {load_1}")
print(f"5 minute load: {load_5}")
print(f"15 minute load: {load_15}")