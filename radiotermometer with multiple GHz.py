import numpy as np
import matplotlib.pyplot as plt

def heat_distribution(depth, temp_surface, temp_core, depth_core):
    temp_distribution = temp_surface + (temp_core - temp_surface) * (depth / depth_core)**2
    temp_distribution[depth > depth_core] = temp_core
    return temp_distribution

def rayleigh_jeans_radiation(wavelength, temperature):
    k_B = 1.381e-23  # Boltzmann constant (J/K)
    return (2 * k_B * temperature) / (wavelength**4)

def attenuation_signal(depth, intensity_initial, absorption_coefficient):
    return intensity_initial * np.exp(-absorption_coefficient * depth)

def total_signal(depth, temp_distribution, signal_intensity, transfer_function):
    return np.trapz(signal_intensity * temp_distribution * transfer_function, depth)

# Parameters
depth = np.linspace(0, 0.05, 100)  # Depth in meters (0 to 5 cm)
temp_surface = 36.5 + 273.15  # Surface temperature in Kelvin
temp_core = 37.1 + 273.15  # Core temperature in Kelvin
depth_core = 0.05  # Depth where core temperature is reached (5 cm)
intensity_initial = 1.0  # Arbitrary units
transfer_function = np.exp(-depth / 0.01)  # Example transfer function

# Frequency range (in GHz)
frequencies = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])  # GHz
frequencies = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # GHz
absorption_coefficients = 10 + 2 * frequencies  # Example absorption model (higher freq = more absorption)

# Set up the plot
plt.figure(figsize=(8, 6))

for freq, absorption_coefficient in zip(frequencies, absorption_coefficients):
    frequency_hz = freq * 1e9  # Convert GHz to Hz
    wavelength = 3e8 / frequency_hz  # Calculate wavelength in meters

    # Calculate temperature distribution
    temp_distribution = heat_distribution(depth, temp_surface, temp_core, depth_core)

    # Calculate Rayleigh-Jeans radiation
    radiation_intensity = rayleigh_jeans_radiation(wavelength, temp_distribution)

    # Calculate signal attenuation with frequency-dependent absorption coefficient
    signal_intensity = attenuation_signal(depth, radiation_intensity, absorption_coefficient)

    # Plot signal intensity for this frequency
    plt.plot(depth * 100, signal_intensity, label=f"{freq} GHz")

# Customize the plot
plt.xlabel("Depth (cm)")
plt.ylabel("Intensity (a.u.)")
plt.title("Signal Intensity vs. Depth for Different Frequencies")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
