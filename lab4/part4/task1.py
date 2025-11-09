import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Загрузка данных 
df = pd.read_excel("s7_data_sample_rev4_50k.xlsx", engine="openpyxl")

airports = pd.read_csv(
    "airports.dat.txt",
    header=None,
    quotechar='"',
    names=[
        "id", "name", "city", "country", "iata", "icao",
        "latitude", "longitude", "alt", "tz_offset", "dst",
        "tz_database", "type", "source"
    ],
    low_memory=False
)
airports = airports[airports["iata"].notna() & (airports["iata"] != "\\N")]
airports["iata"] = airports["iata"].str.strip()

# 2. Предобработка данных
df["ISSUE_DATE"] = pd.to_datetime(df["ISSUE_DATE"], errors="coerce")
df["FLIGHT_DATE_LOC"] = pd.to_datetime(df["FLIGHT_DATE_LOC"], errors="coerce")
df["REVENUE_AMOUNT"] = pd.to_numeric(df["REVENUE_AMOUNT"], errors="coerce")
df = df.dropna(subset=["ISSUE_DATE", "REVENUE_AMOUNT"])

# 3. Объединение с аэропортами 
airports_small = airports[["iata", "city", "country"]].drop_duplicates("iata")
df = df.merge(airports_small.add_prefix("orig_"), left_on="ORIG_CITY_CODE", right_on="orig_iata", how="left")
df = df.merge(airports_small.add_prefix("dest_"), left_on="DEST_CITY_CODE", right_on="dest_iata", how="left")

# 4. Описательная статистика 
print("\n=== ОБЩИЕ СТАТИСТИКИ ===")
print(df["REVENUE_AMOUNT"].describe())

print("\n=== ТИПЫ ПАССАЖИРОВ ===")
print(df["PAX_TYPE"].value_counts())

print("\n=== СПОСОБЫ ОПЛАТЫ ===")
print(df["FOP_TYPE_CODE"].value_counts())

# 5. Топ аэропортов по доходу 
top_airports = (
    df.groupby("ORIG_CITY_CODE")["REVENUE_AMOUNT"]
    .agg(["count", "sum", "mean"])
    .sort_values("sum", ascending=False)
    .head(10)
)
print("\n=== ТОП-10 аэропортов по доходу ===")
print(top_airports)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_airports.index, y=top_airports["sum"], palette="viridis")
plt.title("ТОП-10 аэропортов по суммарному доходу (вылет)")
plt.ylabel("Суммарный доход, руб.")
plt.xlabel("Аэропорт (IATA)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. Сезонность продаж
monthly = (
    df.set_index("ISSUE_DATE")
    .resample("M")["REVENUE_AMOUNT"]
    .sum()
)
plt.figure(figsize=(12, 6))
plt.plot(monthly.index, monthly.values, marker="o")
plt.title("Динамика продаж авиабилетов по месяцам")
plt.ylabel("Суммарная выручка")
plt.xlabel("Дата")
plt.grid(True)
plt.tight_layout()
plt.show()

# 7. Анализ типов пассажиров
plt.figure(figsize=(8, 5))
sns.boxplot(x="PAX_TYPE", y="REVENUE_AMOUNT", data=df, palette="Set2")
plt.title("Распределение суммы билетов по типам пассажиров")
plt.xlabel("Тип пассажира")
plt.ylabel("Сумма билета")
plt.tight_layout()
plt.show()

# 8. Способы оплаты 
pay_stats = (
    df.groupby("FOP_TYPE_CODE")["REVENUE_AMOUNT"]
    .agg(["count", "mean", "sum"])
    .sort_values("sum", ascending=False)
)
print("\n=== Доход по способам оплаты ===")
print(pay_stats)

plt.figure(figsize=(9, 5))
sns.barplot(x=pay_stats.index, y=pay_stats["sum"], palette="coolwarm")
plt.title("Доход по способам оплаты")
plt.ylabel("Суммарный доход")
plt.xlabel("Код способа оплаты")
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()
plt.show()

# 9. Сезонность по типу рейса
if "ROUTE_FLIGHT_TYPE" in df.columns:
    monthly_route = (
        df.groupby([pd.Grouper(key="ISSUE_DATE", freq="M"), "ROUTE_FLIGHT_TYPE"])["REVENUE_AMOUNT"]
        .sum()
        .unstack(fill_value=0)
    )
    monthly_route.plot(figsize=(12, 6))
    plt.title("Сезонность продаж по типу рейса (ВВЛ / МВЛ)")
    plt.ylabel("Суммарный доход")
    plt.xlabel("Месяц")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 10. Dashboard таблица
print("\n=== DASHBOARD ===")
df["Год"] = df["ISSUE_DATE"].dt.year
dashboard = (
    df.groupby(["Год", "ROUTE_FLIGHT_TYPE", "PAX_TYPE", "FOP_TYPE_CODE"])["REVENUE_AMOUNT"]
    .agg(["count", "sum", "mean"])
    .rename(columns={"count": "Кол-во билетов", "sum": "Общая выручка", "mean": "Средний чек"})
    .round(2)
    .sort_values(["Год", "Общая выручка"], ascending=[True, False])
)
print(dashboard.head(20))

# 11. Простой прогноз продаж 
series = monthly.fillna(0)
x = np.arange(len(series))
y = series.values
coeffs = np.polyfit(x, y, deg=2)
poly = np.poly1d(coeffs)
x_future = np.arange(len(series), len(series) + 6)
y_forecast = poly(x_future)
future_dates = pd.date_range(series.index[-1] + pd.offsets.MonthBegin(), periods=6, freq="M")

plt.figure(figsize=(10, 5))
plt.plot(series.index, y, label="История")
plt.plot(future_dates, y_forecast, "--", label="Прогноз (6 мес.)")
plt.title("Прогноз продаж (полином 2-го порядка)")
plt.xlabel("Дата")
plt.ylabel("Суммарная выручка")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

forecast_df = pd.DataFrame({"Дата": future_dates, "Прогноз выручки": np.round(y_forecast, 2)})
print("Прогноз продаж на следующие 6 месяцев:")
print(forecast_df)

print("Анализ успешно завершён.")