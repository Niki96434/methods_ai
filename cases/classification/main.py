from pathlib import Path
import pandas as pd
import numpy as np
from sklearn import preprocessing

'''
Цель: изучить особенности предварительной обработки исходных данных,
преобразования качественных показателей в количественный вид.
Задача: Исследуем набор данных Mushroom Data Set, предназначенный для проведения бинарной классификации грибов.
Набор данных включает 8124 наблюдений по 22 показателям.
'''

indexes = './mushroom/attribute_info.txt'
dataset = './mushroom/agaricus-lepiota.csv'
filePath_csv1 = './mushroom/agaricus-lepiota1.csv'

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
    column = data[i].unique()
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
# В методичке рассматриваются разные способы, а для продолжения работы выбирается Способ 3 (замена ? на 0).

# 1. Удаление строк с ячейками = ? (демонстрация)
print('Удаление строк с ячейками = ?')
data_del_rows = data[data['stalk-root'] != '?']

# 2. Удаление столбца (демонстрация)
print('Удаление столбца')
data_del_col = data.drop(labels = 'stalk-root', axis = 1)

# 3. Новое уникальное значение (выбранный способ: замена ? на 0)
print('Новое уникальное значение')
data.loc[data['stalk-root'] == '?', 'stalk-root'] = np.nan
data['stalk-root'] = data['stalk-root'].fillna(value = '0')
print('Уникальные значения stalk-root после замены:', data['stalk-root'].unique())

filePath_csv2 = './mushroom/agaricus-lepiota2.csv'
data.to_csv(filePath_csv2, index=False)

print('Преобразование качественных данных в количественные')
le = preprocessing.LabelEncoder()

data_raw = data['class']
print('\nИсходный массив:\n', data_raw)
le.fit(data_raw)
print('Классы:', le.classes_)

data_transform = le.transform(data_raw)
print('\nПреобразованный массив:\n', data_transform)
print('Классы:', np.unique(data_transform))

# Преобразование всех столбцов датасета
df_transform = pd.DataFrame()
for col in data.columns:
    le_col = preprocessing.LabelEncoder()
    df_transform[col] = le_col.fit_transform(data[col].astype(str))

print('\nУникальные значения столбцов:')
for col in data.columns:
    print(col, data[col].unique(), df_transform[col].unique())

filePath_csv3 = './mushroom/agaricus-lepiota3.csv'
df_transform.to_csv(filePath_csv3, index=False)


