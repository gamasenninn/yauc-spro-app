import sys
import os
import subprocess
from dotenv import load_dotenv

import prefect
from prefect import task, Flow
from prefect.run_configs import LocalRun

dir_name = os.path.dirname(os.path.abspath(__file__))

load_dotenv()
cmd_anl = os.environ['COMMAND_ANALIZE']
log_anl = os.environ['LOG_ANALIZE']
cmd_image = os.environ['COMMAND_IMAGE']
log_image = os.environ['LOG_IMAGE']

def get_lines(cmd):

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline().decode('utf-8')
        if line:
            yield line

        if not line and proc.poll() is not None:
            break

@task
def t_copy_analize(t):
    #---- copy analize data ----- 
    with open(log_anl,'w') as f:
        for line in get_lines(cmd=cmd_anl):
            sys.stdout.write(line)
            f.write(line)
    return True

@task
def t_copy_image(t):
    #---- copy Image data ----- 
    with open(log_image,'w') as f:
        for line in get_lines(cmd=cmd_image):
            sys.stdout.write(line)
            f.write(line)
    return True

with Flow("rclone-copy",run_config=LocalRun(working_dir=dir_name)) as flow:
    #init_driver()
    t1 = t_copy_analize('')
    t2 = t_copy_image(t1)


if __name__ == '__main__':

    args = sys.argv

    dir_name = os.path.dirname(os.path.abspath(__file__))
    print(dir_name)

    #flow.run_config = LocalRun(working_dir=dir_name)
    if len(args) >1 :
        if args[1] == 'reg':
            flow.register(project_name="hks")
    else:
        flow.run()
    pass
