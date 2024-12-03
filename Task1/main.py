import json
import random
import re
from pprint import pprint

from models import ProductType, ParentCategory, ChildCategory, Tree
import pandas as pd


def create_category_tree(n):
    df = pd.read_excel('Task1/Дерево категорий.xlsx')
    # print(df.head())
    parent_cats = df['Главная категория'].unique()
    # 23 - 98
    # 25 - 2792
    general_cat = parent_cats[n]
    tree = Tree('category_tree')
    types = set()
    parent_category = tree.create_parent_category(general_cat)
    for child_category in df.loc[df['Главная категория'] == general_cat]['Дочерняя категория'].unique():
        category = parent_category.create_child_category(child_category)
        for pr_type in df.loc[(df['Главная категория'] == general_cat) & (df['Дочерняя категория'] == child_category)][
            'Тип товара']:
            type = category.create_product_type(pr_type)
            types.add(type)
    return tree, types


def get_products_df(product_types: set[str]):
    def get_title_and_art(title):
        pattern_title = r"^(.*?)(?=\s\d{5,6})"
        title_match = re.search(pattern_title, title)

        pattern_article = r"\d{5,6}"
        article_match = re.search(pattern_article, title)

        if article_match and article_match:
            return article_match.group(0).strip(), title_match.group(0).strip()
        else:
            pattern_quantity = r",\s\d+\s(штуки|штука|штук)\s*"
            title_cleaned = re.sub(pattern_quantity, "", title)
            return None, title_cleaned.strip()

    df: pd.DataFrame = pd.read_excel('Task1/Список товаров.xlsx')
    df = df.loc[df['Тип товара'].isin(product_types)].reset_index(drop=True)

    df['article'] = df['Наименование'].apply(lambda x: get_title_and_art(x)[0])
    df['title'] = df['Наименование'].apply(lambda x: get_title_and_art(x)[1])
    df = df.drop(columns=['Наименование', ])
    df = df.rename(columns={'Тип товара': 'product_type'})
    df = df.drop_duplicates(subset='title')
    return df

def get_columns_keys(given_products_df):
    df: pd.DataFrame = pd.read_excel('Task1/Данные поставщика.xlsx')
    print(len(df))
    df = df.loc[df['Название'].str.strip().isin(given_products_df['title'])]
    print(len(df))

    products_types_dict = given_products_df.set_index('title').to_dict()['product_type']
    columns_data = dict()

    columns = df.columns
    for index, row in df.iterrows():
        not_na_columns = set()
        for col in columns:
            if not pd.isna(row[col]) and not str(col).startswith('Изображения'):
                not_na_columns.add(col)
        pr_title = row['Название']
        pr_type = products_types_dict[pr_title]
        nncf = frozenset(not_na_columns)
        if nncf not in columns_data:
            columns_data[nncf] = set()
        columns_data[nncf].add(pr_type)

    return columns_data



def save_keys(keys, filepath='Task1/keys.json'):
    columns_data = dict()
    for k, v in keys.items():
        columns_data[str(k)] = str(v)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(columns_data, f, ensure_ascii=False, indent=4)

def load_keys(filepath='Task1/keys.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
        columns_data_lst = json.load(f)
    keys = dict()
    for k, v in columns_data_lst.items():
        keys[frozenset(eval(k))] = set(eval(v))
    return keys

def predict_product_type(keys):
    df: pd.DataFrame = pd.read_excel('Task1/Данные поставщика.xlsx')
    print('Количество товаров без типа', len(df))
    columns = df.columns
    predicted = []
    for index, row in df.iterrows():
        not_na_columns = set()
        for col in columns:
            if not pd.isna(row[col]) and not str(col).startswith('Изображения'):
                not_na_columns.add(col)
        fs = frozenset(not_na_columns)
        if fs in keys:
            predicted.append((row['Название'], keys[fs]))
        else:
            #print(row['Название'], '!!! Не найдено подходящего ключа')
            pass
    return predicted


# Раскоментировать для получения новых ключей

# Получение дерева категорий
# аргумент - номер главной категории, типы которых будут парситься
# category_tree, types = create_category_tree(25)

# Получение списка продуктов с известным типом
# products_df = get_products_df({i.name for i in types})
# print(len(products_df))

# Генерация ключей по столбцам
# keys = get_columns_keys(products_df)
# save_keys(keys)

# Предсказание типов
new_keys = load_keys()
predicted_types = predict_product_type(new_keys)
print('Количество предсказанных типов', len(predicted_types))
pprint(random.choices(predicted_types, k=20))




