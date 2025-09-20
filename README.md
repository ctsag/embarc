# embarc
Organize your mini projects into adventures and your tasks into missions

# running the application on docker
Create a volume
```commandline
docker volume create embarc-db
```
Build the image
```commandline
docker build -t embarc .
```
Run the container
```commandline
docker run --name embarc -d -p 8001:8001 -v embarc-db:/app/embarc/db embarc
```
Use the application at http://localhost:8001
