from lidar_lite import Lidar_Lite
import time
import threading
import keyboard  # Убедитесь, что установили модуль: pip install keyboard

lidar = Lidar_Lite()
connected = lidar.connect(1)

# Флаг для остановки цикла
stop_flag = False

def read_data():
    global stop_flag
    try:
        timestamps = []
        distances = []
        velocities = []
        start_time = time.time()

        print("[START]")

        while not stop_flag:
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

            time.sleep(0.1)  # Добавляем небольшую задержку, чтобы не перегружать процессор

        # После выхода из цикла генерируем график
        lidar.generate_graph(timestamps, distances, velocities)

    except Exception as e:
        print(f"[ERROR] {e}")
        print("[END]")

def listen_for_keypress():
    global stop_flag
    keyboard.wait('q')  # Ждём нажатия клавиши 'q'
    stop_flag = True
    print("\n[STOP] Клавиша 'q' нажата. Остановка сбора данных...")

if __name__ == "__main__":
    # Запускаем поток для отслеживания нажатия клавиши
    key_thread = threading.Thread(target=listen_for_keypress)
    key_thread.daemon = True
    key_thread.start()

    # Запускаем основной цикл сбора данных
    read_data()