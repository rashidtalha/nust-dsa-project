import numpy as np
rng = np.random.default_rng()

class AgentBase():
    # Controls the maximum velocity while the agent is moving
    MAX_VELOCITY = 0.002
    # Model specific parameter. Controls how quickly the agent responds
    # to the updated sink location.
    ACC_FACTOR = 0.001
    # Number of days after which the sink location is updated. Effectively
    # controls when the agent changes direction.
    SINK_UPDATE_STEPS = 60
    
    def __init__(self, x, y, state):
        """
        Initialise the agent.

        Parameter
        ---------
        x : float
            x location of the object (0 < x < 1)
        y : float
            y location of the object (0 < y < 1)
        state : str
            One of the valid states for the agent
            H -> healthy
            S -> symptomatic
            A -> asymptomatic
            P -> perfectly immune/recovered
            D -> dead
        """

        # Position vector
        self.__p = np.array([x, y])
        # Velocity vector
        self.__v = np.array([0, 0])

        # Assigns a valid state to the agent
        self.set_state(state)
        # Controls whether the agent is in quarantine or not
        self.quarantine = False

        # Controls motion-specific data
        self.__sink_duration = 0
        self.s = self.__p
        self.update_sink()

    # Getter methods for private instance variables
    @property
    def p(self):
        return self.__p

    @property
    def v(self):
        return self.__v

    @property
    def sink_duration(self):
        return self.__sink_duration

    # Getter methods for private instance variables
    @p.setter
    def p(self, val):
        self.__p = val

    @v.setter
    def v(self, val):
        self.__v = val

    @sink_duration.setter
    def sink_duration(self, val):
        self.__sink_duration = val

    # Updates the gravitating sink point
    def update_sink(self):
        # Randomly assigns a new sink location
        # The sink can also be outside the bounds of the arena
        ang = rng.uniform(0, 2*np.pi)
        delta = rng.normal(0.3) * np.array([np.cos(ang), np.sin(ang)])
        self.s = self.__p + delta

    # Implements the mechanics of the motion of the agent
    def move(self):
        # Don't move the agent if they are dead
        if self.state == "D":
            return

        # Don't move the agent if they are in quarantine.
        # This reduces computations; the evolution of the virus is not affected.
        if self.quarantine is True:
            return

        # Moves the agent by one unit in the direction of the velocity vector
        while True:
            # Compute the distance to the sink
            dist = np.sqrt(np.sum((self.s - self.__p)**2))
            # Update the acceleration vector
            acc = self.ACC_FACTOR * (self.s - self.__p) / dist
            # Update the velocity vector
            vel = self.__v + acc
            # Check: ensure velocity is less than the maximum allowed value
            vel = np.where(vel == 0, 0.001, vel)
            self.__v = np.where(np.abs(vel) > self.MAX_VELOCITY, self.MAX_VELOCITY * vel / np.abs(vel), vel)

            # Check: ensure that the agent doesn't move outside the bounds of the arena
            if not np.any((self.__p + self.__v < 0) | (self.__p + self.__v > 1)):
                break
            
            # Update the sink and repeat the process if the agent crosses out of the arena
            self.update_sink()
        
        # Update the position vector
        self.__p = self.__p + self.__v
        
        # Check: if enough days have passed for the sink to be update or not
        self.__sink_duration = ((self.__sink_duration + 1) % self.SINK_UPDATE_STEPS)
        if self.__sink_duration == 0:
            self.update_sink()

    def set_state(self, new_state):
        """
        Sets the state of the agent

        Parameters
        ----------
        new_state : str
            Valid health state (H/S/A/P/D)
        """
        
        self.state = new_state
        self.days_infected = 0

    def set_quarantine(self, new_state=True):
        """
        Sets the quarantine status of the agents

        Parameters
        ----------
        new_state : Bool
            True -> move to quarantine
            False -> move out of to quarantine
        """

        self.quarantine = new_state

