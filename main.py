from disease import VirusBase
from community import Community
from agent import AgentBase
from simulator import run_simulation

##############################################

class Virus(VirusBase):
    MAX_SICK_DAYS = 80
    INFECTION_RADIUS = 0.04**2
    SYMPTOMS_PROB = 0.45
    TRANSMISSION_PROB = 0.50
    QUARANTINE_DELAY = 30
    DEATH_PROB = 0.15

N, Ni = 300, 1

c = Community(Virus("COVID"))
c.add_agents(AgentBase, "H", N)
c.add_agents(AgentBase, "S", Ni)

##############################################

if __name__ == '__main__':
    run_simulation(c, save_to_disk=False, fn="output")
