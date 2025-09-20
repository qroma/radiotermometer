import numpy as np
import matplotlib.pyplot as plt

# Параметри антен (середня частота та глибина проникнення з таблиці користувача)
antennas = {
    "1. Щілинна антена": {"freq": 2.0, "depth": 2.0},   # ГГц, см
    "2. Патч антена": {"freq": 2.5, "depth": 1.25},
    "3. Хвилеводна антена": {"freq": 3.0, "depth": 2.25},
    "4. Рупорна антена": {"freq": 4.5, "depth": 4.0}
}

# Умови тканини
T_base = 36.6  # °C - нормальна температура
T_hot = 38.5   # °C - температура локальної ділянки
hot_center = 2.0  # см - глибина центру аномалії
hot_width = 0.5   # см - товщина "гарячої" зони

# Діапазон глибин
depths = np.linspace(0, 5, 500)  # см

# Моделювання вимірюваної температури
plt.figure(figsize=(10,6))

for name, params in antennas.items():
    delta = params["depth"]
    
    # Модель температури в тканині (локальне підвищення)
    tissue_temp = np.full_like(depths, T_base)
    mask = (depths >= hot_center - hot_width/2) & (depths <= hot_center + hot_width/2)
    tissue_temp[mask] = T_hot
    
    # Вагова функція чутливості антени по глибині (експоненційне затухання)
    sensitivity = np.exp(-depths/delta)
    
    # Нормалізація ваг
    sensitivity /= np.sum(sensitivity)
    
    # Вимірювана температура = інтеграл температури з урахуванням чутливості
    measured_temp = np.sum(tissue_temp * sensitivity)
    
    plt.plot(depths, tissue_temp * sensitivity / np.max(sensitivity), label=f"{name}")
#(виміряно: {measured_temp:.2f} °C)
plt.xlabel("Глибина, см")
plt.ylabel("Чутливість, ум. од.")
plt.title("Моделювання виявлення локальної 'гарячої' ділянки різними антенами")
plt.legend()
plt.grid(True)
plt.show()
