import sys
import os
import subprocess
from dotenv import load_dotenv

import prefect
from prefect import task, Flow
from prefect.run_configs import LocalRun

from restart_container import restart_container

dir_name = os.path.dirname(os.path.abspath(__file__))

load_dotenv()
restart_container_name = os.environ['RESTART_CONTAINER_NAME'].split(',')

@task
def t_restart_container(t):
    #---- copy analize data ----- 
    for container_name in restart_container_name:
        if restart_container(container_name):
            print(f"{container_name} container restarted !")
        else:
            print(f"{container_name} Ignored")
    return True

@task
def t_end(t):
    #---- copy Image data ----- 
    print("restart container task end")
    return True

with Flow("restart_container",run_config=LocalRun(working_dir=dir_name)) as flow:
    #init_driver()
    t1 = t_restart_container('')
    t2 = t_end(t1)


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
