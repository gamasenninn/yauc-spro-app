import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
download_dir = os.environ['DOWNLOAD_DIR']
order_filename = os.environ['ORDER_FILENAME']

csv_path = os.path.join(download_dir, order_filename)
df = pd.read_csv(csv_path, encoding='cp932')

engine = create_engine('sqlite:///storpro.db', echo=False)
df.to_sql("order", engine, if_exists='replace')

print("updated DB....OK")
