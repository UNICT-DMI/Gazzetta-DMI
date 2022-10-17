docker stop bot
docker rm bot
docker build --tag gazzetta-dmi .
docker run -it \
--name bot \
--mount type=bind,source="$(pwd)/data",destination=/app/data \
gazzetta-dmi