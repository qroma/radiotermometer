import numpy as np
import matplotlib.pyplot as plt

# --- Improved heat distribution (Gaussian hotspot) ---
def heat_distribution_gaussian(depth, temp_surface, temp_core, depth_core):
    temp_distribution = temp_surface + (temp_core - temp_surface) * (depth / depth_core)**2
    temp_distribution[depth > depth_core] = temp_core

    # Gaussian hotspot at 2.25 cm
    hotspot_center = 0.0225
    hotspot_width = 0.003  # meters (≈0.3 cm)
    hotspot_temp = 38.5 + 273.15  # in Kelvin

    gaussian_bump = np.exp(-((depth - hotspot_center)**2) / (2 * hotspot_width**2))
    gaussian_bump /= np.max(gaussian_bump)  # normalize
    temp_distribution += (hotspot_temp - temp_core) * gaussian_bump

    return temp_distribution

# --- Physics functions ---
def rayleigh_jeans_radiation(wavelength, temperature):
    k_B = 1.381e-23  # Boltzmann constant (J/K)
    return (2 * k_B * temperature) / (wavelength**4)

def attenuation_signal(depth, intensity_initial, absorption_coefficient):
    return intensity_initial * np.exp(-absorption_coefficient * depth)

# --- Parameters ---
#depth = np.linspace(0, 0.05, 200)  # Depth in meters (0 to 5 cm)
depth = np.linspace(0, 0.07, 250)  # 0–7 см
temp_surface = 36.5 + 273.15
temp_core = 37.1 + 273.15
depth_core = 0.05

# --- Temperature profile (Kelvin → °C) ---
temp_distribution = heat_distribution_gaussian(depth, temp_surface, temp_core, depth_core) - 273.15

# --- Antenna frequency ranges and working depths ---
antennas = {
    "Щілинна антена (1-6 ГГц)": {
        "freqs": np.arange(1, 6.5, 1),
        "depth_range": (1, 3)  # cm
    },
    "Патч-антена (1-6 ГГц)": {
        "freqs": np.arange(1, 6.5, 1),
        "depth_range": (0.5, 2)
    },
    "Хвилеводна антена (1-5 ГГц)": {
        "freqs": np.arange(1, 5.5, 1),
        "depth_range": (0.5, 4)
    },
    "Рупорна антена (0.5-8 ГГц)": {
        "freqs": np.arange(0.5, 8.5, 1),
        "depth_range": (2, 7)
    }
}

# --- Absorption coefficients ---
def absorption(freqs):
    return 2 + 0.5 * freqs

# --- Figure setup ---
width_in_inches = 13 / 2.54
height_in_inches = 12 / 2.54
fig, axes = plt.subplots(2, 2, figsize=(width_in_inches, height_in_inches))
axes = axes.flatten()

for ax, (antenna_name, props) in zip(axes, antennas.items()):
    freqs = props["freqs"]
    dmin, dmax = props["depth_range"]

    for freq in freqs:
        frequency_hz = freq * 1e9
        wavelength = 3e8 / frequency_hz
        temp_distribution_K = heat_distribution_gaussian(depth, temp_surface, temp_core, depth_core)
        radiation_intensity = rayleigh_jeans_radiation(wavelength, temp_distribution_K)
        signal_intensity = attenuation_signal(depth, radiation_intensity, absorption(freq))

        # Normalized for visibility
        ax.plot(depth * 100, signal_intensity / signal_intensity[0], label=f"{freq:.1f} ГГц")

    # Highlight antenna working depth range
    ax.axvspan(dmin, dmax, color="gray", alpha=0.2, label=f"Робоча глибина {dmin}-{dmax} см")

    ax.set_xlabel("Глибина, см", fontsize=11)
    ax.set_ylabel("Відносне випромінювання", fontsize=11)
    ax.set_title(antenna_name, fontsize=11)
    ax.legend(fontsize=8, ncol=2)
    ax.grid(True)

plt.tight_layout()
plt.show()
