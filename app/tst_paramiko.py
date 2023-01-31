import paramiko
import os
from dotenv import load_dotenv

load_dotenv()
SSH_HOST = os.environ['SSH_HOST']
SSH_PORT =  os.environ['SSH_PORT']
SSH_USERNAME =  os.environ['SSH_USERNAME']
SSH_PASSWORD =  os.environ['SSH_PASSWORD']


def print_stdout_stderr(stdout,stderr):
    for o in stdout:
        print('[std]', o, end='')
    for e in stderr:
        print('[err]', e, end='')

with paramiko.SSHClient() as ssh:
    # Are you sure you want to continue connecting (yes/no)?
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # ssh接続
    ssh.connect(SSH_HOST, port=SSH_PORT, username=SSH_USERNAME, password=SSH_PASSWORD,timeout=10.0)

    # コマンド実行
    stdin, stdout, stderr = ssh.exec_command('ls -al web/close/back')
    print_stdout_stderr(stdout,stderr)

    try:
        sftp = ssh.open_sftp()
        sftp.put('c:/IMAGE/SCODE/15002-1.jpg','web/close/back/15002-1.jpg')
        for f in sftp.listdir('web/close/back'):
            print(f)
    finally:
        sftp.close()

    # コマンド実行後に標準入力が必要な場合
    # stdin.write('password\n')
    # stdin.flush()
