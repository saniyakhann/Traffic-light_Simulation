import time
import threading
import random

GREEN_DURATION = 10
RED_DURATION = 10
SIMULATION_DURATION = 120  # Total simulation time in seconds

class TrafficLightAI:
    def __init__(self):
        self.lane_1_density = random.randint(0, 20)
        self.lane_2_density = random.randint(0, 20)
        self.lane_1_wait_time = 0
        self.lane_2_wait_time = 0
        self.lane_1_passed = 0
        self.lane_2_passed = 0

    def ai_traffic_light(self):
        end_time = time.time() + SIMULATION_DURATION
        while time.time() < end_time:
            print(f"Initial densities - Lane 1: {self.lane_1_density}, Lane 2: {self.lane_2_density}")

            if self.lane_1_density > self.lane_2_density:
                print("Lane 1: GREEN")
                time.sleep(GREEN_DURATION)
                passed = random.randint(1, 5)
                self.lane_1_density -= passed  # Simulate cars passing
                self.lane_1_passed += passed
                self.lane_2_density += random.randint(0, 2)  # Simulate cars arriving at red light
                self.lane_2_wait_time += RED_DURATION
            else:
                print("Lane 2: GREEN")
                time.sleep(GREEN_DURATION)
                passed = random.randint(1, 5)
                self.lane_2_density -= passed  # Simulate cars passing
                self.lane_2_passed += passed
                self.lane_1_density += random.randint(0, 2)  # Simulate cars arriving at red light
                self.lane_1_wait_time += RED_DURATION

            self.lane_1_density = max(0, self.lane_1_density)
            self.lane_2_density = max(0, self.lane_2_density)

            print(f"Updated densities - Lane 1: {self.lane_1_density}, Lane 2: {self.lane_2_density}")
            print("Switching lights...")
            time.sleep(RED_DURATION)

    def start_ai_based_system(self):
        ai_thread = threading.Thread(target=self.ai_traffic_light)
        ai_thread.start()
        ai_thread.join()

        return self.lane_1_wait_time, self.lane_2_wait_time, self.lane_1_passed, self.lane_2_passed

ai_system = TrafficLightAI()
ai_results = ai_system.start_ai_based_system()
print("AI-based System Results:")
print(f"Lane 1 Total Wait Time: {ai_results[0]} seconds")
print(f"Lane 2 Total Wait Time: {ai_results[1]} seconds")
print(f"Lane 1 Total Cars Passed: {ai_results[2]}")
print(f"Lane 2 Total Cars Passed: {ai_results[3]}")
