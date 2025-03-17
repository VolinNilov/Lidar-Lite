from lidar_lite import Lidar_Lite
import time
import csv

lidar = Lidar_Lite()
connected = lidar.connect(1)

def read_data():
    try:
        timestamps = []
        distances = []
        velocities = []
        start_time = time.time()

        # Открываем CSV файл для записи
        with open('lidar_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Записываем заголовки колонок
            writer.writerow(['Timestamp', 'Distance (cm)', 'Velocity'])

            print("[START] Measurements:")

            while True:
                if connected < -1:
                    print("Not Connected")
                    return 

                distance = lidar.getDistance()
                velocity = lidar.getVelocity()
                print(f"Дистанция: {distance / 100} m;    Скорость: {velocity}")
                
                elapsed_time = time.time() - start_time
                timestamps.append(elapsed_time)
                distances.append(distance)
                velocities.append(velocity)

                # Записываем текущие данные в CSV файл
                writer.writerow([timestamps, distance, velocity])

                # Добавляем небольшую задержку для избежания перегрузки
                time.sleep(0.1)

    except Exception as e:
        print(f"[ERROR] {e}")

read_data()