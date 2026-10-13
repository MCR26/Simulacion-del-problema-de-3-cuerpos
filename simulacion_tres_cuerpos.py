import numpy as np
import matplotlib
# ================================================================
# CONFIGURAR EL BACKEND INTERACTIVO
# Debe hacerse antes de importar pyplot.
# ================================================================
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter


# *************************************************************************
# Constantes
# *************************************************************************

G = 1.0
m1 = 1.0
m2 = 1.0
m3 = 1.0

eps = 1e-4  # Evita singularidades por colisiones


# *************************************************************************
# Condiciones iniciales
# Figura de ocho
# *************************************************************************

r1 = np.array([0.97000436, -0.24308753, 0.0])
r2 = np.array([-0.97000436, 0.24308753, 0.0])
r3 = np.array([0.0, 0.0, 0.0])

v1 = np.array([0.4662036850, 0.4323657300, 0.0])
v2 = np.array([0.4662036850, 0.4323657300, 0.0])
v3 = np.array([-0.93240737, -0.86473146, 0.0])


# *************************************************************************
# Otros casos de condiciones iniciales
# Descomenta uno de estos bloques si deseas probar otra configuración
# *************************************************************************


# # Euler colineal

# r1 = np.array([-1.0, 0.0, 0.0])
# r2 = np.array([0.0, 0.0, 0.0])
# r3 = np.array([1.0, 0.0, 0.0])

# v1 = np.array([0.0, 0.347111, 0.0])
# v2 = np.array([0.0, 0.0, 0.0])
# v3 = np.array([0.0, -0.347111, 0.0])




# Figura de ocho sin simetría XY

# r1 = np.array([0.97000436, -0.24308753, 0.1])
# r2 = np.array([-0.97000436, 0.24308753, -0.1])
# r3 = np.array([0.0, 0.0, 0.0])

# v1 = np.array([0.4662036850, 0.4323657300, 0.01])
# v2 = np.array([0.4662036850, 0.4323657300, -0.01])
# v3 = np.array([-0.93240737, -0.86473146, 0.0])




# Órbitas circulares

# R_orbita = 1.0
# omega = np.sqrt(3.0 / 4.0)

# r1 = np.array([R_orbita, 0.0, 0.0])
# r2 = np.array([ -0.5 * R_orbita, np.sqrt(3.0) / 2.0 * R_orbita, 0.0 ])
# r3 = np.array([ -0.5 * R_orbita, -np.sqrt(3.0) / 2.0 * R_orbita, 0.0 ])

# v1 = np.array([0.0,omega * R_orbita, 0.0])
# v2 = np.array([ -omega * R_orbita * np.sin(np.pi / 3.0), -omega * R_orbita * np.cos(np.pi / 3.0), 0.0 ])
# v3 = np.array([ omega * R_orbita * np.sin(np.pi / 3.0), -omega * R_orbita * np.cos(np.pi / 3.0), 0.0 ])



# *************************************************************************
# Tiempo y parámetros numéricos
# *************************************************************************

t0 = 0.0
tf = 20.0   #la cantidad de tiempo que se tarda en ejecutar asi como la cantidad de puntos que se calculan dependen directamente del tiempo final
h = 0.01
tol = 1e-6

hmax = h
hmin = h / 100.0


# *************************************************************************
# Inicialización
# Orden del vector:
# [r1, r2, r3, v1, v2, v3]
# *************************************************************************

y0 = np.concatenate([r1, r2, r3, v1, v2, v3])

t = t0
y = y0.copy()

T = [t]
Y = [y.copy()]


# *************************************************************************
# Derivada del sistema de tres cuerpos
# *************************************************************************

def derivative(y, G, m1, m2, m3, eps):
    
    r1 = y[0:3]
    r2 = y[3:6]
    r3 = y[6:9]
    v1 = y[9:12]
    v2 = y[12:15]
    v3 = y[15:18]

    # Aceleración del cuerpo 1
    a1 = (G*m2*(r2-r1)/(np.linalg.norm(r2-r1)**2+eps)**1.5 + G*m3*(r3 - r1)/(np.linalg.norm(r3-r1)**2+eps)**1.5)

    # Aceleración del cuerpo 2
    a2 = ( G * m1 * (r1 - r2) / (np.linalg.norm(r1 - r2)**2 + eps)**1.5 + G * m3 * (r3 - r2) / (np.linalg.norm(r3 - r2)**2 + eps)**1.5 )

    # Aceleración del cuerpo 3
    a3 = ( G * m1 * (r1 - r3) / (np.linalg.norm(r1 - r3)**2 + eps)**1.5 + G * m2 * (r2 - r3) / (np.linalg.norm(r2 - r3)**2 + eps)**1.5 )

    dydt = np.zeros(18)
    
    dydt[0:3] = v1
    dydt[3:6] = v2
    dydt[6:9] = v3

    dydt[9:12] = a1
    dydt[12:15] = a2
    dydt[15:18] = a3

    return dydt


# *************************************************************************
# Integración numérica RKF45
# *************************************************************************

print("Iniciando simulación de los tres cuerpos...")
while t < tf:
    restante = tf - t
    if restante <= max(1e-12, hmin):
        t = tf
        break
    h = min(h, restante)
    # Coeficientes de Runge-Kutta-Fehlberg 4(5)
    k1 = h * derivative(y, G, m1, m2, m3, eps)
    k2 = h * derivative(y + (1.0 / 4.0) * k1, G, m1, m2, m3, eps)
    k3 = h * derivative(y + (3.0 / 32.0) * k1 + (9.0 / 32.0) * k2, G, m1, m2, m3, eps)
    k4 = h * derivative(y + (1932.0 / 2197.0) * k1 - (7200.0 / 2197.0) * k2 + (7296.0 / 2197.0) * k3, G, m1, m2, m3, eps)
    k5 = h * derivative(y + (439.0 / 216.0) * k1 - 8.0 * k2 + (3680.0 / 513.0) * k3 - (845.0 / 4104.0) * k4, G, m1, m2, m3, eps)
    k6 = h * derivative( y - (8.0 / 27.0) * k1 + 2.0 * k2 - (3544.0 / 2565.0) * k3 + (1859.0 / 4104.0) * k4 - (11.0 / 40.0) * k5, G, m1, m2, m3, eps)

    # Solución de orden 4
    y4 = (y + (25.0 / 216.0) * k1 + (1408.0 / 2565.0) * k3 + (2197.0 / 4104.0) * k4- (1.0 / 5.0) * k5)

    # Solución de orden 5
    y5 = (y + (16.0 / 135.0) * k1 + (6656.0 / 12825.0) * k3 + (28561.0 / 56430.0) * k4 - (9.0 / 50.0) * k5 + (2.0 / 55.0) * k6)

    # Estimación del error, igual que en MATLAB
    R = np.linalg.norm(y5 - y4) / h
    if R > tol:
        if h <= hmin:
            print(
                f"No se puede cumplir tol: t={t:.17g}, "
                f"tf={tf:.17g}, restante={tf-t:.3e}, "
                f"R={R:.3e}, h={h:.3e}, hmin={hmin:.3e}"
            )
            break

        # Rechazar el paso, reducir h y volver a intentarlo.
        delta = 0.84 * (tol / max(R, 1e-10))**0.25
        h = max(hmin, delta * h)
        continue

    # Aceptar el paso
    t += h
    if np.isclose(t, tf, rtol=0.0, atol=1e-12):
        t = tf

    y = y4.copy()
    T.append(t)
    Y.append(y.copy())

    # Preparar el siguiente paso aceptado
    delta = 0.84 * (tol / max(R, 1e-10))**0.25
    h = min(hmax, max(hmin, delta * h))

    # Comprobar el tamaño mínimo del paso
    if h < hmin:
        print("Advertencia: paso muy pequeño. "
              "Terminando simulación.")
        break


# *************************************************************************
# Extraer posiciones
# *************************************************************************

T = np.array(T)
Y = np.array(Y)

r1_all = Y[:, 0:3]
r2_all = Y[:, 3:6]
r3_all = Y[:, 6:9]


def total_energy(state, G, m1, m2, m3, eps):
    """Energía total para el potencial gravitatorio suavizado de Plummer."""
    positions = (state[0:3], state[3:6], state[6:9])
    velocities = (state[9:12], state[12:15], state[15:18])
    masses = (m1, m2, m3)

    kinetic = sum(0.5 * mass * np.dot(velocity, velocity)
                  for mass, velocity in zip(masses, velocities))
    potential = 0.0
    for i in range(3):
        for j in range(i + 1, 3):
            distance_squared = np.dot(positions[j] - positions[i],
                                      positions[j] - positions[i])
            potential -= G * masses[i] * masses[j] / np.sqrt(distance_squared + eps)
    return kinetic + potential


energy = np.array([total_energy(state, G, m1, m2, m3, eps) for state in Y])
energy_drift = (energy - energy[0]) / abs(energy[0])
print(f"Energía inicial (modelo suavizado): {energy[0]:.12g}")
print(f"Deriva relativa máxima de energía: {np.max(np.abs(energy_drift)):.3e}")
print("Simulación finalizada.")
print(f"Tiempo final alcanzado: {T[-1]:.6f}")
print(f"Número de puntos calculados: {len(T)}")


# ================================================================
# CONFIGURAR LA FIGURA 3D INTERACTIVA
# ================================================================

plt.ion()
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("Órbita de interacción para 3 cuerpos (RKF45)")
ax.grid(True)

# Mantener la misma escala en los tres ejes
ax.set_box_aspect((1, 1, 1))
# Calcular límites a partir de todas las posiciones
all_positions = np.vstack(( r1_all, r2_all, r3_all ))
mins = all_positions.min(axis=0)
maxs = all_positions.max(axis=0)
center = (mins + maxs) / 2.0
radius = max( np.max(maxs - mins) / 2.0, 0.1 ) * 1.1
ax.set_xlim( center[0] - radius,center[0] + radius)
ax.set_ylim(center[1] - radius, center[1] + radius)
ax.set_zlim(center[2] - radius, center[2] + radius)

# Ángulo inicial de observación
ax.view_init(elev=25, azim=45)
# ================================================================
# DIBUJAR LOS TRES CUERPOS
# ================================================================
h1, = ax.plot( [r1_all[0, 0]], [r1_all[0, 1]], [r1_all[0, 2]],"ro", markerfacecolor="r", markersize=8, label="Cuerpo 1" )
h2, = ax.plot([r2_all[0, 0]], [r2_all[0, 1]], [r2_all[0, 2]], "go", markerfacecolor="g", markersize=8, label="Cuerpo 2")
h3, = ax.plot([r3_all[0, 0]], [r3_all[0, 1]], [r3_all[0, 2]], "bo", markerfacecolor="b", markersize=8, label="Cuerpo 3")

# ================================================================
# TRAYECTORIAS
# ================================================================

trail1, = ax.plot([], [], [], "r-", linewidth=1.0)
trail2, = ax.plot([], [], [], "g-", linewidth=1.0)
trail3, = ax.plot([], [], [], "b-", linewidth=1.0)
ax.legend(loc="upper right")

# Mostrar la ventana gráfica
plt.show(block=False)
plt.pause(0.1)

# ================================================================
# CONFIGURAR LA EXPORTACIÓN A MP4
# ================================================================

video_filename = "trayectoria_3cuerpos.mp4"
fps = 30
writer = FFMpegWriter( fps=fps, metadata={ "title": "Simulación de los tres cuerpos" }, bitrate=8000)

# ================================================================
# GENERAR LA ANIMACIÓN
# ================================================================
print("Generando animación y guardando video...")
try:
    with writer.saving(fig, video_filename, dpi=100):
        for k in range(0,len(T),10):
            # Cuerpo 1
            h1.set_data([r1_all[k, 0]],[r1_all[k, 1]])
            h1.set_3d_properties([r1_all[k, 2]])
            # Cuerpo 2
            h2.set_data([r2_all[k, 0]],[r2_all[k, 1]])
            h2.set_3d_properties([r2_all[k, 2]])
            # Cuerpo 3
            h3.set_data([r3_all[k, 0]],[r3_all[k, 1]])
            h3.set_3d_properties([r3_all[k, 2]])

            # Trayectorias recorridas
            trail1.set_data(r1_all[:k + 1, 0],r1_all[:k + 1, 1])
            trail1.set_3d_properties(r1_all[:k + 1, 2])
            trail2.set_data(r2_all[:k + 1, 0],r2_all[:k + 1, 1])
            trail2.set_3d_properties(r2_all[:k + 1, 2])
            trail3.set_data(r3_all[:k + 1, 0],r3_all[:k + 1, 1])
            trail3.set_3d_properties(r3_all[:k + 1, 2])

            # Actualizar la ventana y procesar
            # los eventos del ratón
            fig.canvas.draw_idle()
            fig.canvas.flush_events()

            # Guardar el cuadro en el video
            writer.grab_frame()

            # Mostrar el progreso
            if ((k + 1) % 100 == 0 or k == len(T) - 1):
                print(f"Generando video: "f"{k + 1}/{len(T)} cuadros",end="\r")
except Exception as error:
    print(f"\nError al generar el video: {error}")
    raise
finally:
    print(f"\nVideo guardado como: {video_filename}")
    # Mantener la ventana abierta
    # y permitir la interacción con el ratón
    plt.ioff()
    plt.show()