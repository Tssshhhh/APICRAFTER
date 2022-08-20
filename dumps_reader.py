import datetime
import glob
import json
import pandas as pd


def create_excel() -> list:
    list_of_dicts = []
    for _ in glob.glob('dumps\*'):
        with open(_, 'r', encoding='cp1251') as f:
            file = f.read()
            dump = json.loads(file)
        for _ in dump:
            list_of_dicts.append(_)
    df = pd.DataFrame.from_dict(list_of_dicts)
    time_ = datetime.datetime.now().time().strftime("%H.%M")
    df.to_excel(f'parsed_page{time_}.xlsx')


if __name__ == "__main__":
    create_excel()
