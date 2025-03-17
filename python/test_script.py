import time
import csv

from lidar_lite import Lidar_Lite

def read_data():
  try:
      with Lidar_Lite() as lidar:
          connected = lidar.connect(1)
          if connected < 0:
              raise ConnectionError("Failed to connect to Lidar-Lite.")

          def read_data():
              timestamps = []
              distances = []
              velocities = []
              start_time = time.time()

              with open('lidar_data.csv', mode='w', newline='') as file:
                  writer = csv.writer(file)
                  writer.writerow(['Timestamp', 'Distance (m)', 'Velocity'])

                  print("[START] Measurements:")

                  while True:
                      distance = lidar.getDistance()
                      velocity = lidar.getVelocity()
                      elapsed_time = time.time() - start_time

                      print(f"[MEASURMENTS] {elapsed_time / 60}. Дистанция: {distance / 100} m; Скорость: {velocity}")

                      timestamps.append(elapsed_time)
                      distances.append(distance)
                      velocities.append(velocity)

                      writer.writerow([elapsed_time, distance, velocity])
                      time.sleep(0.1)

          read_data()

  except Exception as e:
      print(f"[ERROR] {e}")

read_data()