import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

import os, logging
import pymysql, smtplib
import param_common as param
from cocacola import calc_price, plot_graph
from demographic import *

# get the list of the path from a csv file.
def path_listup(df):
    path_dict = {}
    separator = "/" # create the full path to the csv file reading a csv file
    
    for index, row in df.iterrows():
        #path_list = []
        path_dict[row[1]] = separator.join([row[0], row[1], row[2]]) # dictionary: folder, full path
    return path_dict

def insert_data():
    chk = "Select * from sqlite_master where type=%"
    for index, row in df.iterrows():    
        #print(row['name'], row['age'], row['city'])
        sql = "INSERT INTO sample (name, age, city) VALUES (%s, %s, %s)"
        chk = cur.execute(chk, row['name'] , row['age'], row['city'])
        
        if chk == 0:
            success = success + 1
        else:
            fail = fail + 1
    success_chk_list = {'number of success query': success, 'number of fail': fail}
    return success_chk_list

def send_mail(mail_address, mail_pw):
    
    logging.info('メール送信処理を開始します。')
    try:
        # メールの内容(SSMから取得)
        from_address = mail_address
        to_address = mail_address
        subject = "Data analysis report"
        bodyText = "Here's your data analysis report."
        inquiry_category = "Data analysis"
        attachments = []
    except Exception as e:
        logging.error('メールの内容をSSMから取得できませんでした。{}'.format(e))
            
    try:
        if "gmail.com" in mail_address:
            port = 465
            with smtplib.SMTP_SSL('smtp.gmail.com', port) as smtp_server:
                smtp_server.login(mail_address, gmail_pw)
                message = 'Subject: {}\n\n{}'.format(subject, bodyText)
                smtp_server.sendmail(from_address, to_address, message)
            logging.info('正常にgmail送信完了')
            
        elif "outlook" in mail_address:
            port = 587
            with smtplib.SMTP('smtp-mail.outlook.com', port) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(mail_address, gmail_pw)
                message = 'Subject: {}\n\n{}'.format(subject, bodyText)
                smtp_server.sendmail(from_address, to_address, message)
            logging.info('正常にOutlookメール送信完了')

    except Exception as e:
        logging.error('メール送信処理でエラーが発生しました。{}'.format(e))


if __name__ == "__main__":
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # current directory path
    current_file_path = os.path.abspath(__file__)

    credentials = Credentials.from_service_account_file(f"{current_file_path}\credentials.json", scopes=scope)
    gc = gspread.authorize(credentials)
    workbook = gc.open("csv_list")
    sheet = workbook.worksheet("Sheet1")
    data = sheet.get_all_values()
    
    df = pd.DataFrame(data)
    df_list = path_listup(df)
    
    try:
        logging.info("SSMパラメータ取得開始します。")
        db_name = param.db_name
        db_tbl = param.db_tbl
        db_usrname = param.db_usrname
        db_pw = param.db_pw
        path = param.path
        gmail_addr = param.gmail_addr
        gmail_pw = param.gmail_pw
    except Exception as e:
        logging.error('SSMパラメータの取得に失敗しました。{}'.format(e))
    
    #read the csv file contains the csv path to create the dataframe and create its list.
    current_file_path= os.path.dirname(__file__)
    
    # DBへ接続して、データを加工して入れていく
    logging.info("データベースへの接続開始します。")
    try:
        conn = pymysql.connect(
            host='localhost', 
            user=db_usrname, 
            password=db_pw, 
            db=db_name, 
            charset='utf8'
            )
        cur = conn.cursor()
    except Exception as e:
        logging.error('データベースへの接続失敗: {}'.format(e))

    for key, value in df_list.items():
        if key == 'folder':
           continue 
        
        print(f"Processing...{key}")
        print('--------------------------------')
        
        if ('coca-cola' in key) == True:
            replace_num = [1, 2, 3, 4, 5, 6]
            
            for num in replace_num:
                if ("_" + str(num) in value) == True:
                    value = value.replace(("_" + str(num)), "")
            df = pd.read_csv(value)
            
            if ('KO' in value) == True and ('price' in value) == True:
                dict = calc_price(df, "open") #戻し値として、成功した数、失敗した数を返す。
                result1 = plot_graph(dict, "Coca_open_price", current_file_path, cur, cur)
                
                dict = calc_price(df, "high")
                result2 = plot_graph(dict, "Coca_high_price", current_file_path, cur)
                
                dict = calc_price(df, "low")
                result3 = plot_graph(dict, "Coca_low_price", current_file_path, cur)
                
                dict = calc_price(df, "close")
                result4 = plot_graph(dict, "Coca_close_price", current_file_path, cur)
                
            elif ('PEP' in value) == True and ('price' in value) == True:
                dict = calc_price(df, "open") #戻し値として、成功した数、失敗した数を返す。
                result5 = plot_graph(dict, "PEP_open_price", current_file_path, cur)
                
                dict = calc_price(df, "high")
                result6 = plot_graph(dict, "PEP_high_price", current_file_path, cur)
                
                dict = calc_price(df, "low")
                result7 = plot_graph(dict, "PEP_low_price", current_file_path, cur)
                
                dict = calc_price(df, "close")
                result8 = plot_graph(dict, "PEP_close_price", current_file_path, cur)
        else: 
            df = pd.read_csv(value)

            # 各種データの処理を行う。(いまだ、作成中)
            if ('Ai' in key) == True:
                print("AAA")
            
            elif ('demographic' in key) == True:
                # County,State,State FIPS Code,County FIPS Code,FIPS,Total Population,Male Population,Female Population,Total Race Responses,White Alone,Black or African American Alone,Hispanic or Latino
                dict = demographic(df)
                plot_graph_graphic(dict, "demographic", current_file_path, cur)
                
            elif ('internet' in key) == True:
                print("AAA")
                
            elif ('laptop' in key) == True:
                print("AAA")
                
            elif ('sleep' in key) == True:
                print("AAA")
                
            elif ('user' in key) == True:
                print("AAA")
                
            elif ('population' in key) == True:
                print('AAA')
    
    send_option = input("Send mail?(y/n): ")

    if send_option == 'y':
        send_mail(gmail_addr, gmail_pw)

