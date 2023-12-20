import numpy as np
from scipy.spatial.distance import cdist
rng = np.random.default_rng()

class Community():
    def __init__(self, virus_obj):
        """
        Initialise the community. Requires an object modelling a viral disease.
        """
        self.__virus = virus_obj
        self.__agents = []

        # Keep track of stats internally
        self.num = 0
        self.count = {}
        self.count["H"] = 0
        self.count["S"] = 0
        self.count["A"] = 0
        self.count["P"] = 0
        self.count["D"] = 0

    # Getter methods for private instance variables
    @property
    def agents(self):
        return self.__agents

    @property
    def virus(self):
        return self.__virus

    def add_agents(self, obj, state, count=1):
        """
        Adds a specified number of new agents with the specified state to the community
        """
        for _ in range(count):
            xval = rng.uniform(0,1)
            yval = rng.uniform(0,1)
            self.__agents.append(obj(xval, yval, state))
            self.num += 1
            if state == "H": self.count["H"] += 1
            if state == "S": self.count["S"] += 1
            if state == "A": self.count["A"] += 1
            if state == "P": self.count["P"] += 1
            if state == "D": self.count["D"] += 1

    def get_xy(self, state, quarantine):
        """
        Returns an array of locations of the agents with the specified state and
        quarantine status
        """
        bucket = np.array([a.p for a in self.__agents if ((a.state == state) and (a.quarantine == quarantine))])
        if len(bucket) == 0:
            return np.array([]), np.array([])
        x, y = bucket.T
        return x, y

    def sim_counter(self, max_steps=1200):
        """
        Generator that keeps running until the community can no longer evolve further
        because there are no more infected agents. Used when running the simulation in
        matplotlib
        """
        n = 0
        while (self.count["S"] + self.count["A"]) > 0:
            yield n + 1
            n += 1
            if n == max_steps:
                break
        yield n + 1

    def evolve(self):
        """
        Evolves the community at each simulation step
        """
        if self.__virus.QUARANTINE_DELAY >= 0:
            for a in self.__agents:
                if (a.state == "S") and (a.quarantine is False):
                    if a.days_infected >= self.__virus.QUARANTINE_DELAY:
                        a.set_quarantine(True)

        # (S/A) to (D/P):
        curr_inf_all = [a for a in self.__agents if a.state in ("A", "S")]
        if len(curr_inf_all) == 0:
            self.count["S"], self.count["A"] = 0, 0
            return
        
        for a in curr_inf_all:
            a.days_infected += 1
            if a.days_infected >= self.__virus.MAX_SICK_DAYS:
                self.count[a.state] -= 1
                if rng.uniform(0,1) < self.__virus.DEATH_PROB:
                    a.set_state("D")
                    self.count["D"] += 1
                else:
                    a.set_state("P")
                    self.count["P"] += 1

        # H to (S/A):
        curr_inf, curr_sus = [], []
        curr_inf_loc, curr_sus_loc = [], []
        for a in self.__agents:
            if a.quarantine is False:
                if (a.state in ("A", "S")):
                    curr_inf.append(a)
                    curr_inf_loc.append(a.p)
                elif (a.state == "H"):
                    curr_sus.append(a)
                    curr_sus_loc.append(a.p)

        if (len(curr_sus) > 0) and (len(curr_inf) > 0):
            res = cdist(curr_sus_loc, curr_inf_loc, metric="sqeuclidean")
            res = np.argwhere(res < self.__virus.INFECTION_RADIUS)
            for pt in res:
                if rng.uniform(0,1) < self.__virus.TRANSMISSION_PROB:
                    self.count["H"] -= 1
                    if rng.uniform(0,1) < self.__virus.SYMPTOMS_PROB:
                        curr_sus[pt[0]].set_state("S")
                        self.count["S"] += 1
                    else:
                        curr_sus[pt[0]].set_state("A")
                        self.count["A"] += 1

        for a in self.__agents:
            a.move()
