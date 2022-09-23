import docker
client = docker.from_env()

for image in client.images.list():
    print (image.id,image.tags)

for container in client.containers.list():
    print (container.id,container.name,)

container = container = client.containers.get('selchrome')
container.stop()
container.start()
