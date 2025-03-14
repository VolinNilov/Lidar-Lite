from lidar_lite import Lidar_Lite
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

    while True:
      if connected < -1:
          print("Not Connected")
          return 
      distance = lidar.getDistance()
      velocity = lidar.getVelocity()
      print(f"Дистанция: {distance};    Скорость: {velocity}")
          
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