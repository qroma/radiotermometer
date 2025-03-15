import numpy as np
import matplotlib.pyplot as plt

# Redefine the adjusted heat distribution function
def heat_distribution(depth, temp_surface, temp_core, depth_core, thermal_conductivity, metabolic_heat, density, specific_heat):
    """
    Calculate the temperature distribution in tissue layers based on depth.

    depth: np.array - Array of depths (m).
    temp_surface: float - Surface temperature (K).
    temp_core: float - Core temperature (K) at depth_core.
    depth_core: float - Depth at which core temperature is reached (m).
    thermal_conductivity: float - Thermal conductivity (W/m*K).
    metabolic_heat: float - Metabolic heat generation (W/m^3).
    density: float - Tissue density (kg/m^3).
    specific_heat: float - Specific heat capacity (J/kg*K).

    Returns:
    Temperature distribution as a function of depth.
    """
    temp_distribution = temp_surface + (temp_core - temp_surface) * (depth / depth_core)**2
    temp_distribution[depth > depth_core] = temp_core
    return temp_distribution

def rayleigh_jeans_radiation(wavelength, temperature):
    """
    Calculate the spectral radiance using the Rayleigh-Jeans law.

    wavelength: float - Wavelength (m).
    temperature: float - Temperature (K).

    Returns:
    Spectral radiance (W/m^3).
    """
    k_B = 1.381e-23  # Boltzmann constant (J/K)
    return (2 * k_B * temperature) / (wavelength**4)

def attenuation_signal(depth, intensity_initial, absorption_coefficient):
    """
    Calculate signal attenuation based on the depth of tissue.

    depth: np.array - Array of depths (m).
    intensity_initial: float - Initial signal intensity (arbitrary units).
    absorption_coefficient: float - Absorption coefficient (1/m).

    Returns:
    Signal intensity as a function of depth.
    """
    return intensity_initial * np.exp(-absorption_coefficient * depth)

def total_signal(depth, temp_distribution, signal_intensity, transfer_function):
    """
    Calculate the total signal received by the radiothermometer.

    depth: np.array - Array of depths (m).
    temp_distribution: np.array - Temperature distribution in tissue.
    signal_intensity: np.array - Signal intensity at each depth.
    transfer_function: np.array - Weighting function of the radiothermometer.

    Returns:
    Total signal.
    """
    return np.trapz(signal_intensity * temp_distribution * transfer_function, depth)

# Parameters
depth = np.linspace(0, 0.05, 100)  # Depth in meters (0 to 5 cm)
temp_surface = 36.5 + 273.15  # Surface temperature in Kelvin
temp_core = 37.1 + 273.15  # Core temperature in Kelvin
depth_core = 0.05  # Depth where core temperature is reached (5 cm)
thermal_conductivity = 0.5  # W/m*K
metabolic_heat = 5000  # W/m^3
density = 1000  # kg/m^3
specific_heat = 3500  # J/kg*K
absorption_coefficient = 20  # 1/m
intensity_initial = 1.0  # Arbitrary units
transfer_function = np.exp(-depth / 0.01)  # Example transfer function

# Wavelength and frequency parameters
frequency = 1e9  # Frequency in Hz (e.g., 1 GHz)
wavelength = 3e8 / frequency  # Wavelength in meters

# Calculate temperature distribution
temp_distribution = heat_distribution(
    depth, temp_surface, temp_core, depth_core, thermal_conductivity, metabolic_heat, density, specific_heat
)

# Calculate Rayleigh-Jeans radiation at each depth
radiation_intensity = rayleigh_jeans_radiation(wavelength, temp_distribution)

# Calculate signal attenuation
signal_intensity = attenuation_signal(depth, radiation_intensity, absorption_coefficient)

# Calculate total signal
total_received_signal = total_signal(depth, temp_distribution, signal_intensity, transfer_function)

# Output results
result = f"Total received signal: {total_received_signal:.4f}"

# Перевести розміри з сантиметрів у дюйми
width_in_inches = 13 / 2.54
height_in_inches = 8 / 2.54

# Visualization
# Visualization for the temperature distribution
plt.figure(figsize=(width_in_inches, height_in_inches))
plt.plot(depth * 100, temp_distribution - 273.15, label="Розподіл температури")
plt.xlabel("Глибина, см", fontsize=12)
plt.ylabel("Температура, °C", fontsize=12)
plt.legend(fontsize=12)
plt.grid()
plt.show()

# Visualization for the radiation intensity
plt.figure(figsize=(width_in_inches, height_in_inches))
plt.plot(depth * 100, radiation_intensity, label="Випромінювання", color="green")
plt.xlabel("Глибина, см", fontsize=12)
plt.ylabel("Випромінювання, у.о.", fontsize=12)
plt.legend(fontsize=12)
plt.grid()
plt.show()

# Visualization for the signal intensity
plt.figure(figsize=(width_in_inches, height_in_inches))
plt.plot(depth * 100, signal_intensity, label="Випромінювання", color="orange")
plt.xlabel("Глибина, см", fontsize=12)
plt.ylabel("Випромінювання, у.о.", fontsize=12)
plt.legend(fontsize=12)
plt.grid()
plt.show()

result