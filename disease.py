class VirusBase():
    # Total duration of infection, then the status evolves
    MAX_SICK_DAYS = 50
    # Models how viral the disease is (arbitrary units normalised to 1)
    INFECTION_RADIUS = 0.02**2
    
    # Probability of catching the disease when in close proximity
    TRANSMISSION_PROB = 0.2
    # Probability of developing symptoms when infected
    SYMPTOMS_PROB = 1
    # Mortality rate (normalised between 0 and 1)
    DEATH_PROB = 0
    
    # Number of days after developing symptoms when the agent is quarantined
    QUARANTINE_DELAY = 10

    # Whether immmunity can be lost
    IMMUNITY_LOSS = False
    # Number of days after recovering when the immunity is lost
    IMMUNITY_LOSS_DELAY = -1
    
    def __init__(self, name="Generic Virus"):
        """
        Initialise the disease object
        
        Paremeters
        ----------
        name : str
            Name of the disease
        """
        
        self.__name = name

    # Getter and setter methods for the private instance variables
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val):
        self.__name = val
