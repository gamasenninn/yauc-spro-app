from random import randint
from prefect import task, Flow

@task
def random_list():
    return [i for i in range(randint(1, 10))]

@task
def squared(x):
    return x ** 2

@task
def sum_up(l):
    print(f"Squared results: {l}")
    print(f"Sum: {sum(l)}")

with Flow('DynamicFlow') as flow:
    l = random_list()
    squared_res = squared.map(l)
    sum_res = sum_up(squared_res)

#flow.run()
flow.register(project_name="test")