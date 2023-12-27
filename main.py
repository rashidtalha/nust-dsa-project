from disease import VirusBase
from community import Community
from agent import AgentBase
from simulator import run_simulation

import sys

##############################################

# Control the disease's parameters by inheriting the base class
# See the class file for description of each parameter

    # MAX_SICK_DAYS = 80
    # INFECTION_RADIUS = 0.04**2

    # TRANSMISSION_PROB = 0.50
    # SYMPTOMS_PROB = 0.45
    # DEATH_PROB = 0.15

    # QUARANTINE_DELAY = 30

class Virus(VirusBase):
    MAX_SICK_DAYS = 80
    INFECTION_RADIUS = 0.04**2

    TRANSMISSION_PROB = 0.50
    SYMPTOMS_PROB = 0.45
    DEATH_PROB = 0.15

    QUARANTINE_DELAY = 30

# Control the agent's parameters by inheriting the base class
# See the class file for description of each parameter
class Person(AgentBase):
    # MAX_VELOCITY = 0.002
    # ACC_FACTOR = 0.001
    SINK_UPDATE_STEPS = 120
    pass

# Set the initial number of healthy and infected (symptomatic) agents
Nh, Ns = 300, 1

##############################################

def main(save_to_disk):
    """
    Primary entry point for the simulation script.
    """

    # Initialise the community, and introduce a virus
    c = Community(Virus("COVID"))
    
    # Include some susceptible and infected agents to the community
    c.add_agents(Person, "H", Nh)
    c.add_agents(Person, "S", Ns)

    # Start the simulation
    run_simulation(c, save_to_disk=save_to_disk, fn="output")

if __name__ == '__main__':
    usr = sys.argv[1:]
    if (len(usr) > 0) and (usr[0].lower() == "save"):
        main(True)
    else:
        main(False)
