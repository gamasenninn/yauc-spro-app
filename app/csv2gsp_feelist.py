import pandas as pd
import os
from dotenv import load_dotenv
import datetime
import gspread
import gspread_dataframe as gs_df

def csv2gsp_feelist():
    load_dotenv()
    data_dir = os.environ['DATA_DIR']
    fee_list_filename = os.environ['FEE_LIST_FILENAME']
    db_name = os.environ['SQLITE_DB_NAME']
    gsp_json = os.environ['GSP_JSON']
    spreadsheet_key = os.environ['SPREADSHEET_KEY']
    sheet_name = os.environ['SHEET_NAME']
    fee_list_file_path = os.path.join(
        data_dir, datetime.datetime.now().strftime('%y%m%d')+'_'+fee_list_filename)

    if not os.path.isfile(fee_list_file_path):
        return False

    df = pd.read_csv(fee_list_file_path, encoding='cp932')


    #-----------------Googleスプレッドシートの事前設定 ---------------------

    #ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
    from oauth2client.service_account import ServiceAccountCredentials
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    credentials = ServiceAccountCredentials.from_json_keyfile_name(gsp_json, scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #----------------- シートの設定 ---------------------

    #共有設定したスプレッドシートのシート1を開く
    workbook = gc.open_by_key(spreadsheet_key)
    #worksheet = workbook.sheet1
    worksheet = workbook.worksheet(sheet_name)

    #-----------------スプレッドシートへの書き込み---------------------

    gs_df.set_with_dataframe(worksheet,df)
    return True

if __name__ == '__main__':
    dir_name = os.path.dirname(os.path.abspath(__file__))
    print(dir_name)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if csv2gsp_feelist():
        print("updated G spread shhet!")
    else:
        print("Ignored")