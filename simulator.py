import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

colour = '#e8e8e8'
plt.rcParams.update({
    "figure.facecolor":  colour,
    "axes.facecolor":    colour,
    "savefig.facecolor": colour,
    "font.family": "monospace",
    "savefig.dpi": 256
})

def run_simulation(c, save_to_disk=False, fn="output"):
    fig = plt.figure(tight_layout=True, figsize=(12,7.3))
    gs = fig.add_gridspec(nrows=4, ncols=7)
    pad = 0.035

    ##############################################

    ax_sim = fig.add_subplot(gs[:, :4])
    ax_sim.set(xlim=(-pad, 1 + pad), ylim=(-pad, 1 + pad), aspect=True)
    ax_sim.set_yticks([])
    ax_sim.set_xticks([])
    ms, mew = 6, 0.5
    mec = "#000000"
    gr_h, = ax_sim.plot([], [], ls="", marker="^", ms=ms, mew=mew, mec=mec, c="#44aa00", label="Healthy")
    gr_p, = ax_sim.plot([], [], ls="", marker="o", ms=ms, mew=mew, mec=mec, c="#a793ac", label="Recovered")
    gr_s, = ax_sim.plot([], [], ls="", marker="o", ms=ms, mew=mew, mec=mec, c="#aa0000", label="Symptomatic")
    gr_a, = ax_sim.plot([], [], ls="", marker="o", ms=ms, mew=mew, mec=mec, c="#ffcc00", label="Asymptomatic")
    gr_d, = ax_sim.plot([], [], ls="", marker="x", ms=ms, mew=2, mec="#3d2b1f", zorder=-5, label="Dead")
    ax_sim.legend(loc='upper left', bbox_to_anchor=(0, 0), ncols=3, frameon=False)

    ##############################################

    ax_qr = fig.add_subplot(gs[3, 4])
    ax_qr.set(xlim=(-pad, 1 + pad), ylim=(-pad, 1 + pad), aspect=True)
    ax_qr.set_yticks([])
    ax_qr.set_xticks([])
    ms, mew = 4, 0.5
    qr_s, = ax_qr.plot([], [], ls="", marker="o", ms=ms, mew=mew, c="#aa0000")
    qr_p, = ax_qr.plot([], [], ls="", marker="o", ms=ms, mew=mew, c="#a793ac")
    qr_d, = ax_qr.plot([], [], ls="", marker="x", ms=ms, mew=2, mec="#3d2b1f", zorder=-5)

    ##############################################

    ax_pk = fig.add_subplot(gs[3, 5:])
    ax_pk.set(xlim=(0,1), ylim=(-0.01,1))
    ax_pk.axis(False)

    ax_pk.axhline(0.00, ls="-", lw=0.5, c="#000000")
    ax_pk.axhline(0.25, ls="--", lw=0.5, c="#000000")
    ax_pk.axhline(0.50, ls="--", lw=0.5, c="#000000")
    ax_pk.axhline(0.75, ls="--", lw=0.5, c="#000000")
    ax_pk.axhline(1.00, ls="-", lw=0.5, c="#000000")
    ax_pk.text(0, 0.25+0.02, "25 %", fontsize=8)
    ax_pk.text(0, 0.50+0.02, "50 %", fontsize=8)
    ax_pk.text(0, 0.75+0.02, "75 %", fontsize=8)

    pk_e, = ax_pk.plot([], [], lw="1.5", c="#a793ac", label="Infected (Cumulative)")
    pk_i, = ax_pk.plot([], [], lw="1.5", c="#aa0000", label="Infected (Active)")
    ax_pk.legend(loc='upper left', bbox_to_anchor=(0, 0), ncols=1, frameon=False)

    ##############################################

    ax_info = fig.add_subplot(gs[:3, 4:])
    ax_info.set(xlim=(0,2), ylim=(0,2))
    ax_info.axis(False)
    ax_info.text(2, 1.85, "(Model: Stochastic SIR)", va="top", ha="right")

    t_days = ax_info.text(0, 1.85, "Day: 0", va="top")

    t_h = ax_info.text(0, 1.65, f"Healthy: {c.count['H']} ({c.count['H']/c.num:.2%})", va="top")
    t_s = ax_info.text(0, 1.55, f"Symptomatic: {c.count['S']} ({c.count['S']/c.num:.2%})", va="top")
    t_a = ax_info.text(0, 1.45, f"Asymptomatic: {c.count['A']} ({c.count['A']/c.num:.2%})", va="top")
    t_r = ax_info.text(0, 1.35, f"Recovered: {c.count['P']} ({c.count['P']/c.num:.2%})", va="top")
    t_d = ax_info.text(0, 1.25, f"Dead: {c.count['D']} ({c.count['D']/c.num:.2%})", va="top")

    t_q = ax_info.text(0, 1.05, f"Quarantined: {len([0 for a in c.agents if a.quarantine])}", va="top")

    ax_info.text(0, 0.85, f"Infection Probability: {c.virus.TRANSMISSION_PROB:.2f}", va="top")
    ax_info.text(0, 0.75, f"Asymptomatic Probability: {1-c.virus.SYMPTOMS_PROB:.2f}", va="top")
    ax_info.text(0, 0.65, f"Mortality Probability: {c.virus.DEATH_PROB:.2f}", va="top")

    ax_info.text(0, 0.55, f"Quarantine Delay: {c.virus.QUARANTINE_DELAY} days", va="top")
    ax_info.text(0, 0.45, f"Maximum Infection Duration: {c.virus.MAX_SICK_DAYS} days", va="top")
    ax_info.text(0, 0.35, f"Tranmission Radius: {c.virus.INFECTION_RADIUS:.2e}", va="top")

    ax_info.text(0, 0.15, f"Allow Immunity Loss: {c.virus.IMMUNITY_LOSS}", va="top")

    hist_infected, hist_ever = [], []

    def updater(k):
        gr_h.set_data(c.get_xy("H", False))
        gr_s.set_data(c.get_xy("S", False))
        gr_a.set_data(c.get_xy("A", False))
        gr_p.set_data(c.get_xy("P", False))
        gr_d.set_data(c.get_xy("D", False))

        qr_s.set_data(c.get_xy("S", True))
        qr_p.set_data(c.get_xy("P", True))
        qr_d.set_data(c.get_xy("D", True))

        x_pk = np.arange(len(hist_infected))
        
        pk_i.set_data(x_pk, hist_infected)
        pk_e.set_data(x_pk, hist_ever)

        ax_pk.set(xlim=(0, max(1, len(hist_infected)) ))

        hist_infected.append( (c.count["S"] + c.count["A"]) / c.num )
        hist_ever.append( (c.count["S"] + c.count["A"] + c.count["P"] + c.count["D"]) / c.num )
        
        c.evolve()

        nth = 4
        if k%nth == 0:
            L = k//nth
            t_days.set_text(f"Day: {L}")

            t_h.set_text(f"Healthy: {c.count['H']} ({c.count['H']/c.num:.2%})")
            t_s.set_text(f"Sympomatic: {c.count['S']} ({c.count['S']/c.num:.2%})")
            t_a.set_text(f"Asymptomatic: {c.count['A']} ({c.count['A']/c.num:.2%})")
            t_r.set_text(f"Recovered: {c.count['P']} ({c.count['P']/c.num:.2%})")
            t_d.set_text(f"Dead: {c.count['D']} ({c.count['D']/c.num:.2%})")
            t_q.set_text(f"Quarantined: {len([0 for a in c.agents if a.quarantine])}")

    ani = anim.FuncAnimation(fig, updater, frames=c.sim_counter, interval=33, repeat=False, cache_frame_data=False)

    if save_to_disk:
        print("Exporting to disk ...")
        writer = anim.FFMpegWriter(fps=1000/33)
        ani.save(f"{fn}.mp4", writer=writer)
        print(f"Saved to {fn}.mp4")
        return

    plt.show()
