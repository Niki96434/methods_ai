from pathlib import Path
import pandas as pd
import numpy as np

'''
Цель: изучить особенности предварительной обработки исходных данных,
преобразования качественных показателей в количественный вид.
Задача: Исследуем набор данных Mushroom Data Set, предназначенный для проведения бинарной классификации грибов.
Набор данных включает 8124 наблюдений по 22 показателям.
'''

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

indexes = BASE_DIR / 'attribute_info.txt'
dataset = PROJECT_ROOT / 'mushroom' / 'agaricus-lepiota.csv'
filePath_csv1 = PROJECT_ROOT / 'mushroom' / 'agaricus-lepiota1.csv'

with open(indexes, 'r', encoding='utf-8') as f:
    file_text = []
    for file in f:
        file_text.append(file)

attributes_names = ['class']
for atr in file_text:
    name = atr[: atr.find(':')]
    name = name[atr.find('.') + 2 :]
    attributes_names.append(name)

dataset_csv = pd.read_csv(dataset, sep=",")
dataset_csv.columns = attributes_names
dataset_csv.to_csv(filePath_csv1, index = False)

# Предобработка данных

data = pd.read_csv(filePath_csv1)

for i in data.columns:
    column = data.iloc[:, i].unique()
    print(column)

print('\nудаление столбца veil-type с 1 уникальным значением')
for col in data.columns:
    if len(data[col].unique()) == 1:
        data = data.drop(labels = col, axis = 1)

print('\nпоиск пропущенных значений')
for col in data.columns:
    if '?' in data[col].unique():
        print(col, data[col].unique())
        print('\nподсчет пропущенных значений в ячейках таблицы')
        print(len(data[col][data[col] == '?']))

# Обработка пропущенных значений
print('Удаление строк с ячейками = ?')
data = data[data['stalk-root'] != '?']

print('Удаление столбца')
data = data.drop(labels = 'stalk-root', axis = 1)
del data['stalk-root']

print('Новое уникальное значение')
data['stalk-root'][data['stalk-root'] == '?'] = np.nan
data['stalk-root'] = data['stalk-root'].fillna(value = 0)
print(len(data['stalk-root'][data['stalk-root'].isna()]))

print('Метод прямого заполнения')
data['stalk-root'][data['stalk-root'] == '?'] = np.nan
data['stalk-root'] = data['stalk-root'].fillna(method = 'ffill')

print('Метод обратного заполнения')
data['stalk-root'][data['stalk-root'] == '?'] = np.nan
data['stalk-root'] = data['stalk-root'].fillna(method = 'bfill')

print('Заменим символы ? на 0:')
data['stalk-root'][df['stalk-root'] == '?'] = np.nan
print(data['stalk-root'].unique())

filePath_csv2 = PROJECT_ROOT / 'mushroom' / 'agaricus-lepiota2.csv'
data.to_csv(filePath_csv2, index=False)
