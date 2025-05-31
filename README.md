REQUIREMENTS:
  - sudo access to firmware.itops.io

TO PULL AND RUN NEW DOCKER IMAGE:
- Must remove previous docker container and image
  - To see running containers or available images: sudo docker image ls / sudo docker container ls
  - To remove container/image: sudo docker container rm [id or name] / sudo docker image rm [id or name]
 
- To pull new ztp_service image: docker pull sshreve/ztp_service
 
- To run container from image: sudo docker run --name ztp_service --volume \var:/mnt/var -p 85:8000 sshreve/ztp_service:latest

TO RUN CONTAINER FROM EXISTING IMAGE:
- sudo docker container start [name]

TO ACCESS CONTAINER:
- sudo docker exec -it [name] /bin/bash
- To escape container: Ctrl + p then Ctrl + q

TO ACCESS mac_registry DB:
- Access container
- Navigate to ./mnt/ztp/configs
- Run sqlite3 mac_registry.sqlite
