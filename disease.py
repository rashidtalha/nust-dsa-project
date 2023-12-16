class VirusBase():
    MAX_SICK_DAYS = 50
    INFECTION_RADIUS = 0.02**2
    
    TRANSMISSION_PROB = 0.2
    SYMPTOMS_PROB = 1
    DEATH_PROB = 0
    
    QUARANTINE_DELAY = 10
    IMMUNITY_LOSS = False
    IMMUNITY_LOSS_DELAY = 80
    
    def __init__(self, name="Generic Virus"):
        self.name = name
