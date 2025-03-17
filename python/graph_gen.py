import csv
import matplotlib.pyplot as plt
from lidar_lite import Lidar_Lite

lidar = Lidar_Lite()

def read_csv_and_generate_graph(file_path):
    time_stamps = []
    distances_array = []
    velocities_array = []

    try:
        print("[START] Graph generation ...")
        # Открываем CSV файл для чтения
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовки

            # Читаем данные из файла
            for row in reader:
                if len(row) == 3:  # Убедимся, что строка содержит все три значения
                    timestamp = float(row[0])
                    distance = float(row[1])
                    velocity = float(row[2])

                    time_stamps.append(timestamp)
                    distances_array.append(distance)
                    velocities_array.append(velocity)

        # Генерируем графики
        lidar.generate_graph(time_stamps, distances_array, velocities_array)
        print("[END] Of graph generation.")

    except Exception as e:
        print(f"[ERROR] {e}")

read_csv_and_generate_graph('lidar_data.csv')