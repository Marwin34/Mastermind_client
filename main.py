import communication
import time

if __name__ == '__main__':
    communication_module = communication.ComSupervisor("127.0.0.1", 50001)
    communication_module.connect()
    time_stamp = 0.016  # 60 FPS
    last_update = 0

    while True:
        if time.perf_counter() - last_update >= time_stamp:
            data = {
                'type': 'hi',
                'value': input()
            }

            communication_module.send(data)

            # print(1 / (time.perf_counter() - last_update))
            last_update = time.perf_counter()
