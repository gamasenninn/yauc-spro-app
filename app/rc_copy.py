import sys
import subprocess


cmd_anl = 'rclone copy  -v  C:\OneDrive\ドキュメント\PY_SRC\YH_ANL_CLI_SEL\graph lolipop_ftp:analize'
log_anl = "rc_analize.log"

def get_lines(cmd):

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline().decode('cp932')
        if line:
            yield line

        if not line and proc.poll() is not None:
            break


if __name__ == '__main__':
    with open(log_anl,'w') as f:
        for line in get_lines(cmd=cmd_anl):
            sys.stdout.write(line)
            f.write(line)
