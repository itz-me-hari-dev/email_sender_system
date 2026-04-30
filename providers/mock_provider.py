import time
import random

class MockProvider:

    def send(self, user):
        
        # simulate API delay
        time.sleep(random.uniform(0.1, 0.3))

        # simulate failure (20%)
        if random.random() < 0.2:
            raise Exception("Simulated failure")

        return "sent"