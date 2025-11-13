import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Параметры
INPUT_FILE = "lab_4_part_5.xlsx"
OUTPUT_TXT = "sales_analysis.txt"

print("Загружаю файл:", INPUT_FILE)

# Чтение данных
df = pd.read_excel(INPUT_FILE, engine="openpyxl", header=1, usecols="B:J")
print("Колонки в файле:", df.columns.tolist())

expected = ["Дата", "Год", "Год-мес", "точка", "бренд", "товар", "Количество", "Продажи", "Себестоимость"]
missing = [c for c in expected if c not in df.columns]
if missing:
    raise SystemExit(f"Входной файл не содержит ожидаемых колонок: {missing}. Проверьте файл.")

df = df[expected].copy()

# Приведение типов
df["Дата"] = pd.to_datetime(df["Дата"], errors="coerce")
df = df.dropna(subset=["Дата"])
df["Количество"] = pd.to_numeric(df["Количество"], errors="coerce").fillna(0)
df["Продажи"] = pd.to_numeric(df["Продажи"], errors="coerce").fillna(0)
df["Себестоимость"] = pd.to_numeric(df["Себестоимость"], errors="coerce").fillna(0)

# Создаем месячную колонку
df["Месяц"] = df["Дата"].dt.to_period("M")
df["Месяц_ts"] = df["Месяц"].dt.to_timestamp()

# ДОБАВЛЕНО: Расчет дополнительных показателей
df["СредняяЦена"] = np.where(df["Количество"] > 0, df["Продажи"] / df["Количество"], 0.0)
df["Прибыль"] = df["Продажи"] - df["Себестоимость"]
df["Рентабельность"] = np.where(df["Себестоимость"] > 0, df["Прибыль"] / df["Себестоимость"] * 100, 0.0)

# 1. Анализ по товару 
agg_product = (
    df.groupby("товар")
    .agg(
        КоличествоПродано=("Количество", "sum"),
        ОбщиеПродажи=("Продажи", "sum"),
        ОбщаяСебестоимость=("Себестоимость", "sum"),
        ОбщаяПрибыль=("Прибыль", "sum"),
        СредняяЦена=("СредняяЦена", "mean"),
        СредняяРентабельность=("Рентабельность", "mean"),
    )
    .sort_values("ОбщиеПродажи", ascending=False)
)
agg_product["Рентабельность"] = np.where(agg_product["ОбщаяСебестоимость"] > 0, agg_product["ОбщаяПрибыль"] / agg_product["ОбщаяСебестоимость"] * 100, 0)

# 2. Анализ по точке реализации 
agg_store = (
    df.groupby("точка")
    .agg(
        КоличествоПродано=("Количество", "sum"),
        ОбщиеПродажи=("Продажи", "sum"),
        ОбщаяСебестоимость=("Себестоимость", "sum"),
        ОбщаяПрибыль=("Прибыль", "sum"),
    )
    .sort_values("ОбщиеПродажи", ascending=False)
)
agg_store["Рентабельность"] = np.where(agg_store["ОбщаяСебестоимость"] > 0, agg_store["ОбщаяПрибыль"] / agg_store["ОбщаяСебестоимость"] * 100, 0)

# 3. Средние продажи на точку (по товару)
pivot_prod_store = df.pivot_table(index="товар", columns="точка", values="Продажи", aggfunc="sum", fill_value=0)
avg_sales_per_store = pivot_prod_store.replace(0, np.nan).mean(axis=1).fillna(0).sort_values(ascending=False)

# 4. Месячная динамика
monthly_total = df.groupby("Месяц_ts").agg({
    "Продажи": "sum",
    "Себестоимость": "sum", 
    "Прибыль": "sum"}).sort_index()
monthly_total["Рентабельность"] = np.where(monthly_total["Себестоимость"] > 0, monthly_total["Прибыль"] / monthly_total["Себестоимость"] * 100, 0)
monthly_pct_change = monthly_total["Продажи"].pct_change().fillna(0) * 100

# 5. Месячная динамика по товарам
monthly_by_product = df.groupby(["Месяц_ts", "товар"]).agg({
    "Продажи": "sum",
    "Прибыль": "sum"}).unstack(fill_value=0)
monthly_by_product = monthly_by_product.asfreq('MS').fillna(0)

# ПРОГНОЗЫ
forecasts = {}
H = 6

def forecast_series(series, h=6):
    if series.sum() == 0 or series.dropna().shape[0] < 3:
        return None
    s = series.copy().astype(float)
    try:
        model = ExponentialSmoothing(s, trend="add", seasonal=None, initialization_method="estimated")
        fit = model.fit(optimized=True)
        pred = fit.forecast(h)
        return pred
    except Exception:
        x = np.arange(len(s))
        y = s.values
        mask = ~np.isnan(y)
        if mask.sum() < 2:
            return None
        coef = np.polyfit(x[mask], y[mask], deg=min(2, mask.sum()-1))
        p = np.poly1d(coef)
        xp = np.arange(len(s), len(s)+h)
        idx = pd.date_range(s.index[-1] + pd.offsets.MonthBegin(), periods=h, freq='MS')
        return pd.Series(p(xp), index=idx)

for product in monthly_by_product["Продажи"].columns:
    series = monthly_by_product["Продажи"][product].asfreq('MS').fillna(0)
    pred = forecast_series(series, h=H)
    forecasts[product] = pred

# ЗАПИСЬ ОТЧЕТА
with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write("ПОЛНЫЙ АНАЛИЗ ПРОДАЖ И РЕНТАБЕЛЬНОСТИ\n")
    f.write("="*80 + "\n\n")

    f.write("1) Анализ по каждому товару (топ 50):\n")
    f.write("(включая прибыль и рентабельность)\n")
    f.write(agg_product.head(50).round(2).to_string())
    f.write("\n\n")

    f.write("2) Анализ по каждой точке реализации:\n")
    f.write("(включая прибыль и рентабельность)\n")
    f.write(agg_store.round(2).to_string())
    f.write("\n\n")

    f.write("3) Средние продажи на точку (по товарам) — топ 50:\n")
    f.write(avg_sales_per_store.head(50).round(2).to_string())
    f.write("\n\n")

    f.write("4) Месячная динамика общего товарооборота и прибыли:\n")
    f.write(monthly_total.round(2).to_string())
    f.write("\n\n")

    f.write("5) Рост/спад продаж (%) по месяцам:\n")
    f.write(monthly_pct_change.round(2).to_string())
    f.write("\n\n")

    f.write("6) Прогнозы продаж (на {} мес) по товарам:\n".format(H))
    for prod, pred in forecasts.items():
        if pred is None:
            continue
        f.write(f"\nТовар: {prod}\n")
        f.write(pred.round(2).to_string())
        f.write("\n")

print(f"Отчёт сохранён в {OUTPUT_TXT}")

# ВИЗУАЛИЗАЦИЯ
plt.rcParams.update({'figure.max_open_warning': 0})

# 1) ТОП-10 товаров по выручке и прибыли
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

agg_product.head(10)["ОбщиеПродажи"].plot(kind="bar", ax=ax1, color='skyblue')
ax1.set_title("ТОП-10 товаров по выручке")
ax1.set_xlabel("Товар")
ax1.set_ylabel("Продажи")
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, linestyle='--', alpha=0.5)

agg_product.head(10)["ОбщаяПрибыль"].plot(kind="bar", ax=ax2, color='lightgreen')
ax2.set_title("ТОП-10 товаров по прибыли")
ax2.set_xlabel("Товар")
ax2.set_ylabel("Прибыль")
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# 2) ТОП-10 точек по выручке и прибыли
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

agg_store.head(10)["ОбщиеПродажи"].plot(kind="bar", ax=ax1, color="tab:orange")
ax1.set_title("ТОП-10 точек по выручке")
ax1.set_xlabel("Точка")
ax1.set_ylabel("Продажи")
ax1.grid(True, linestyle='--', alpha=0.5)

agg_store.head(10)["ОбщаяПрибыль"].plot(kind="bar", ax=ax2, color="tab:green")
ax2.set_title("ТОП-10 точек по прибыли")
ax2.set_xlabel("Точка")
ax2.set_ylabel("Прибыль")
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# 3) Динамика продаж и прибыли
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

monthly_total[["Продажи", "Прибыль"]].plot(ax=ax1, marker="o")
ax1.set_title("Динамика продаж и прибыли по месяцам")
ax1.set_xlabel("Месяц")
ax1.set_ylabel("Сумма")
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

monthly_total["Рентабельность"].plot(ax=ax2, marker="o", color="red")
ax2.set_title("Динамика рентабельности по месяцам (%)")
ax2.set_xlabel("Месяц")
ax2.set_ylabel("Рентабельность (%)")
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# 4) Рост/спад (%) по месяцам
fig, ax = plt.subplots(figsize=(16, 7))
monthly_pct_change.plot(marker="o", ax=ax, color="red")
ax.set_title("Рост/спад продаж (%) по месяцам")
ax.set_xlabel("Месяц")
ax.set_ylabel("Изменение (%)")
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 5) Динамика продаж по топ-6 товарам
top_products = agg_product.head(6).index.tolist()
fig, ax = plt.subplots(figsize=(16, 9))
for prod in top_products:
    ax.plot(monthly_by_product["Продажи"].index, monthly_by_product["Продажи"][prod], marker='o', label=prod)
ax.set_title("Месячные продажи по топ-6 товарам")
ax.set_xlabel("Месяц")
ax.set_ylabel("Продажи")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 6) Тепловая карта: продукт x точка
try:
    import seaborn as sns
    top10 = agg_product.head(10).index
    heat = pivot_prod_store.loc[top10]
    fig, ax = plt.subplots(figsize=(18, 10))
    sns.heatmap(heat, cmap="YlGnBu", ax=ax, annot=True, fmt='.0f')
    ax.set_title("Тепловая карта: выручка (товар x точка) — топ10 товаров")
    plt.tight_layout()
    plt.show()
except Exception:
    print("Seaborn не установлен — тепловая карта пропущена.")

# 7) Анализ рентабельности по товарам
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# Топ-10 по рентабельности 
profitability_products = agg_product[agg_product["СредняяРентабельность"].abs() < 1000].nlargest(10, "СредняяРентабельность")
profitability_products["СредняяРентабельность"].plot(kind="bar", ax=ax1, color='purple')
ax1.set_title("ТОП-10 товаров по рентабельности (%)")
ax1.set_xlabel("Товар")
ax1.set_ylabel("Рентабельность (%)")
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, linestyle='--', alpha=0.5)

# Соотношение продажи/прибыль для топ-10 товаров
top10_products = agg_product.head(10)
x = range(len(top10_products))
width = 0.35
ax2.bar(x, top10_products["ОбщиеПродажи"], width, label='Продажи', color='skyblue')
ax2.bar([i + width for i in x], top10_products["ОбщаяПрибыль"], width, label='Прибыль', color='lightgreen')
ax2.set_title("Соотношение продаж и прибыли (топ-10 товаров)")
ax2.set_xlabel("Товары")
ax2.set_ylabel("Сумма")
ax2.set_xticks([i + width/2 for i in x])
ax2.set_xticklabels(top10_products.index, rotation=45)
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

print("Всё выполнено. Полный отчёт и графики готовы.")