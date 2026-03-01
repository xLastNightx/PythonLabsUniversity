# генерируем элементы одежды (платье,штаны, блюзку) их количество(на складе), их цену, страна производства, количество проданного
# считаем остаток, стоимость реализованной(проданной) продукции (генерируем цену за 1 штуку)
#факер для этого. 
# и сделать визуализацию

import pandas as pd
import numpy as np
from faker import Faker
import matplotlib.pyplot as plt

def generate_clothing_data(num_items=50):
    fake = Faker('ru_RU')
    np.random.seed(42)
    
    data = []
    types = ['платье', 'штаны', 'блузка']
    
    for _ in range(num_items):
        item_type = np.random.choice(types)
        
        if item_type == 'платье':
            price = round(np.random.uniform(60, 300), 2)
        elif item_type == 'штаны':
            price = round(np.random.uniform(40, 150), 2)
        else:  # блузка
            price = round(np.random.uniform(30, 100), 2)
        
        in_stock = np.random.randint(5, 100)
        sold = np.random.randint(0, in_stock)
        left = in_stock - sold
        revenue = round(sold * price, 2)
        
        data.append({
            'Тип': item_type,
            'На_складе': in_stock,
            'Цена_шт': price,
            'Страна': fake.country(), 
            'Продано': sold,
            'Остаток': left,
            'Выручка': revenue
        })
    
    return pd.DataFrame(data)

df = generate_clothing_data(50)

# Сохраняем вывод в файл
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("первые 10 записей:\n")
    f.write(str(df.head(10)))
    f.write("\n")
    
    f.write(f"всего выручка: {df['Выручка'].sum():.2f} руб.\n\n")

# Выводим в консоль
print("первые 10 записей:")
print(df.head(10))
print(f"\nвсего выручка: {df['Выручка'].sum():.2f} руб.")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Анализ продаж одежды', fontsize=16, fontweight='bold')

# 1. Горизонтальная столбчатая диаграмма
sales_by_type = df.groupby('Тип')['Продано'].sum().sort_values()
types_ordered = sales_by_type.index
values = sales_by_type.values

axes[0, 0].barh(types_ordered, values, color=['lightblue', 'lightgreen', 'lightcoral'])
axes[0, 0].set_title('1. Продажи по типам одежды')
axes[0, 0].set_xlabel('Количество проданных единиц')
for i in range(len(values)):
    v = values[i]
    axes[0, 0].text(v + 2, i, str(v), va='center')

# 2. Линейный график
months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн']
monthly_avg_price = {}

for item_type in ['платье', 'штаны', 'блузка']:
    type_data = df[df['Тип'] == item_type]
    base_price = type_data['Цена_шт'].mean()
    monthly_prices = [base_price * np.random.uniform(0.9, 1.1) for _ in range(6)]
    monthly_avg_price[item_type] = monthly_prices

for item_type, prices in monthly_avg_price.items():
    axes[0, 1].plot(months, prices, marker='o', label=item_type, linewidth=2)

axes[0, 1].set_title('2. Динамика средней цены по месяцам')
axes[0, 1].set_xlabel('Месяцы')
axes[0, 1].set_ylabel('Средняя цена, руб')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 3. Круговая диаграмма
top_countries = df['Страна'].value_counts().head(5)
colors = ["#ff6b6b", '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
axes[1, 0].pie(top_countries.values, labels=top_countries.index, autopct='%1.1f%%',startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
axes[1, 0].set_title('3. ТОП-5 стран производства')

# 4. Сравнение продаж и остатков
summary_by_type = df.groupby('Тип').agg({ # операции выполнить над каждой группой
    'Продано': 'sum',
    'Остаток': 'sum'
}).reset_index()

types = summary_by_type['Тип']
sold_values = summary_by_type['Продано']
stock_values = summary_by_type['Остаток']

x = np.arange(len(types))
width = 0.35

axes[1, 1].bar(x - width/2, sold_values, width, label='Продано', color='skyblue', edgecolor='black')
axes[1, 1].bar(x + width/2, stock_values, width, label='Остаток', color='lightcoral', edgecolor='black')

axes[1, 1].set_title('4. Сравнение продаж и остатков по типам одежды')
axes[1, 1].set_xlabel('Тип одежды')
axes[1, 1].set_ylabel('Количество, шт')
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(types)
axes[1, 1].legend()
axes[1, 1].grid(True, axis='y', alpha=0.3)

for i in range(len(types)):
    axes[1, 1].text(i - width/2, sold_values[i] + 5, str(sold_values[i]), ha='center', va='bottom', fontsize=9, fontweight='bold')
    axes[1, 1].text(i + width/2, stock_values[i] + 5, str(stock_values[i]), ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()

# Вычисляем данные для вывода
type_summary = df.groupby('Тип').agg({
    'На_складе': 'sum',
    'Продано': 'sum',
    'Остаток': 'sum',
    'Выручка': 'sum',
    'Цена_шт': ['mean', 'min', 'max']
}).round(2)

total_initial = df['На_складе'].sum()
total_sold = df['Продано'].sum()
total_left = df['Остаток'].sum()
total_revenue = df['Выручка'].sum()
avg_price = df['Цена_шт'].mean()

top_selling = df.nlargest(5, 'Продано').reset_index(drop=True)
top_selling.index = top_selling.index + 1

top_expensive = df.nlargest(5, 'Цена_шт').reset_index(drop=True)
top_expensive.index = top_expensive.index + 1

# Продолжаем запись в файл
with open('output.txt', 'a', encoding='utf-8') as f:
    f.write("сводка по типам одежды:\n")
    f.write(str(type_summary))
    f.write("\n\n")
    
    f.write("ТОП-5 СТРАН ПРОИЗВОДСТВА:\n")
    top_countries_list = list(df['Страна'].value_counts().head(5).items())
    for i in range(len(top_countries_list)):
        country, count = top_countries_list[i]
        percentage = (count / len(df)) * 100
        f.write(f"{i+1}. {country}: {count} позиций ({percentage:.1f}%)\n")
    f.write("\n")
    
    f.write("ОБЩАЯ СТАТИСТИКА:\n")
    f.write(f"Всего товаров на складе было: {total_initial} шт.\n")
    f.write(f"Всего продано товаров: {total_sold} шт.\n")
    f.write(f"Остаток на складе: {total_left} шт.\n")
    f.write(f"Общая выручка: {total_revenue:.2f} руб.\n")
    f.write(f"Средняя цена товара: {avg_price:.2f} руб.\n")
    f.write("\n")
    
    f.write("ТОП-5 САМЫХ ПРОДАВАЕМЫХ ПОЗИЦИЙ:\n")
    f.write(str(top_selling[['Тип', 'Цена_шт', 'Продано', 'Выручка', 'Страна']]))
    f.write("\n\n")
    
    f.write("ТОП-5 САМЫХ ДОРОГИХ ПОЗИЦИЙ:\n")
    f.write(str(top_expensive[['Тип', 'Цена_шт', 'Продано', 'Выручка', 'Страна']]))
    f.write("\n\n")
    
    f.write(f"Всего позиций: {len(df)}\n")

print("\nсводка по типам одежды:")
print(type_summary)

print("\nТОП-5 СТРАН ПРОИЗВОДСТВА:")
top_countries_list = list(df['Страна'].value_counts().head(5).items())
for i in range(len(top_countries_list)):
    country, count = top_countries_list[i]
    percentage = (count / len(df)) * 100
    print(f"{i+1}. {country}: {count} позиций ({percentage:.1f}%)")

print("\nОБЩАЯ СТАТИСТИКА:")
print(f"Всего товаров на складе было: {total_initial} шт.")
print(f"Всего продано товаров: {total_sold} шт.")
print(f"Остаток на складе: {total_left} шт.")
print(f"Общая выручка: {total_revenue:.2f} руб.")
print(f"Средняя цена товара: {avg_price:.2f} руб.")

print("\nТОП-5 САМЫХ ПРОДАВАЕМЫХ ПОЗИЦИЙ:")
print(top_selling[['Тип', 'Цена_шт', 'Продано', 'Выручка', 'Страна']])

print("\nТОП-5 САМЫХ ДОРОГИХ ПОЗИЦИЙ:")
print(top_expensive[['Тип', 'Цена_шт', 'Продано', 'Выручка', 'Страна']])

print(f"\nВсего позиций: {len(df)}")