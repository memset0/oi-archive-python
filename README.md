# oi-archive-python

### Usage

Require Python3.6+ and pip3 installed.

```
git clone https://github.com/oi-archive/source.git source
pip3 install flask markdown
sh command/start.sh
```

or 

Require Docker installed.

```
wget https://github.com/oi-archive/source/archive/master.zip
unzip master.zip
mv source-master source
sh command/docker-build.sh
```

and run container with

```
docker container run -d -p 8080:8080 -it oi-archive
```