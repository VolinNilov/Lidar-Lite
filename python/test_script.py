from lidar_lite import Lidar_Lite
import matplotlib.pyplot as plt
import time

lidar = Lidar_Lite()
connected = lidar.connect(1)

def read_data():
  try:
    timestamps = []
    distances = []
    velocities = []
    start_time = time.time()

    print ("[START]")

    while not lidar.exit_requested('q'):
        if connected < -1:
            print("Not Connected")
            return 
        distance = lidar.getDistance()
        velocity = lidar.getVelocity()
        print(f"Distance: {distance};    Velocity: {velocity}")
            
        elapsed_time = time.time() - start_time
        timestamps.append(elapsed_time)
        distances.append(distance)
        velocities.append(velocity)
    
    print("Finish reading data from lidar.")
    lidar.generate_graph(timestamps, distances, velocities)
    print("[END]")
    
  except Exception as e:
    print(f"[ERROR] {e}")
    print ("[END]")

read_data()