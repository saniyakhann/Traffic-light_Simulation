#this is a simulation of a traffic light set up with a timer

import time
import threading
import random

GREEN_DURATION = 10
RED_DURATION = 10
SIMULATION_DURATION = 120  # Total simulation time in seconds

class TrafficLightTimer:
    def __init__(self):
        self.lane_1_wait_time = 0
        self.lane_2_wait_time = 0
        self.lane_1_passed = 0
        self.lane_2_passed = 0

    def timer_traffic_light(self, lane_id):
        end_time = time.time() + SIMULATION_DURATION
        while time.time() < end_time:
            if lane_id == 1:
                self.lane_1_wait_time += RED_DURATION
                self.lane_1_passed += random.randint(1, 5)  # Simulate cars passing
            else:
                self.lane_2_wait_time += RED_DURATION
                self.lane_2_passed += random.randint(1, 5)  # Simulate cars passing

            print(f"Lane {lane_id}: GREEN")
            time.sleep(GREEN_DURATION)
            print(f"Lane {lane_id}: RED")
            time.sleep(RED_DURATION)

    def start_timer_based_system(self):
        lane_1_thread = threading.Thread(target=self.timer_traffic_light, args=(1,))
        lane_2_thread = threading.Thread(target=self.timer_traffic_light, args=(2,))

        lane_1_thread.start()
        lane_2_thread.start()

        lane_1_thread.join()
        lane_2_thread.join()

        return self.lane_1_wait_time, self.lane_2_wait_time, self.lane_1_passed, self.lane_2_passed

timer_system = TrafficLightTimer()
timer_results = timer_system.start_timer_based_system()
print("Timer-based System Results:")
print(f"Lane 1 Total Wait Time: {timer_results[0]} seconds")
print(f"Lane 2 Total Wait Time: {timer_results[1]} seconds")
print(f"Lane 1 Total Cars Passed: {timer_results[2]}")
print(f"Lane 2 Total Cars Passed: {timer_results[3]}")

