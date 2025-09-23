R = 8.314  # Дж/(моль·К)
# по уравнению pV = nRT => n = pV/RT
p = float(input("enter pressure (in pa): "))
V = float(input("enter size (in m^3): "))
T_celsius = float(input("temperature (in celsius): "))

# из Цельсия в Кельвины
T_kelvin = T_celsius + 273.15
n = p * V / (T_kelvin * R)

print(f"amount of gas: {n:.4f} моль")