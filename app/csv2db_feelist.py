import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import datetime

load_dotenv()
data_dir = os.environ['DATA_DIR']
fee_list_filename = os.environ['FEE_LIST_FILENAME']
db_name = os.environ['SQLITE_DB_NAME']

fee_list_file_path = os.path.join(
    data_dir, datetime.datetime.now().strftime('%y%m%d')+'_'+fee_list_filename)

df = pd.read_csv(fee_list_file_path, encoding='cp932')

engine = create_engine(f'sqlite:///{db_name}.db', echo=False)
df.to_sql("fee_list", engine, if_exists='replace')

print("updated DB!")
