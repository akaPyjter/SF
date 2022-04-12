import os
import pickle
from shutil import copyfile


def load_database(market):
    try:
        file = f'data\\database_{market}.data'
        if os.path.isfile(file) and os.path.getsize(file) > 0:
            with open(file, 'rb') as database:
                return pickle.load(database)
    except EOFError:
        file = f'data\\backup_{market}.data'
        if os.path.isfile(file) and os.path.getsize(file) > 0:
            with open(file, 'rb') as database:
                return pickle.load(database)


def read_data_from_file(market):
    file = f'data\\{market}_data.txt'
    if os.path.isfile(file) and os.path.getsize(file) > 0:
        with open(file) as input_data:
            data = input_data.read()
            data_indexes = data.split("\n")
            return data_indexes


def save_database(market, data):
    # TODO zapis danych do osobnych plikow unikac trzymania wszystkiego w ramie
    with open(f'data\\database_{market}.data', 'wb') as database:
        pickle.dump(data, database)
        copyfile(f'data\\database_{market}.data', f'data\\backup_{market}.data')


