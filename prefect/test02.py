import prefect
from prefect import task, Flow

@task
def hello_task():
    logger = prefect.context.get("logger")
    logger.info("Hello world!")

@task
def hello_task2():
    logger = prefect.context.get("logger")
    logger.info("Hello world!-------2")


#flow = Flow("hello-flow", tasks=[hello_task])
with Flow("hello2-flow") as flow:
    hello_task()
    hello_task2()

flow.register(project_name="test")