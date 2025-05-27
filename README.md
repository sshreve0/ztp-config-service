To be run on firmware.itops.io

TO PULL AND RUN NEW DOCKER IMAGE:
- must remove previous docker container and image
  - to see running containers or available images: sudo docker image ls / sudo docker container ls
  - to remove container/image: sudo docker container rm [id or name] / sudo docker image rm [id or name]
 
- to pull new ztp_service image: docker pull sshreve/ztp_service
 
- to run container from image: sudo docker run --name ztp_service --volume \var:/mnt/var -p 85:8000 sshreve/ztp_service:latest

TO RUN CONTAINER FROM EXISTING IMAGE:
- sudo docker container start [name]
