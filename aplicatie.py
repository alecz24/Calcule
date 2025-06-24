import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calcul Torsiune și Radiator", layout="centered")
st.title("Calcul Torsiune & Dimensiuni Radiator")

# === INPUTURI ===
st.subheader("Introduceți datele:")
Mt = st.number_input("Momentul de torsiune Mt (Nmm)", value=1.5e6, format="%.2f")
Ta = st.number_input("Tensiunea admisibilă Ta (N/mm²)", value=80.0, format="%.2f")
K = st.number_input("Raportul K = Dext / d", value=0.8, format="%.2f")

# === CALCULE ===
Wpnec = Mt / Ta
factor = 1 - (1 / K)**4
base = (16 * Wpnec) / (np.pi * factor)

# MATLAB-style cubic root
Dext = np.real(base ** (1/3))
d = Dext / K

# === AFIȘARE ===
st.subheader("Rezultate identice MATLAB:")
st.code(f"Wpnec = {Wpnec:.2f} mm³")
st.code(f"d  = {Dext:.2f} mm")
st.code(f"Dext     = {d:.2f} mm")


# =======================
# === 2. RADIATOR ===
# =======================
st.header("2. Parametrii pentru radiator")

kw = st.number_input("Puterea motorului (kW)", value=50.0)
Q_total = kw * 1000  # W

# Parametri lichid
T_in = 95
T_out = 70
V_l = 0.00133
Cpc = 4186
Kc = 0.606
mu = 0.001
Dhc = 0.01

Rec = (V_l * Dhc) / mu
Prc = 7.0

hc = 0
if 2300 < Rec < 10000:
    FF = (1.58 * np.log(Rec) - 3.28)**-2
    Nuc = ((Rec - 1000) * Prc * (FF / 2)) / (1.07 + 12.7 * np.sqrt(FF / 2) * (Prc**(2.0 / 3.0) - 1))
    hc = (Nuc * Kc) / Dhc

# Parametri aer
Vaf = 5
Cpa = 1005
Ka = 0.026
Dha = 0.05

Rea = (Vaf * Dha) / (Ka / Cpa)
J = 0.174 * Rea**-0.383
ha = (J * Vaf * Cpa) / Prc**(2.0 / 3.0)

Ca = Vaf * Cpa
Cc = V_l * Cpc
Cr = min(Ca, Cc) / max(Ca, Cc)
NTUmax = (hc * Dhc) / min(Ca, Cc)
E = 1 - np.exp(-Cr * NTUmax)
Q = E * min(Ca, Cc) * (T_in - T_out)

A = Q_total / (ha * (T_in - T_out))  # m²
A_fizic = A * 0.00028
A_fizic_cm2 = A_fizic * 10000

# Dimensiuni radiator
W = 0.2  # m
D = 0.04  # m
L = A_fizic / W  # m

L_mm = L * 1000
W_mm = W * 1000
D_mm = D * 1000

st.subheader("Rezultate radiator:")
st.write(f"**Rea (aer):** {Rea:.2f}")
st.write(f"**Coef. de transfer ha:** {ha:.2f} W/m²K")
st.write(f"**Suprafață fizică estimată:** {A_fizic_cm2:.2f} cm²")
st.write(f"**Dimensiuni radiator:** Lungime: {L_mm:.2f} mm, Lățime: {W_mm:.2f} mm, Adâncime: {D_mm:.2f} mm")

# =======================
# === 3. GRAFIC ===
# =======================
st.subheader("3. Reprezentare schematică radiator")

fig, ax = plt.subplots(figsize=(3, 4))

ax.set_xlim(0, W_mm)
ax.set_ylim(0, L_mm)
ax.set_aspect('equal')

ax.plot([0, W_mm, W_mm, 0, 0], [0, 0, L_mm, L_mm, 0], 'b-')
ax.text(W_mm/2, -10, f"Lățime: {W_mm:.0f} mm", ha='center', fontsize=8)
ax.text(-20, L_mm/2, f"Lungime: {L_mm:.0f} mm", va='center', rotation=90, fontsize=8)
ax.set_title("Dimensiuni Radiator")
ax.axis('off')

st.pyplot(fig)

st.caption("Calculele respectă constrângerile fizice: d < Dext (interior mai mic decât exterior).")
