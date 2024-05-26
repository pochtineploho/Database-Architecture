import os
import re
import pandas as pd
from datetime import datetime

# Директория с результатами
results_dir = "D:/DataGripProjects/flowwow/performance_test/query_performance_results"

# Регулярное выражение для извлечения данных из файлов
pattern = re.compile(r"Best Case: (\d+\.\d+)\nAverage Case: (\d+\.\d+)\nWorst Case: (\d+\.\d+)")


# Функция для извлечения данных из файлов
def extract_data_from_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
    match = pattern.search(content)
    if match:
        best_case = float(match.group(1))
        average_case = float(match.group(2))
        worst_case = float(match.group(3))
        return best_case, average_case, worst_case
    return None


# Словарь для хранения данных по каждому типу запроса
query_data = {
    "Order Statistics": [],
    "Products and Shops by Rating and Name": [],
    "Most popular shop": [],
    "Most popular product": [],
    "Most Purchased Collection": []
}


# Функция для извлечения метки времени из имени файла
def extract_timestamp_from_filename(filename):
    # Предполагается, что timestamp это последние 15 символов имени файла, перед ".txt"
    timestamp_str = filename[-19:-4]
    return datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')


# Чтение всех файлов и извлечение данных
for filename in os.listdir(results_dir):
    if filename.endswith(".txt"):
        parts = filename.split('_')
        query_name = ' '.join(parts[:-2])
        try:
            timestamp = extract_timestamp_from_filename(filename)
        except ValueError:
            print(f"Filename {filename} does not match the expected timestamp format.")
            continue
        data = extract_data_from_file(os.path.join(results_dir, filename))
        if data:
            query_data[query_name].append((timestamp, data))

# Создание Excel файла
with pd.ExcelWriter('query_performance_summary.xlsx') as writer:
    for query_name, data in query_data.items():
        # Сортировка данных по timestamp
        data.sort(key=lambda x: x[0])

        # Создание DataFrame и запись в Excel
        df = pd.DataFrame(data, columns=["Timestamp", "Results"])
        df["Best Case"] = df["Results"].apply(lambda x: x[0])
        df["Average Case"] = df["Results"].apply(lambda x: x[1])
        df["Worst Case"] = df["Results"].apply(lambda x: x[2])
        df.drop(columns=["Results"], inplace=True)

        df.to_excel(writer, sheet_name=query_name, index=False)

        # Пример вычисления изменения производительности (Best Case)
        initial_best_case = df["Best Case"].iloc[0]
        final_best_case = df["Best Case"].iloc[-1]
        change_best_case = ((final_best_case - initial_best_case) / initial_best_case) * 100
        print(f"{query_name} Best Case Change: {change_best_case:.2f}%")

print("Excel file 'query_performance_summary.xlsx' created.")
