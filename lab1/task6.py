R = 8.314  # Дж/(моль·К)
# по уравнению pV = nRT => n = pV/RT
p = float(input("Введите давление (в Па): "))
V = float(input("Введите объем (в м^3): "))
T_celsius = float(input("Введите температуру (в Цельсия): "))

# из Цельсия в Кельвины
T_kelvin = T_celsius + 273.15
n = p * V / (T_kelvin * R)

print(f"Количество газа: {n:.4f} моль")