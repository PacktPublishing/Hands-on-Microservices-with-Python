# Microservices installation
This is a a guide to install all of the Microservices

## Project setup
Create the following project structure
```
$ mkdir code
$ cd code
$ git clone git@github.com:PacktPublishing/Hands-on-Microservices-with-Python.git frontend.git
$ git clone git@github.com:PacktPublishing/Hands-on-Microservices-with-Python-User-Service.git user_service.git
$ git clone git@github.com:PacktPublishing/Hands-on-Microservices-with-Python-Product-Service.git product_service.git
$ git clone git@github.com:PacktPublishing/Hands-on-Microservices-with-Python-Order-Service.git order_service.git
```

You should have the following project structure:
```
~/code/
    - frontend.git/
    - user_service.git/
    - product_service.git/
    - order_service.git/
```
The deployment is done within the frontend.git folder
```
$ cd frontend.git
```

## Docker Machine (optional)
Create a Docker machine for the project
````
$ docker-machine create packt-order-management
````
Start the machine

```
$ docker-machine start packt-order-management
```
Update the shell
```
$ docker-machine env packt-order-management
$ eval $(docker-machine env packt-order-management)
```

Get the IP of the machine
```
$ docker-machine ip packt-order-management
192.168.99.100
```

## Docker Compose
Install the containers.
Run the following commands from inside the frontend.git folder.

```
$ docker-compose -f docker-compose.deploy.yml up -d
```
Check that all the containers are running
```
$ docker-compose ps 

CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                    NAMES
c193f5e1177b        frontendgit_order      "python app.py"          18 hours ago        Up 20 seconds       0.0.0.0:8083->5000/tcp   frontendgit_order_1
cb6a8f7f5e34        frontendgit_product    "python app.py"          18 hours ago        Up 21 seconds       0.0.0.0:8081->5000/tcp   frontendgit_product_1
195cdcf889d3        frontendgit_user       "python app.py"          18 hours ago        Up 20 seconds       0.0.0.0:8082->5000/tcp   frontendgit_user_1
8589f3eaa1d9        frontendgit_frontend   "/bin/sh -c 'python …"   18 hours ago        Up 21 seconds       0.0.0.0:80->5000/tcp     frontendgit_frontend_1
cee1a3965390        mysql:5.7.22           "docker-entrypoint.s…"   18 hours ago        Up 21 seconds       3306/tcp                 frontendgit_product_db_1
f63fb7b63efb        mysql:5.7.22           "docker-entrypoint.s…"   18 hours ago        Up 21 seconds       3306/tcp                 frontendgit_user_db_1
798bec4eb1b9        mysql:5.7.22           "docker-entrypoint.s…"   18 hours ago        Up 21 seconds       3306/tcp                 frontendgit_order_db_1
```

## Product database
To add products into the product database please follow [this guide](https://github.com/PacktPublishing/Hands-on-Microservices-with-Python-Product-Service/blob/master/docs/install/install.md)

# Run the application
Go to the IP address in a web browser. If you are using Docker Machine then the IP will be the IP of the machine. If you are not using Docker machine the IP will be your local host

## To rebuild the Docker images and recreate the containers
```
$ docker-compose -f docker-compose.deploy.yml build
```
Then run the following to recreate the containers
```
$ docker-compose -f docker-compose.deploy.yml up -d
```