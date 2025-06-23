import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calcul Torsiune și Radiator", layout="centered")

# Afișare logo
st.image("logo.png", width=150)

st.title("Calcul Torsiune & Dimensiuni Radiator")

# --- INPUTURI UTILIZATOR ---
st.header("1. Parametrii pentru torsiune")
Mt = st.number_input("Momentul de torsiune (Nmm)", value=1.5e6, format="%.2f")
Ta = st.number_input("Tensiunea admisibilă (N/mm²)", value=80.0)
K = st.number_input("Raportul K = d / Dext", value=0.8)

# --- CALCUL TORSIUNE ---
# factor = 1 - (d / Dext)^4 = 1 - K^4
factor = 1 - K**4
Wpnec = Mt / Ta  # mm^3
d = ((16 * Wpnec) / (np.pi * factor))**(1/3)
Dext = d / K

# Afișare rezultate torsiune
st.subheader("Rezultate torsiune:")
st.write(f"**Wpnec (modul de rezistență):** {Wpnec:.2f} mm³")
st.write(f"**Diametrul interior d:** {d:.2f} mm")
st.write(f"**Diametrul exterior Dext:** {Dext:.2f} mm")

# --- RADIATOR ---
st.header("2. Parametrii pentru radiator")
kw = st.number_input("Puterea motorului (kW)", value=50.0)
Q_total = kw * 1000  # W

# Parametri fixi
T_in = 95  # °C
T_out = 70  # °C
V_l = 0.00133  # m³/s
Cpc = 4186  # J/kgK
Kc = 0.606  # W/mK
mu = 0.001  # Pa·s
Dhc = 0.01  # m

Rec = (V_l * Dhc) / mu
Prc = 7.0

hc = 0
if 2300 < Rec < 10000:
    FF = (1.58 * np.log(Rec) - 3.28)**-2
    Nuc = ((Rec - 1000) * Prc * (FF / 2)) / (1.07 + 12.7 * np.sqrt(FF / 2) * (Prc**(2.0 / 3.0) - 1))
    hc = (Nuc * Kc) / Dhc

Vaf = 5  # m³/s
Cpa = 1005  # J/kgK
Ka = 0.026  # W/mK
Dha = 0.05  # m

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
A_fizic = A * 0.00028  # coef. de pierdere
A_fizic_cm2 = A_fizic * 10000  # cm²

# Dimensiuni radiator
W = 0.2  # m
D = 0.04  # m
L = A_fizic / W  # m

L_mm = L * 1000
W_mm = W * 1000
D_mm = D * 1000

st.subheader("Rezultate radiator:")
st.write(f"**Rea (aer):** {Rea:.2f}")
st.write(f"**Coef. de transfer aer ha:** {ha:.2f} W/m²K")
st.write(f"**Suprafață fizică estimată:** {A_fizic_cm2:.2f} cm²")
st.write(f"**Dimensiuni radiator:** Lungime: {L_mm:.2f} mm, Lățime: {W_mm:.2f} mm, Adâncime: {D_mm:.2f} mm")

# --- DESEN ---
st.subheader("3. Reprezentare dimensiuni radiator")
fig, ax = plt.subplots()

ax.set_xlim(0, W_mm)
ax.set_ylim(0, L_mm)
ax.set_aspect('equal')

ax.plot([0, W_mm, W_mm, 0, 0], [0, 0, L_mm, L_mm, 0], 'b-')
ax.text(W_mm/2, -10, f"Lățime: {W_mm:.0f} mm", ha='center', fontsize=8)
ax.text(-20, L_mm/2, f"Lungime: {L_mm:.0f} mm", va='center', rotation=90, fontsize=8)
ax.set_title("Dimensiuni Radiator")
ax.axis('off')

st.pyplot(fig)

st.caption("Aplicație creată cu Streamlit pentru calculul dimensional al unui arbore solicitat la torsiune și radiator auto.")
