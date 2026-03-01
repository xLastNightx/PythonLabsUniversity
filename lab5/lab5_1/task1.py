# task.py
import requests, os, time, re, sys
from bs4 import BeautifulSoup
from slugify import slugify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache_pages")
os.makedirs(CACHE_DIR, exist_ok=True)

INPUT_FILE = os.path.join(BASE_DIR, "countries.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "countries_data.csv")
DEFAULT_COUNTRIES = ["France", "Brazil", "Japan", "Germany", "Canada", "Australia"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def ensure_countries_file(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            for c in DEFAULT_COUNTRIES:
                f.write(c + "\n")

def load_page_cached(country, refresh=False):
    file_name = slugify(country) + ".html"
    cache_path = os.path.join(CACHE_DIR, file_name)
    if os.path.exists(cache_path) and not refresh:
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()
    url = f"https://en.wikipedia.org/wiki/{country}"
    print(f"Загружаю: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=12)
    resp.raise_for_status()
    html = resp.text
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(html)
    time.sleep(1)
    return html

def clean(text):
    return re.sub(r"\[[^\]]*\]", "", text).replace("\u00a0", " ").strip()

def extract_number(text):
    """Извлекает число из текста, убирая пробелы и запятые"""
    if not text:
        return ""
    
    # Ищем шаблоны типа 12,345,678 или 12 345 678
    match = re.search(r"(\d{1,3}(?:[,\s]\d{3})*(?:\.\d+)?)", str(text))
    if match:
        num_str = match.group(1).replace(" ", "").replace(",", "")
        # Если есть десятичная часть, берем только целую
        if "." in num_str:
            return num_str.split(".")[0]
        return num_str
    return ""

def extract_capital(td):
    """Извлекает столицу из ячейки"""
    if not td:
        return ""
    
    # Пробуем найти ссылку с названием столицы
    a = td.find("a")
    if a:
        return clean(a.get_text())
    
    # Или берем текст ячейки
    text = clean(td.get_text())
    # Убираем дополнительные пояснения в скобках
    text = re.split(r'[\(\[{]', text)[0].strip()
    return text

def extract_area(td):
    """Извлекает площадь из ячейки"""
    if not td:
        return ""
    
    text = clean(td.get_text())
    
    # Ищем число с указанием км²
    area_match = re.search(r"(\d{1,3}(?:[,\s]\d{3})*(?:\.\d+)?)\s*(?:km²|km2|sq\s*mi)", text, re.IGNORECASE)
    if area_match:
        return extract_number(area_match.group(1))
    
    # Если не нашли с единицами измерения, ищем просто большое число
    return extract_number(text)

def extract_population(td):
    """Извлекает население из ячейки"""
    if not td:
        return ""
    
    text = clean(td.get_text())
    
    # Обрабатываем формат "X million"
    million_match = re.search(r"(\d+(?:\.\d+)?)\s*million", text, re.IGNORECASE)
    if million_match:
        millions = float(million_match.group(1))
        return str(int(millions * 1_000_000))
    
    # Ищем числа с разделителями
    numbers = re.findall(r"\d{1,3}(?:[,\s]\d{3})+", text)
    for num in numbers:
        clean_num = extract_number(num)
        if clean_num and 100000 <= int(clean_num) <= 2000000000:
            return clean_num
    
    # Ищем любые большие числа
    large_numbers = re.findall(r"\d{6,}", text.replace(" ", "").replace(",", ""))
    for num in large_numbers:
        if 100000 <= int(num) <= 2000000000:
            return num
    
    return ""

def find_info_by_label(soup, label_patterns):
    """Ищет информацию по меткам в инфобоксе"""
    for label in label_patterns:
        element = soup.find(lambda tag: tag.name in ['th', 'td'] and 
                           any(pattern.lower() in tag.get_text().lower() 
                               for pattern in label_patterns[label]))
        if element:
            # Переходим к следующему элементу (данные обычно в следующей ячейке)
            next_td = element.find_next('td')
            if next_td:
                return next_td
    return None

def parse_country_data(country, refresh=False):
    """Парсит данные о стране из Википедии"""
    html = load_page_cached(country, refresh)
    if not html:
        return (country, "", "", "")
    
    soup = BeautifulSoup(html, "html.parser")
    infobox = soup.find("table", class_=lambda c: c and "infobox" in str(c).lower())
    
    if not infobox:
        return (country, "", "", "")
    
    capital = area = population = ""
    
    # Словарь для поиска различных вариантов написания меток
    labels = {
        'capital': ['capital', 'capital and largest city'],
        'area': ['area', 'total area', 'area total', '• total'],
        'population': ['population', '• total', 'population total']
    }
    
    # Поиск столицы
    capital_td = find_info_by_label(infobox, {'capital': labels['capital']})
    if capital_td:
        capital = extract_capital(capital_td)
    
    # Поиск площади
    area_td = find_info_by_label(infobox, {'area': labels['area']})
    if area_td:
        area = extract_area(area_td)
    
    # Поиск населения
    population_td = find_info_by_label(infobox, {'population': labels['population']})
    if population_td:
        population = extract_population(population_td)
    
    # Альтернативный метод: перебор всех строк таблицы
    if not all([capital, area, population]):
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            
            if not th or not td:
                continue
                
            header_text = clean(th.get_text()).lower()
            data_text = clean(td.get_text())
            
            # Столица
            if not capital and any(pattern in header_text for pattern in labels['capital']):
                capital = extract_capital(td)
            
            # Площадь
            if not area and any(pattern in header_text for pattern in labels['area']):
                area = extract_area(td)
            
            # Население
            if not population and any(pattern in header_text for pattern in labels['population']):
                population = extract_population(td)
    
    return (country, capital, area, population)

def save_aligned_csv(rows, output_file):
    """Сохраняет данные в выровненном CSV формате"""
    header = ["country", "city", "area (km2)", "population"]
    all_rows = [tuple(header)] + rows
    
    # Вычисляем максимальные ширины для каждого столбца
    widths = [max(len(str(row[i])) for row in all_rows) for i in range(4)]
    
    with open(output_file, "w", encoding="utf-8") as f:
        # Заголовок
        f.write(" | ".join(str(header[i]).ljust(widths[i]) for i in range(4)) + "\n")
        f.write("-" * (sum(widths) + 9) + "\n")
        
        # Данные
        for row in rows:
            f.write(" | ".join(str(row[i]).ljust(widths[i]) for i in range(4)) + "\n")

def main():
    refresh = "--refresh" in sys.argv
    ensure_countries_file(INPUT_FILE)
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        countries = [x.strip() for x in f if x.strip()]
    
    rows = []
    for country in countries:
        print(f"Парсинг: {country}")
        try:
            data = parse_country_data(country, refresh)
            rows.append(data)
            print(f"  Найдено: столица='{data[1]}', площадь='{data[2]}', население='{data[3]}'")
        except Exception as e:
            print(f"Ошибка при парсинге {country}: {e}")
            rows.append((country, "", "", ""))
    
    save_aligned_csv(rows, OUTPUT_FILE)
    print(f"\nГотово! Данные сохранены в {OUTPUT_FILE}")
    
    # Вывод результатов в консоль для проверки
    print("\nРезультаты:")
    print("country   | city     | area (km2) | population")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:<9} | {row[1]:<8} | {row[2]:<10} | {row[3]}")

if __name__ == "__main__":
    main()