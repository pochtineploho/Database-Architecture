import pandas as pd
import glob
import os
import re
from datetime import datetime

# Директория с результатами
file_path = "D:/DataGripProjects/flowwow/to_tables/resPartition"

# Регулярное выражение для извлечения данных из файлов
pattern = re.compile(r"Query: (.+)\nBest Case: ([\d.]+)\nAverage Case: ([\d.]+)\nWorst Case: ([\d.]+)")

def extract_data(filename):
    with open(filename, 'r') as file:
        content = file.read()
    queries = pattern.findall(content)
    data = {
        'Query': [],
        'Best Case': [],
        'Average Case': [],
        'Worst Case': []
    }
    for query, best, avg, worst in queries:
        data['Query'].append(query)
        data['Best Case'].append(float(best))
        data['Average Case'].append(float(avg))
        data['Worst Case'].append(float(worst))
    timestamp_str = os.path.basename(filename).split('_')[1].replace('.txt', '')
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
    except ValueError:
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d')
    return timestamp, data

# Чтение всех файлов в директории
files = glob.glob(os.path.join(file_path, 'results_*.txt'))

# Словарь для хранения всех данных
all_data = {}

# Извлечение данных из каждого файла
for file in files:
    timestamp, data = extract_data(file)
    for query in data['Query']:
        if query not in all_data:
            all_data[query] = []
        index = data['Query'].index(query)
        all_data[query].append({
            'Timestamp': timestamp,
            'Best Case': data['Best Case'][index],
            'Average Case': data['Average Case'][index],
            'Worst Case': data['Worst Case'][index]
        })

# Создание Excel файла с данными
with pd.ExcelWriter('results.xlsx') as writer:
    for query, records in all_data.items():
        df = pd.DataFrame(records)
        df = df.sort_values(by='Timestamp')
        df.to_excel(writer, sheet_name=query[:31], index=False)

