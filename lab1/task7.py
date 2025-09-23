seconds = int(input("enter number of seconds: "))

# Расчет
minutes = seconds // 60
sec = seconds % 60

# Вывод
print(f"{seconds}: {minutes} minutes {sec} seconds")