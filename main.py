from disease import VirusBase
from community import Community
from agent import AgentBase
from simulator import run_simulation

##############################################

# Control the disease's parameters by inheriting the base class
# See the class file for description of each parameter
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
    pass

# Set the initial number of healthy and infected (symptomatic) agents
Nh, Ns = 300, 1

##############################################

def main():
    """
    Primary entry point for the simulation script.
    """

    # Initialise the community, and introduce a virus
    c = Community(Virus("COVID"))
    
    # Include some susceptible and infected agents to the community
    c.add_agents(Person, "H", Nh)
    c.add_agents(Person, "S", Ns)

    # Start the simulation
    run_simulation(c, save_to_disk=False, fn="output")

if __name__ == '__main__':
    main()
