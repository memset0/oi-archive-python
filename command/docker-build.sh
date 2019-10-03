docker stop oi-archive && docker rm oi-archive
git pull
if [ -d "./source" ]; then
	cd ./source
	git pull
	cd ../
fi
docker image build . -t oi-archive
docker container run --name oi-archive -d -p 8080:8080 -v $PWD/source:/app/source -it oi-archive