"""Figures for 'Spacetime from the least mathematics' (beginner text).
Light CPU: numpy and matplotlib only. Run from this folder: python3 make_figures.py
Writes PNG files to ../figures/. Formulas used are the ones in the text:
- boosted Coulomb profile gamma/sqrt(rho^2+gamma^2 zeta^2)
- Kerr profile along the spin axis, Balasin and Nachbagauer (1995), normalised so that
  a non-spinning mass gives -4 log(rho)
- Planck 2018 and Pantheon+ numbers from newton-check-1.md (own fit of public data).
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
out = "../figures/"
C1 = "#1f4e79"; C2 = "#c0392b"; C3 = "#2e7d32"; G = "#999999"
plt.rcParams.update({"font.size": 9})

# Fig 1: the three unit curves x^2 - k t^2 = 1
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.6))
th = np.linspace(0, 2*np.pi, 400)
s = np.linspace(-1.4, 1.4, 400)
L = 1.8
for a in ax:
    a.axhline(0, color="#dddddd", lw=0.8); a.axvline(0, color="#dddddd", lw=0.8)
    a.set_xlim(-L, L); a.set_ylim(-L, L); a.set_aspect("equal"); a.axis("off")
ax[0].plot(np.cos(th), np.sin(th), color=C1, lw=2.5)
ax[0].set_title("complex: k = -1\ncircle, rotations", fontsize=9)
for sg in (1, -1):
    ax[1].plot([sg, sg], [-L, L], color=C1, lw=2.5)
ax[1].set_title("dual: k = 0\ntwo lines, Galileo", fontsize=9)
for sg in (1, -1):
    ax[2].plot(sg*np.cosh(s), np.sinh(s), color=C1, lw=2.5)
ax[2].plot([-L, L], [-L, L], color=C2, lw=1, ls="--"); ax[2].plot([-L, L], [L, -L], color=C2, lw=1, ls="--")
ax[2].set_title("split-complex: k = +1\nhyperbola, boosts", fontsize=9)
for a in ax:
    a.text(L, -0.12, "x", fontsize=8, ha="right", color=G); a.text(0.06, L-0.1, "t", fontsize=8, color=G)
plt.tight_layout(); plt.savefig(out + "fig1_three_planes.png", dpi=200, bbox_inches="tight", pad_inches=0.1); plt.close()

# Fig 2: a boost squeezes a unit square at constant area
fig, ax = plt.subplots(1, 4, figsize=(7.2, 2.2), sharey=True)
sq = np.array([[-.5, -.5], [.5, -.5], [.5, .5], [-.5, .5]])
for a, eta in zip(ax, [0, 0.7, 1.4, 2.4]):
    # light-cone coordinates u = t-x, v = t+x ; boost: u -> e^-eta u, v -> e^eta v
    x, t = sq[:, 0], sq[:, 1]
    u, v = t-x, t+x
    u2, v2 = u*np.exp(-eta), v*np.exp(eta)
    P = np.c_[(v2-u2)/2, (v2+u2)/2]
    area = 0.5*abs(np.dot(P[:, 0], np.roll(P[:, 1], -1)) - np.dot(P[:, 1], np.roll(P[:, 0], -1)))
    a.add_patch(Polygon(P, closed=True, fc="#a9c4e0", ec=C1, lw=2))
    a.plot([-2.5, 2.5], [-2.5, 2.5], color=C2, lw=0.9, ls="--"); a.plot([-2.5, 2.5], [2.5, -2.5], color=C2, lw=0.9, ls="--")
    a.set_xlim(-2.5, 2.5); a.set_ylim(-2.5, 2.5); a.set_aspect("equal"); a.axis("off")
    a.set_title("speed %.2f c\narea %.2f" % (np.tanh(eta), area), fontsize=8.5)
plt.tight_layout(); plt.savefig(out + "fig2_squeeze.png", dpi=200); plt.close()

# Fig 3: boosted field of a mass across the line of motion becomes tall and thin
fig, ax = plt.subplots(figsize=(4.6, 2.7))
z = np.linspace(-3, 3, 1500)
for g, c in zip([1.5, 3, 10, 30], ["#9bb8d6", "#5f8fbf", C1, "#0b2540"]):
    ax.plot(z, g/np.sqrt(1 + (g*z)**2), color=c, lw=2, label="speed %.4f c" % np.sqrt(1-1/g**2))
ax.set_xlabel("distance along the direction of motion"); ax.set_ylabel("strength of the field")
ax.set_ylim(0, 31); ax.legend(frameon=False, fontsize=8)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig(out + "fig3_boosted_field.png", dpi=200); plt.close()

# Fig 4: spinning case along the axis: profile, source disk, source point
a = 1.0
rho = np.linspace(0.02, 2.2, 600)
sch = -4*np.log(rho)
b = np.sqrt(np.clip(a*a - rho**2, 0, None))
kerr = np.where(rho > a, sch, -4*np.log(a + b) + 2*b/a)
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.6), gridspec_kw={"width_ratios": [1.5, 1, 1]})
ax[0].plot(rho, sch, color=G, ls="--", lw=1.5, label="no spin")
ax[0].plot(rho, kerr, color=C1, lw=2.5, label="spin a = 1")
ax[0].axvline(a, color="#dddddd", lw=0.8)
ax[0].set_ylim(-4, 8); ax[0].set_xlabel("distance from the axis"); ax[0].set_ylabel("strength of the shock")
ax[0].legend(frameon=False, fontsize=8)
for sp in ("top", "right"): ax[0].spines[sp].set_visible(False)
ax[0].set_title("Seen from the side", fontsize=9)
ax[1].add_patch(Circle((0, 0), 1, fc="#a9c4e0", ec=C2, lw=3)); ax[1].set_xlim(-1.5, 1.5); ax[1].set_ylim(-1.5, 1.5)
ax[1].set_aspect("equal"); ax[1].axis("off"); ax[1].set_title("Pushed along the axis:\na disk with a rim", fontsize=9)
ax[2].plot([0], [0], "o", color=G, ms=4, mfc="none"); ax[2].plot([1], [0], "o", color=C2, ms=9)
ax[2].annotate("", xy=(0.93, 0), xytext=(0.07, 0), arrowprops=dict(arrowstyle="->", color=G))
ax[2].text(0.5, 0.18, "a", ha="center", color=G)
ax[2].set_xlim(-0.6, 1.6); ax[2].set_ylim(-1.5, 1.5); ax[2].set_aspect("equal"); ax[2].axis("off")
ax[2].set_title("Pushed across the axis:\none point, moved by a", fontsize=9)
plt.tight_layout(); plt.savefig(out + "fig4_spinning.png", dpi=200); plt.close()

# Fig 5: a flash of light lives on the cone
fig, ax = plt.subplots(figsize=(3.6, 3.4))
x = np.linspace(-3, 3, 10)
ax.fill_between([-3, 0, 3], [3, 0, 3], [3, 3, 3], color="#eef3f9")
ax.plot([-3, 0, 3], [3, 0, 3], color=C1, lw=2.5)
for T in (1, 2, 3):
    ax.plot([-T, T], [T, T], "o", color=C2, ms=6)
ax.plot([0], [0], "o", color="black", ms=6)
ax.text(0.12, -0.1, "flash", fontsize=8.5, va="top")
ax.text(1.0, 0.1, "not reached yet", fontsize=8, color=G, ha="left")
ax.text(-2.9, 0.15, "red dots: where the\nlight is at each time", fontsize=8, color=C2, ha="left")
ax.text(0, 2.7, "inside: dark again\n(in 3 space dimensions)", fontsize=8, color=G, ha="center", va="top")
ax.set_xlabel("space"); ax.set_ylabel("time"); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(-3, 3); ax.set_ylim(-0.6, 3.1)
plt.tight_layout(); plt.savefig(out + "fig5_cone.png", dpi=200); plt.close()

# Fig 6: the data on the sign
fig, ax = plt.subplots(figsize=(5.4, 2.4))
rows = [("Planck 2018 + BAO, flat model", -0.5334, 0.0084, C1),
        ("Pantheon+ supernovae, flat model", -0.502, 0.027, C3),
        ("Pantheon+ supernovae, no model", -0.34, 0.17, C2)]
for i, (lab, v, e, c) in enumerate(rows[::-1]):
    ax.errorbar(v, i, xerr=e, fmt="o", color=c, capsize=4, lw=2)
    ax.text(0.57, i, lab, va="center", fontsize=8.5)
ax.axvline(0, color="black", lw=1)
ax.text(0.02, 2.55, "slowing down", fontsize=8, color=G, ha="left"); ax.text(-0.02, 2.55, "speeding up", fontsize=8, color=G, ha="right")
ax.set_xlim(-0.8, 0.55); ax.set_ylim(-0.6, 2.9); ax.set_yticks([])
ax.set_xlabel("deceleration parameter q0 (one standard error)")
for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig(out + "fig6_data.png", dpi=200, bbox_inches="tight"); plt.close()
print("ok")
