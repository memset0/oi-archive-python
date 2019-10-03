if [ -d "./source" ]; then
	cd ./source
	git pull
	cd ../
fi
docker exec -it oi-archive git pull