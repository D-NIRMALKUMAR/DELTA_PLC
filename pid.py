import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Initialize session state for previous values to make it persistent across updates
if "previous_error" not in st.session_state:
    st.session_state.previous_error = 0
if "I_term" not in st.session_state:
    st.session_state.I_term = 0
if "temperatures" not in st.session_state:
    st.session_state.temperatures = []
if "output_history" not in st.session_state:
    st.session_state.output_history = []

# PID Control function
def pid_control(setpoint, current_temp, Kp, Ki, Kd, previous_error, I_term, dt):
    error = setpoint - current_temp
    P_term = Kp * error
    I_term += Ki * error * dt
    D_term = Kd * (error - previous_error) / dt
    output = P_term + I_term + D_term
    previous_error = error
    return output, previous_error, I_term

# Streamlit UI elements
st.title("PID Controller Simulation for Temperature Control")

# Setpoint slider
setpoint = st.slider("Setpoint Temperature (°C)", min_value=50, max_value=100, value=75)

# PID Parameter Sliders
Kp = st.slider("Proportional Gain (Kp)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
Ki = st.slider("Integral Gain (Ki)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
Kd = st.slider("Derivative Gain (Kd)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)

# Simulation time steps
num_steps = st.slider("Number of Time Steps", min_value=10, max_value=200, value=50)
dt = 1  # Time step duration in seconds

# Simulation
current_temp = 50  # Starting temperature
temperatures = [current_temp]

for step in range(num_steps):
    output, st.session_state.previous_error, st.session_state.I_term = pid_control(
        setpoint, current_temp, Kp, Ki, Kd, st.session_state.previous_error, st.session_state.I_term, dt
    )
    current_temp += output * 0.1 - 0.1  # Heating + small cooling effect
    temperatures.append(current_temp)
    st.session_state.output_history.append(output)

# Plotting the Temperature and PID Output over Time
fig, ax = plt.subplots(2, 1, figsize=(10, 8))
time = np.arange(len(temperatures))

# Temperature Plot
ax[0].plot(time, temperatures, label="Temperature (°C)")
ax[0].axhline(y=setpoint, color="r", linestyle="--", label="Setpoint")
ax[0].set_title("Temperature Over Time")
ax[0].set_xlabel("Time Step")
ax[0].set_ylabel("Temperature (°C)")
ax[0].legend()

# PID Output Plot
ax[1].plot(time[:-1], st.session_state.output_history, label="PID Output", color="purple")
ax[1].set_title("PID Output Over Time")
ax[1].set_xlabel("Time Step")
ax[1].set_ylabel("Output")
ax[1].legend()

st.pyplot(fig)

# Reset Button
if st.button("Reset Simulation"):
    st.session_state.previous_error = 0
    st.session_state.I_term = 0
    st.session_state.temperatures = []
    st.session_state.output_history = []
    st.experimental_rerun()
