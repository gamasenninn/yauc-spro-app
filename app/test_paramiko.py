import paramiko
import os
from dotenv import load_dotenv

load_dotenv()
SSH_HOST = os.environ['SSH_HOST']
SSH_PORT =  os.environ['SSH_PORT']
SSH_USERNAME =  os.environ['SSH_USERNAME']
SSH_PASSWORD =  os.environ['SSH_PASSWORD']



with paramiko.SSHClient() as ssh:
    # 初回ログイン時に「Are you sure you want to continue connecting (yes/no)?」と
    # きかれても問題なく接続できるように。
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # ssh接続
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USERNAME, password=SSH_PASSWORD)

    # コマンド実行
    stdin, stdout, stderr = ssh.exec_command('ls -al')

    # コマンド実行後に標準入力が必要な場合
    # stdin.write('password\n')
    # stdin.flush()

    # 実行結果を表示
    for o in stdout:
        print('[std]', o, end='')
    for e in stderr:
        print('[err]', e, end='')