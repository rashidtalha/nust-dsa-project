import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

from disease import VirusBase
from community import Community
from agent import AgentBase

class Covid(VirusBase):
    MAX_SICK_DAYS = 50
    INFECTION_RADIUS = 0.035**2
    SYMPTOMS_PROB = 0.70
    TRANSMISSION_PROB = 0.20
    QUARANTINE_DELAY = 40
    DEATH_PROB = 0.15

class Agent(AgentBase):
    SINK_UPDATE_STEPS = 30
    MAX_VELOCITY = 0.003

c = Community(Covid("COVID"))
N, Ni = 200, 1
c.add_agents(Agent, "H", N)
c.add_agents(Agent, "S", Ni)

##############################################


colour = '#f3eeea'
plt.rcParams.update({
    "figure.facecolor":  colour,
    "axes.facecolor":    colour,
    "savefig.facecolor": colour
})

fig = plt.figure(tight_layout=True, figsize=(12.3,5.5))
gs = fig.add_gridspec(nrows=4, ncols=9)

ax_sim = fig.add_subplot(gs[:, :4])
pad = 0.035
ax_sim.set(xlim=(-pad, 1 + pad), ylim=(-pad, 1 + pad), aspect=True)
ax_sim.set_yticks([])
ax_sim.set_xticks([])

ax_stack = fig.add_subplot(gs[0:2, 4:])
ax_stack.set(xlim=(0,1), ylim=(0,100))
ax_stack.axis(False)

ax_qr = fig.add_subplot(gs[3, 4])
pad = 0.035
ax_qr.set(xlim=(-pad, 1 + pad), ylim=(-pad, 1 + pad), aspect=True)
ax_qr.set_yticks([])
ax_qr.set_xticks([])

ax_info = fig.add_subplot(gs[2:, 6:])
# ax_info.set_yticks([])
# ax_info.set_xticks([])
ax_info.axis(False)

ms, mew = 4, 0.5
mec = "#000000"
gr_h, = ax_sim.plot([], [], ls="", marker="^", ms=ms, mew=mew, mec=mec, c="#44aa00")
gr_s, = ax_sim.plot([], [], ls="", marker="o", ms=ms, mew=mew, mec=mec, c="#aa0000")
gr_a, = ax_sim.plot([], [], ls="", marker="o", ms=ms, mew=mew, mec=mec, c="#ffcc00")
gr_p, = ax_sim.plot([], [], ls="", marker="o", ms=ms, mew=mew, mec=mec, c="#a793ac")
gr_d, = ax_sim.plot([], [], ls="", marker="x", ms=ms, mew=2, mec="#3d2b1f", zorder=-5)

ax_qr.text(0, 1.1, f"Quarantine", va="bottom")
qr_s, = ax_qr.plot([], [], ls="", marker="o", ms=ms, mew=mew, mec=mec, c="#aa0000")
qr_p, = ax_qr.plot([], [], ls="", marker="o", ms=ms, mew=mew, mec=mec, c="#a793ac")
qr_d, = ax_qr.plot([], [], ls="", marker="x", ms=ms, mew=2, mec="#3d2b1f", zorder=-5)

hist = {"I":[], "RI":[]}

t = ax_info.text(0.1, 0.1, f"", va="bottom")

def updater(k):
    print(c.count["S"], c.count["A"])
    gr_h.set_data(c.get_xy("H", False))
    gr_s.set_data(c.get_xy("S", False))
    gr_a.set_data(c.get_xy("A", False))
    gr_p.set_data(c.get_xy("P", False))
    gr_d.set_data(c.get_xy("D", False))

    qr_s.set_data(c.get_xy("S", True))
    qr_p.set_data(c.get_xy("P", True))
    qr_d.set_data(c.get_xy("D", True))
    
    c.evolve()

    hist["I"].append( 100 * (c.count["S"] + c.count["A"]) / c.num )
    hist["RI"].append( 100 * (c.count["S"] + c.count["A"] + c.count["P"] + c.count["D"]) / c.num )

    nth = 2
    if k%nth == 0:
        xstack = np.arange(len(hist["I"]))
        ax_stack.fill_between(xstack, 100+np.zeros_like(xstack), color="#44aa00")
        ax_stack.fill_between(xstack, hist["RI"], color="#a793ac")
        ax_stack.fill_between(xstack, hist["I"], color="#aa0000")
        ax_stack.set(xlim=(0, max(1, k-1)))
        L = k//nth
        if k%(2*nth) == 0:
            t.set_text(f"Day: {L//2}")

s = c.sim_counter()
ani = anim.FuncAnimation(fig, updater, frames=s, interval=40, repeat=False, cache_frame_data=True)
# writer = anim.FFMpegWriter(fps=1000/33)
# ani.save("output.mp4", writer=writer)

plt.show()
print("Here")
