import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker

# Инициализация генератора данных
fake = Faker('ru_RU')
np.random.seed(42) # Чтобы данные повторялись и не сбивались (проще анализировать)

n_students = 500  # количество студентов
years = np.random.choice(range(2019, 2024), n_students)
forms = np.random.choice(['Бюджет', 'Платное'], n_students, p=[0.6, 0.4])
specialties = np.random.choice(['Информатика', 'Экономика', 'Юриспруденция', 'Филология', 'Математика', 'Физика'], n_students)

# Генерация баллов
ct_scores = np.random.normal(70, 10, n_students).clip(30, 100)          # Баллы ЦТ/ЦЭ
att_scores = np.random.normal(8, 1, n_students).clip(4, 10)             # Средний балл аттестата
total_scores = ct_scores * 0.7 + att_scores * 10 * 0.3                  # Общий балл при поступлении

# Генерация личных данных
data = {
    'ФИО': [fake.name() for _ in range(n_students)],
    'Год поступления': years,
    'Форма обучения': forms,
    'Балл ЦТ/ЦЭ': np.round(ct_scores, 1),
    'Средний балл аттестата': np.round(att_scores, 2),
    'Общий балл при поступлении': np.round(total_scores, 2),
    'Специальность': specialties,
    'Адрес': [fake.address().replace('\n', ', ') for _ in range(n_students)],
    'Телефон': [fake.phone_number() for _ in range(n_students)]
}

df = pd.DataFrame(data)

# Средний балл ЦТ/ЦЭ по годам
avg_ct_by_year = df.groupby('Год поступления')['Балл ЦТ/ЦЭ'].mean()

# Средний балл аттестата по годам
avg_att_by_year = df.groupby('Год поступления')['Средний балл аттестата'].mean()

# Средний общий балл (условно "проходной")
avg_total_by_year = df.groupby('Год поступления')['Общий балл при поступлении'].mean()

# Количество студентов по специальностям
count_by_specialty = df['Специальность'].value_counts()

# Статистика по форме обучения
count_by_form = df['Форма обучения'].value_counts()

plt.figure(figsize=(14, 8))

# 1. Динамика среднего балла ЦТ/ЦЭ
plt.subplot(2, 2, 1)
plt.plot(avg_ct_by_year.index, avg_ct_by_year.values, marker='o')
plt.title('Динамика среднего балла ЦТ/ЦЭ')
plt.xlabel('Год поступления')
plt.ylabel('Средний балл')
plt.grid(True)

# 2. Динамика среднего балла аттестата
plt.subplot(2, 2, 2)
plt.plot(avg_att_by_year.index, avg_att_by_year.values, marker='s', color='orange')
plt.title('Динамика среднего балла аттестата')
plt.xlabel('Год поступления')
plt.ylabel('Средний балл')
plt.grid(True)

# 3. Динамика "проходного" балла
plt.subplot(2, 2, 3)
plt.plot(avg_total_by_year.index, avg_total_by_year.values, marker='^', color='green')
plt.title('Динамика проходного балла')
plt.xlabel('Год поступления')
plt.ylabel('Средний общий балл')
plt.grid(True)

# 4. Количество поступивших по специальностям
plt.subplot(2, 2, 4)
count_by_specialty.plot(kind='bar', color='purple')
plt.title('Количество поступивших по специальностям')
plt.ylabel('Количество студентов')
plt.xticks(rotation=45)

# Визуализация статистики по формам обучения
plt.figure(figsize=(5, 4))
count_by_form.plot(kind='bar', color=['skyblue', 'lightcoral'])
plt.title('Статистика по формам обучения')
plt.ylabel('Количество студентов')
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("\nСТАТИСТИКА ПО ФОРМАМ ОБУЧЕНИЯ:")
print(count_by_form)

print("\nСРЕДНИЕ БАЛЛЫ ПО ГОДАМ:")
summary = pd.DataFrame({
    'ЦТ/ЦЭ': avg_ct_by_year.round(2),
    'Аттестат': avg_att_by_year.round(2),
    'Общий': avg_total_by_year.round(2)
})
print(summary)