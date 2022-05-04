from prefect import task, Flow, Parameter

@task(log_stdout=True)
def say_hello(param):
    print(f"Hello, {param}!")

with Flow("My First Flow") as flow:
    param = Parameter('param')
    say_hello(param)

flow.run(param='world') # "Hello, world!"
flow.run(param='cloud') # "Hello, cloud!"