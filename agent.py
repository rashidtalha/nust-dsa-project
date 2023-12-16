import numpy as np
rng = np.random.default_rng()

class AgentBase():
    SINK_UPDATE_STEPS = 60
    MAX_VELOCITY = 0.002
    ACC_FACTOR = 0.001
    
    def __init__(self, x, y, state):
        self.p = np.array([x, y])
        self.v = np.array([0, 0])

        self.set_state(state)
        self.quarantine = False

        self.sink_duration = 0
        self.s = self.p
        self.update_sink()

    def update_sink(self):
        ang = rng.uniform(0, 2*np.pi)
        delta = rng.normal(0.3) * np.array([np.cos(ang), np.sin(ang)])
        self.s = self.p + delta

    def move(self):
        if self.state == "D":
            return

        while True:
            dist = np.sqrt(np.sum((self.s - self.p)**2))
            acc = self.ACC_FACTOR * (self.s - self.p) / dist
            vel = self.v + acc
            vel = np.where(vel == 0, 0.001, vel)
            self.v = np.where(np.abs(vel) > self.MAX_VELOCITY, self.MAX_VELOCITY * vel / np.abs(vel), vel)

            if not np.any((self.p + self.v < 0) | (self.p + self.v > 1)):
                break
            
            self.update_sink()
            
        self.p = self.p + self.v
        self.sink_duration = ((self.sink_duration + 1) % self.SINK_UPDATE_STEPS)
        if self.sink_duration == 0:
            self.update_sink()

    def set_state(self, new_state):
        self.state = new_state
        self.radius = 0
        self.days_infected = 0

    def set_quarantine(self, new_state=True):
        self.quarantine = new_state

