import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def csv2db_order():
    load_dotenv()
    download_dir = os.environ['DOWNLOAD_DIR']
    order_filename = os.environ['ORDER_FILENAME']
    db_name = os.environ['SQLITE_DB_NAME']

    csv_path = os.path.join(download_dir, order_filename)
    df = pd.read_csv(csv_path, encoding='cp932')

    engine = create_engine(f'sqlite:///{db_name}.db', echo=False)
    df.to_sql("order", engine, if_exists='replace')

if __name__ == '__main__':

    csv2db_order()
    print("updated DB!")
