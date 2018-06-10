# Docker Machine

Create a Docker machine
```
$ docker-machine create packt-order-management
```

Set the Docker machine to the current shell

```
$ eval $(docker-machine env packt-order-management)
```

Get the IP of the docker machine
```
$ docker-machine ip packt-order-management
```

# Docker composer
Run the containers
```
$ docker-compose up -d
```
