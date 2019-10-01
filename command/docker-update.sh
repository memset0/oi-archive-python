docker rm $(docker stop $(docker ps -a -q --filter ancestor=oi-archive --format="{{.ID}}"))
git pull
docker image build . -t oi-archive
docker container run -p 8080:8080 -it oi-archive