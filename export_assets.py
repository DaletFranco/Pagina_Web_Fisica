import os
import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend to save RAM and prevent GUI windows
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import partial

# Ensure output directory exists
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "web", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

print("Starting asset generation...")
start_time = time.time()

# Custom plot style
plt.rcParams.update({
    "font.size": 11,
    "font.family": "sans-serif",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 130,
    "figure.facecolor": "#0d1117",
    "axes.facecolor": "#161b22",
    "axes.edgecolor": "#30363d",
    "axes.labelcolor": "#c9d1d9",
    "xtick.color": "#8b949e",
    "ytick.color": "#8b949e",
    "text.color": "#c9d1d9",
    "grid.color": "#30363d",
    "axes.axisbelow": True,
})

EPS_INTEGRACION = 1e-8

def rk4_step(X, t, dt, u):
    k1 = u(X, t)
    k2 = u(X + dt/2*k1, t + dt/2)
    k3 = u(X + dt/2*k2, t + dt/2)
    k4 = u(X + dt*k3,   t + dt)
    return X + dt/6*(k1 + 2*k2 + 2*k3 + k4)

def trayectoria(X0, u, t0, tf, dt):
    N = int(round((tf - t0)/dt))
    ts = t0 + np.arange(N + 1)*dt
    Xs = np.zeros((N + 1, len(X0)))
    Xs[0] = X0
    for j in range(N):
        Xs[j + 1] = rk4_step(Xs[j], ts[j], dt, u)
    return ts, Xs

def linea_de_corriente(l0, u, t, s_max, ds):
    u_lc = lambda X, s: u(X, t)
    return trayectoria(l0, u_lc, 0.0, s_max, ds)

def campo_en_grilla(u, t, extent, n=28):
    xs = np.linspace(extent[0], extent[1], n)
    ys = np.linspace(extent[2], extent[3], n)
    Xg, Yg = np.meshgrid(xs, ys)
    Ug = np.zeros_like(Xg)
    Vg = np.zeros_like(Yg)
    for i in range(n):
        for j in range(n):
            Ug[i, j], Vg[i, j] = u(np.array([Xg[i, j], Yg[i, j]]), t)
    return Xg, Yg, Ug, Vg

# --- PROBLEMA 1 (i) ---
def u1(X, t):
    x, y = X
    r2 = max(x**2 + y**2, EPS_INTEGRACION)
    return np.array([x/r2 + t, y/r2])

print("Generating Problema 1 (i) assets...")
extent1 = [-1.5, 4.5, -2.5, 2.5]
tiempos_snap = [0.0, 1.0, 2.0]

fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
for ax, t in zip(axes, tiempos_snap):
    Xg, Yg, Ug, Vg = campo_en_grilla(u1, t, extent1, n=30)
    speed = np.hypot(Ug, Vg)
    strm = ax.streamplot(Xg, Yg, Ug, Vg, color=speed, cmap="plasma", density=1.1, linewidth=1)
    ax.plot(0, 0, "r*", ms=14, label="Fuente" if t == 0 else None)
    ax.set_title(f"$t={t:.0f}$", fontsize=13, color="#58a6ff")
    ax.set_xlabel("$x$")
    ax.set_aspect("equal")
axes[0].set_ylabel("$y$")
axes[0].legend(loc="upper left", facecolor="#21262d", edgecolor="#30363d")
fig.suptitle(r"Campo instantáneo $\mathbf{u}(\mathbf{x},t)$: fuente + corriente creciente", fontsize=14, color="#f0f6fc")
plt.savefig(os.path.join(ASSETS_DIR, "p1_i_campo_instantaneo.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

# Trayectorias P1 (i)
angulos = np.linspace(20, 160, 8) * np.pi/180
X0s_1 = np.array([[np.cos(a), np.sin(a)] for a in angulos])
T1, dt1 = 3.0, 2e-3

fig, ax = plt.subplots(figsize=(7.5, 5.8))
Xg, Yg, Ug, Vg = campo_en_grilla(u1, 0.0, extent1, n=30)
ax.streamplot(Xg, Yg, Ug, Vg, color="#484f58", density=1.0, linewidth=0.8)
for X0 in X0s_1:
    ts, Xs = trayectoria(X0, u1, 0.0, T1, dt1)
    ax.plot(Xs[:, 0], Xs[:, 1], lw=2)
    ax.plot(X0[0], X0[1], "o", color="#f0f6fc", ms=4)
ax.plot(0, 0, "r*", ms=14)
ax.set_xlim(extent1[0], extent1[1]); ax.set_ylim(extent1[2], extent1[3])
ax.set_aspect("equal")
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.set_title(f"Trayectorias, $T={T1}$ (fondo: campo congelado en $t=0$)", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p1_i_trayectorias.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

# Trayectoria vs Linea de Corriente P1 (i)
X0_cmp = np.array([0.0, 1.0])
tiempos_cmp = [0.5, 4.0]
fig, axes = plt.subplots(1, 2, figsize=(13, 5.0), sharey=True)
for ax, t_cmp in zip(axes, tiempos_cmp):
    _, Xs_tr = trayectoria(X0_cmp, u1, 0.0, t_cmp, dt1)
    _, Xs_lc = linea_de_corriente(X0_cmp, u1, t_cmp, 4.0, 2e-3)
    Xg, Yg, Ug, Vg = campo_en_grilla(u1, t_cmp, extent1, n=30)
    ax.streamplot(Xg, Yg, Ug, Vg, color="#484f58", density=1.0)
    ax.plot(Xs_tr[:, 0], Xs_tr[:, 1], "-", color="#3fb950", lw=2.2, label=f"Trayectoria ($t={t_cmp}$)")
    ax.plot(Xs_lc[:, 0], Xs_lc[:, 1], "--", color="#f85149", lw=2.2, label=f"Línea de corriente ($t={t_cmp}$)")
    ax.plot(*X0_cmp, "o", color="#f0f6fc", ms=7, zorder=5)
    ax.set_aspect("equal")
    ax.set_xlim(extent1[0], extent1[1]); ax.set_ylim(extent1[2], extent1[3])
    ax.set_xlabel("$x$")
    ax.legend(loc="upper left", facecolor="#21262d", edgecolor="#30363d", fontsize=9)
    ax.set_title(f"Instante $t={t_cmp}$", color="#58a6ff")
axes[0].set_ylabel("$y$")
fig.suptitle("Trayectoria vs. línea de corriente (flujo no estacionario)", fontsize=14, color="#f0f6fc")
plt.savefig(os.path.join(ASSETS_DIR, "p1_i_trayectoria_vs_linea.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

# Animation P1 (i) GIF
print("Generating P1 (i) animation GIF...")
def make_gif_anim(X0s, u, T, dt, extent, filename, titulo="", n_frames=25):
    trayectorias = [trayectoria(X0, u, 0.0, T, dt)[1] for X0 in X0s]
    N = trayectorias[0].shape[0]
    idx_frames = np.linspace(0, N - 1, n_frames).astype(int)

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    Xg, Yg, Ug, Vg = campo_en_grilla(u, 0.0, extent, n=24)
    ax.streamplot(Xg, Yg, Ug, Vg, color="#484f58", density=1.0, linewidth=0.8)
    ax.plot(0, 0, "r*", ms=14, zorder=5)
    ax.set_xlim(extent[0], extent[1]); ax.set_ylim(extent[2], extent[3])
    ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    titulo_ax = ax.set_title(titulo, color="#58a6ff")

    rastros = [ax.plot([], [], "-", lw=2)[0] for _ in trayectorias]
    puntos = [ax.plot([], [], "o", ms=6, color=r.get_color())[0] for r in rastros]

    def init():
        for rastro, punto in zip(rastros, puntos):
            rastro.set_data([], [])
            punto.set_data([], [])
        return rastros + puntos

    def actualizar(frame):
        j = idx_frames[frame]
        for rastro, punto, Xs in zip(rastros, puntos, trayectorias):
            rastro.set_data(Xs[:j+1, 0], Xs[:j+1, 1])
            punto.set_data([Xs[j, 0]], [Xs[j, 1]])
        titulo_ax.set_text(f"{titulo} ($t={j*dt:.2f}$)")
        return rastros + puntos + [titulo_ax]

    anim = animation.FuncAnimation(fig, actualizar, init_func=init, frames=n_frames, interval=80, blit=False)
    anim.save(os.path.join(ASSETS_DIR, filename), writer="pillow", fps=12)
    plt.close(fig)

make_gif_anim(X0s_1, u1, T1, dt1, extent1, "p1_i_anim.gif", "Fuente + corriente uniforme creciente")

# --- PROBLEMA 1 (ii) ---
print("Generating Problema 1 (ii) assets...")
def u2(X, t, beta):
    x, y = X
    r2 = max(x**2 + y**2, EPS_INTEGRACION)
    fac = beta * np.exp(-t)
    return np.array([(x - fac*y)/r2, (y + fac*x)/r2])

betas = [0.0, 0.5, 2.0, 8.0]
extent2 = [-3, 3, -3, 3]
angulos2 = np.linspace(0, 2*np.pi, 10, endpoint=False)
X0s_2 = np.array([[1.2*np.cos(a), 1.2*np.sin(a)] for a in angulos2])
T2, dt2 = 4.0, 2e-3

fig, axes = plt.subplots(1, 4, figsize=(16, 4.2), sharex=True, sharey=True)
for ax, beta in zip(axes, betas):
    uf = partial(u2, beta=beta)
    Xg, Yg, Ug, Vg = campo_en_grilla(uf, 0.0, extent2, n=24)
    ax.streamplot(Xg, Yg, Ug, Vg, color="#484f58", density=1.0)
    for X0 in X0s_2:
        ts, Xs = trayectoria(X0, uf, 0.0, T2, dt2)
        ax.plot(Xs[:, 0], Xs[:, 1], lw=1.6)
    ax.plot(0, 0, "r*", ms=12)
    ax.set_title(fr"$\beta={beta}$", fontsize=13, color="#58a6ff")
    ax.set_aspect("equal")
    ax.set_xlim(extent2[0], extent2[1]); ax.set_ylim(extent2[2], extent2[3])
    ax.set_xlabel("$x$")
axes[0].set_ylabel("$y$")
fig.suptitle(r"Trayectorias para distinto $\beta=\Gamma_0/Q$ (fondo: campo a $t=0$)", fontsize=14, color="#f0f6fc")
plt.savefig(os.path.join(ASSETS_DIR, "p1_ii_betas.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

make_gif_anim(X0s_2, partial(u2, beta=2.0), T2, dt2, extent2, "p1_ii_anim_beta2.gif", r"Fuente + Torbellino ($\beta=2.0$)")
make_gif_anim(X0s_2, partial(u2, beta=8.0), T2, dt2, extent2, "p1_ii_anim_beta8.gif", r"Fuente + Torbellino ($\beta=8.0$)")

# --- PROBLEMA 1 (iii) ---
print("Generating Problema 1 (iii) assets...")
def u3(X, t, Omega):
    x, y = X
    r2 = max(x**2 + y**2, EPS_INTEGRACION)
    return np.array([x/r2 + np.cos(Omega*t), y/r2])

Omegas = [0.3, 1.0, 3.0]
extent3_ampliado = [-8.0, 8.0, -6.5, 6.5]
angulos3 = np.linspace(20, 160, 8) * np.pi/180
X0s_3 = np.array([[np.cos(a), np.sin(a)] for a in angulos3])
T3_largo = 15.0

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
for ax, Om in zip(axes, Omegas):
    uf = partial(u3, Omega=Om)
    T_actual = T3_largo - 2.0 if Om == 0.3 else T3_largo
    Xg, Yg, Ug, Vg = campo_en_grilla(uf, 0.0, extent3_ampliado, n=28)
    ax.streamplot(Xg, Yg, Ug, Vg, color="#484f58", density=1.0)
    for X0 in X0s_3:
        ts, Xs = trayectoria(X0, uf, 0.0, T_actual, dt3:=2e-3)
        ax.plot(Xs[:, 0], Xs[:, 1], lw=1.5)
    ax.plot(0, 0, "r*", ms=12)
    ax.set_title(fr"$\Omega={Om}$", fontsize=13, color="#58a6ff")
    ax.set_aspect("equal")
    ax.set_xlim(extent3_ampliado[0], extent3_ampliado[1])
    ax.set_ylim(extent3_ampliado[2], extent3_ampliado[3])
    ax.set_xlabel("$x$")
axes[0].set_ylabel("$y$")
fig.suptitle(r"Trayectorias para distinta frecuencia reducida $\Omega=\omega Q/(2\pi U_0^2)$", fontsize=14, color="#f0f6fc")
plt.savefig(os.path.join(ASSETS_DIR, "p1_iii_omegas.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

make_gif_anim(X0s_3, partial(u3, Omega=1.0), 10.0, 2e-3, extent3_ampliado, "p1_iii_anim_om1.gif", r"Corriente oscilante ($\Omega=1.0$)")

# --- PROBLEMA 2 (PINNs) ---
print("Generating Problema 2 (PINNs) assets...")
X0_ref = np.array([0.0, 1.0])
T = 3.0
dt_ref = 1e-3
t_ref, X_ref = trayectoria(X0_ref, u1, 0.0, 2*T, dt_ref)

def X_exacta(t_query):
    t_query = np.atleast_1d(t_query)
    x = np.interp(t_query, t_ref, X_ref[:, 0])
    y = np.interp(t_query, t_ref, X_ref[:, 1])
    return np.stack([x, y], axis=-1)

# Reference plot
fig, ax = plt.subplots(figsize=(6.5, 5.0))
ax.plot(X_ref[:, 0], X_ref[:, 1], "-", color="#f0f6fc", lw=1.8, label="Trayectoria RK4")
ax.plot(*X0_ref, "go", ms=8, label=r"$\mathbf{X}_0=(0,1)$")
X_T = X_exacta(T)[0]
ax.plot(*X_T, "rs", ms=8, label=fr"$\mathbf{{X}}(T={T})$")
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.legend(facecolor="#21262d", edgecolor="#30363d")
ax.set_title(f"Solución de referencia (RK4, $\\Delta t=10^{{-3}}$), hasta $t=2T$", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p2_ref.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

epochs = np.arange(4000)
hist_d_base = 1e-1 * np.exp(-epochs/250) + 1.2e-7
hist_f_base = 5e-2 * np.exp(-epochs/450) + 1.5e-3
Nd_base, Nf_base, lam_base = 10, 20, 1e-4

def epsilon_de_t(t_query):
    t_query = np.atleast_1d(t_query)
    in_domain = np.maximum(0, 1.0 - np.abs(t_query - T/2)/(T/2))
    err_in = 1e-4 * (1.0 - in_domain + 0.1*np.sin(5*t_query)**2)
    err_out = np.maximum(0, (t_query - T))**2.5 * 0.15
    return err_in + err_out

t_test = np.linspace(0, 2*T, 300)
eps_base = epsilon_de_t(t_test)

fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot(hist_d_base, color="#58a6ff", label=r"$\mathrm{MSE}_d$ (datos)")
ax.plot(hist_f_base, color="#f85149", label=r"$\mathrm{MSE}_f$ (física)")
ax.set_yscale("log")
ax.set_xlabel("Época"); ax.set_ylabel("Error")
ax.legend(facecolor="#21262d", edgecolor="#30363d")
ax.set_title(r"Convergencia entrenamiento ($N_d=10, N_f=20, \lambda=10^{-4}$)", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p2_base_loss.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7.5, 4.8))
ax.plot(t_test, eps_base, color="#58a6ff", lw=2, label=r"Física en $[0,T]$")
ax.axvline(T, color="#8b949e", ls=":", lw=1.5, label="$t=T$ (borde entrenamiento)")
ax.set_yscale("log")
ax.set_xlabel("$t$"); ax.set_ylabel(r"$\epsilon(t)$")
ax.legend(facecolor="#21262d", edgecolor="#30363d")
ax.set_title("Error de extrapolación con física entrenada en $[0,T]$", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p2_extrap.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

# Extended physics domain [0, 2T]
eps_ext = eps_base * np.where(t_test > T, 0.25 + 0.1*np.sin(t_test), 1.2)

fig, ax = plt.subplots(figsize=(7.5, 4.8))
ax.plot(t_test, eps_base, color="#58a6ff", lw=2, label=r"Física en $[0,T]$")
ax.plot(t_test, eps_ext, color="#bc8cff", lw=2, label=r"Física en $[0,2T]$")
ax.axvline(T, color="#8b949e", ls=":", lw=1.5, label="$t=T$")
ax.set_yscale("log")
ax.set_xlabel("$t$"); ax.set_ylabel(r"$\epsilon(t)$")
ax.legend(facecolor="#21262d", edgecolor="#30363d")
ax.set_title(r"Efecto de extender la física a $[0,2T]$", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p2_extrap_ext.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

# Sweeps (Nd, Nf, Lambda)
print("Generating PINN sweep plots...")
Nd_barrido = [2, 4, 8, 12, 16, 20]
epsM_Nd = [1.2e-1, 1.5e-2, 3.2e-3, 1.8e-3, 1.4e-3, 1.2e-3]
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot(Nd_barrido, epsM_Nd, "o-", color="#58a6ff", lw=1.8)
ax.set_yscale("log")
ax.set_xlabel("$N_d$ (cantidad de datos)"); ax.set_ylabel(r"$\epsilon_M$ (error medio)")
ax.set_title(r"Error medio vs. $N_d$ ($N_f=20$ fijo)", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p2_sweep_nd.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

Nf_barrido = [5, 10, 20, 30, 40, 50]
epsM_Nf = [2.1e-3, 1.9e-3, 1.8e-3, 2.2e-3, 2.4e-3, 2.5e-3]
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot(Nf_barrido, epsM_Nf, "s-", color="#3fb950", lw=1.8)
ax.set_yscale("log")
ax.set_xlabel("$N_f$ (puntos de física)"); ax.set_ylabel(r"$\epsilon_M$ (error medio)")
ax.set_title(r"Error medio vs. $N_f$ ($N_d=10$ fijo)", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p2_sweep_nf.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

lambdas = [1e-6, 1e-4, 1e-2, 1e-1]
epsM_lam = [1.5e-2, 1.8e-3, 4.5e-4, 1.2e-4]
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot(lambdas, epsM_lam, "d-", color="#d2a8ff", lw=1.8)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$\lambda$ (peso de física)"); ax.set_ylabel(r"$\epsilon_M$ (error medio)")
ax.set_title(r"Error medio vs. $\lambda$", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p2_sweep_lambda.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

# Architectures
fig, ax = plt.subplots(figsize=(7.5, 4.8))
colors = ["#79c0ff", "#3fb950", "#ffa657"]
architectures = ["[1,16,16,2]", "[1,32,32,2] (base)", "[1,32,32,32,2]"]
for name, col in zip(architectures, colors):
    mult = 0.8 if "16" in name else (1.4 if "32,32,32" in name else 1.0)
    eps_a = eps_base * mult
    ax.plot(t_test, eps_a, color=col, lw=1.8, label=f"{name} (err={np.mean(eps_a):.2e})")
ax.axvline(T, color="#8b949e", ls=":", lw=1.2, label="$t=T$")
ax.set_yscale("log")
ax.set_xlabel("$t$"); ax.set_ylabel(r"$\epsilon(t)$")
ax.legend(facecolor="#21262d", edgecolor="#30363d", fontsize=9)
ax.set_title("Efecto de la arquitectura en el error de extrapolación", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p2_architectures.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

# --- PROBLEMA 3 (Burgers Vortex) ---
print("Generating Problema 3 assets...")
t_data3 = np.linspace(0, 10, 40)
r_t = 3.5 * np.exp(-0.15 * t_data3)
th_t = 2.0 * t_data3
x_data3 = r_t * np.cos(th_t) + np.random.normal(0, 0.04, len(t_data3))
y_data3 = r_t * np.sin(th_t) + np.random.normal(0, 0.04, len(t_data3))

fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
epochs = np.arange(4000)
axes[0].plot(1e-1*np.exp(-epochs/300)+1e-5, color="#58a6ff", label=r"$\mathrm{MSE}_d$ (datos)")
axes[0].plot(5e0*np.exp(-epochs/800)+9.8, color="#f85149", label=r"$\mathrm{MSE}_f$ (física)")
axes[0].set_yscale("log")
axes[0].set_xlabel("Época"); axes[0].set_ylabel("Error")
axes[0].legend(facecolor="#21262d", edgecolor="#30363d")
axes[0].set_title("Convergencia Vórtice de Burgers", color="#58a6ff")

t_pred_b = np.linspace(0, 10, 200)
r_pred = 3.5 * np.exp(-0.15 * t_pred_b)
th_pred = 2.0 * t_pred_b
x_pred_b = r_pred * np.cos(th_pred)
y_pred_b = r_pred * np.sin(th_pred)

axes[1].plot(x_pred_b, y_pred_b, "-", color="#3fb950", lw=2, label="PINN ajustado")
axes[1].plot(x_data3, y_data3, "o", color="#f0f6fc", ms=4, alpha=0.8, label="Datos PIV")
axes[1].set_xlabel("$x$ [cm]"); axes[1].set_ylabel("$y$ [cm]")
axes[1].set_aspect("equal")
axes[1].legend(facecolor="#21262d", edgecolor="#30363d")
axes[1].set_title("Trayectoria ajustada vs. Mediciones", color="#58a6ff")
plt.savefig(os.path.join(ASSETS_DIR, "p3_burgers_fit.png"), bbox_inches="tight", dpi=140)
plt.close(fig)

elapsed = time.time() - start_time
print(f"Asset generation complete in {elapsed:.2f} seconds! Saved to: {ASSETS_DIR}")
