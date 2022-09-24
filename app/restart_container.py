import docker
from dotenv import load_dotenv
import os

def print_container_list(client):
    print("----- Container ------")
    for container in client.containers.list():
        print (container.id,container.name,)


def print_image_list(client):
    print("----- Image ------")
    for image in client.images.list():
        print (image.id,image.tags)

def restart_container(container_name):
    client = docker.from_env()

    container = container = client.containers.get(container_name)
    container.stop()
    container.start()

    return True

if __name__ == '__main__':

    load_dotenv()
    restart_container_name = os.environ['RESTART_CONTAINER_NAME'].split(',')

    client = docker.from_env()

    print_image_list(client)
    print_container_list(client)

    for container_name in restart_container_name:
        if restart_container(container_name):
            print(f"{container_name} container restarted !")
        else:
            print(f"{container_name} Ignored")
