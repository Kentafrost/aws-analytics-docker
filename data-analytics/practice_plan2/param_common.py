import boto3

ssm_client = boto3.client('ssm', region_name='ap-southeast-2')

db_name = ssm_client.get_parameter(Name='db_dbname', WithDecryption=True)['Parameter']['Value']
db_tbl = ssm_client.get_parameter(Name='db_tablename', WithDecryption=True)['Parameter']['Value']
db_usrname = ssm_client.get_parameter(Name='db_username', WithDecryption=True)['Parameter']['Value']
db_pw = ssm_client.get_parameter(Name='db_pw', WithDecryption=True)['Parameter']['Value']
path = ssm_client.get_parameter(Name='folder_path', WithDecryption=True)['Parameter']['Value']

gmail_addr = ssm_client.get_parameter(Name='my_main_gmail_address', WithDecryption=True)['Parameter']['Value']
gmail_pw = ssm_client.get_parameter(Name='my_main_gmail_password', WithDecryption=True)['Parameter']['Value']