import time
import threading
import random
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score

#configuration constants
GREEN_DURATION = 10
RED_DURATION = 10
SIMULATION_DURATION = 30  #reduced for quicker testing

class TrafficLightSystem:
    """base class for traffic light systems"""
    def __init__(self):
        self.lane_1_wait = 0
        self.lane_2_wait = 0
        self.lane_1_cars = 0
        self.lane_2_cars = 0
        self.lock = threading.Lock()

class TimerSystem(TrafficLightSystem):
    """timer-based system with fixed intervals"""
    def run_lane(self, lane_id):
        end_time = time.time() + SIMULATION_DURATION
        while time.time() < end_time:
            with self.lock:
                if lane_id == 1:
                    self.lane_1_wait += RED_DURATION
                    self.lane_1_cars += random.randint(1, 5)
                else:
                    self.lane_2_wait += RED_DURATION
                    self.lane_2_cars += random.randint(1, 5)
            time.sleep(GREEN_DURATION + RED_DURATION)

    def simulate(self):
        lane1 = threading.Thread(target=self.run_lane, args=(1,))
        lane2 = threading.Thread(target=self.run_lane, args=(2,))
        lane1.start(); lane2.start()
        lane1.join(); lane2.join()
        return self.get_results()

    def get_results(self):
        return {"lane1_wait": self.lane_1_wait, "lane2_wait": self.lane_2_wait,
                "lane1_cars": self.lane_1_cars, "lane2_cars": self.lane_2_cars}

class AISystem(TrafficLightSystem):
    """ai-based system with dynamic scheduling"""
    def __init__(self):
        super().__init__()
        self.lane1_density = random.randint(5, 20)
        self.lane2_density = random.randint(5, 20)

    def simulate(self):
        end_time = time.time() + SIMULATION_DURATION
        while time.time() < end_time:
            with self.lock:
                if self.lane1_density > self.lane2_density:
                    cars_passed = min(self.lane1_density, random.randint(1, 5))
                    self.lane1_density -= cars_passed
                    self.lane1_cars += cars_passed
                    self.lane2_density += random.randint(0, 2)
                    self.lane2_wait += GREEN_DURATION
                else:
                    cars_passed = min(self.lane2_density, random.randint(1, 5))
                    self.lane2_density -= cars_passed
                    self.lane2_cars += cars_passed
                    self.lane1_density += random.randint(0, 2)
                    self.lane1_wait += GREEN_DURATION
            time.sleep(GREEN_DURATION + 2)  #green + transition time

        return self.get_results()

    def get_results(self):
        return {"lane1_wait": self.lane_1_wait, "lane2_wait": self.lane_2_wait,
                "lane1_cars": self.lane_1_cars, "lane2_cars": self.lane_2_cars}

def run_machine_learning():
    """run ml traffic prediction simulation"""
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    model = SVC(kernel='rbf', random_state=0)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    #save predictions
    pd.DataFrame(y_pred, columns=['predicted_traffic']).to_csv('traffic_predictions.csv', index=True)
    
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average='weighted'),
        "recall": recall_score(y_test, y_pred, average='weighted')
    }

def print_results(title, results):
    """helper function to print results consistently"""
    print(f"\n=== {title} ===")
    if "accuracy" in results:  #ml results
        print(f"accuracy: {results['accuracy']:.2%}")
        print(f"precision: {results['precision']:.2%}")
        print(f"recall: {results['recall']:.2%}")
    else:  #traffic system results
        print(f"lane 1: {results['lane1_wait']}s wait, {results['lane1_cars']} cars")
        print(f"lane 2: {results['lane2_wait']}s wait, {results['lane2_cars']} cars")
        total_wait = results['lane1_wait'] + results['lane2_wait']
        total_cars = results['lane1_cars'] + results['lane2_cars']
        print(f"total: {total_wait}s wait, {total_cars} cars")

#main execution
if __name__ == "__main__":
    #run timer system
    timer = TimerSystem()
    timer_results = timer.simulate()
    print_results("timer system results", timer_results)
    
    #run ai system
    ai = AISystem()
    ai_results = ai.simulate()
    print_results("ai system results", ai_results)
    
    #compare efficiency
    timer_total = timer_results['lane1_wait'] + timer_results['lane2_wait']
    ai_total = ai_results['lane1_wait'] + ai_results['lane2_wait']
    improvement = (timer_total - ai_total) / timer_total * 100
    print(f"\nwait time improvement: {improvement:.1f}%")
    
    #run ml prediction
    ml_results = run_machine_learning()
    print_results("ml traffic prediction", ml_results)
    print("predictions saved to 'traffic_predictions.csv'")
