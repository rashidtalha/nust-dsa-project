import numpy as np
from scipy.spatial.distance import cdist
rng = np.random.default_rng()

class Community():
    def __init__(self, virus_obj):
        self.virus = virus_obj
        self.agents = []

        self.num = 0
        self.count = {}
        self.count["H"] = 0
        self.count["S"] = 0
        self.count["A"] = 0
        self.count["P"] = 0
        self.count["D"] = 0

    def add_agents(self, obj, state, count=1):
        for _ in range(count):
            xval = rng.uniform(0,1)
            yval = rng.uniform(0,1)
            self.agents.append(obj(xval, yval, state))
            self.num += 1
            if state == "H": self.count["H"] += 1
            if state == "S": self.count["S"] += 1
            if state == "A": self.count["A"] += 1
            if state == "P": self.count["P"] += 1
            if state == "D": self.count["D"] += 1

    def get_xy(self, state, quarantine):
        bucket = np.array([a.p for a in self.agents if ((a.state == state) and (a.quarantine == quarantine))])
        if len(bucket) == 0:
            return np.array([]), np.array([])
        x, y = bucket.T
        return x, y

    def sim_counter(self, max_steps=800):
        n = 0
        while (self.count["S"] + self.count["A"]) > 0:
            yield n + 1
            n += 1
            if n == max_steps:
                break
        yield n + 1

    def evolve(self):
        if self.virus.QUARANTINE_DELAY >= 0:
            for a in self.agents:
                if (a.state == "S") and (a.quarantine is False):
                    if a.days_infected >= self.virus.QUARANTINE_DELAY:
                        a.set_quarantine(True)

        # (S/A) to (D/P):
        curr_inf_all = [a for a in self.agents if a.state in ("A", "S")]
        if len(curr_inf_all) == 0:
            self.count["S"], self.count["A"] = 0, 0
            return
        
        for a in curr_inf_all:
            a.days_infected += 1
            if a.days_infected >= self.virus.MAX_SICK_DAYS:
                self.count[a.state] -= 1
                if rng.uniform(0,1) < self.virus.DEATH_PROB:
                    a.set_state("D")
                    self.count["D"] += 1
                else:
                    a.set_state("P")
                    self.count["P"] += 1

        # H to (S/A):
        curr_inf, curr_sus = [], []
        curr_inf_loc, curr_sus_loc = [], []
        for a in self.agents:
            if a.quarantine is False:
                if (a.state in ("A", "S")):
                    curr_inf.append(a)
                    curr_inf_loc.append(a.p)
                elif (a.state == "H"):
                    curr_sus.append(a)
                    curr_sus_loc.append(a.p)

        if (len(curr_sus) > 0) and (len(curr_inf) > 0):
            res = cdist(curr_sus_loc, curr_inf_loc, metric="sqeuclidean")
            res = np.argwhere(res < self.virus.INFECTION_RADIUS)
            for pt in res:
                if rng.uniform(0,1) < self.virus.TRANSMISSION_PROB:
                    self.count["H"] -= 1
                    if rng.uniform(0,1) < self.virus.SYMPTOMS_PROB:
                        curr_sus[pt[0]].set_state("S")
                        self.count["S"] += 1
                    else:
                        curr_sus[pt[0]].set_state("A")
                        self.count["A"] += 1

        for a in self.agents:
            a.move()
