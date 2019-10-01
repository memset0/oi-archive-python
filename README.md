# oi-archive-python

### Usage

```shell
# Require Python3.6+ and pip3 installed.
git clone https://github.com/oi-archive/source.git source
pip3 install flask markdown
sh command/start.sh
```

or 

```shell
# Require Docker installed.
wget https://github.com/oi-archive/source/archive/master.zip
mv master.zip source.zip
docker image build . -t oi-archive
# and run container with
docker container run -d -p 8080:8080 -it oi-archive
```


### Demo

![](https://i.loli.net/2019/10/02/d9EQPpqCDIGXwah.png)
![](https://i.loli.net/2019/10/02/8guPhLr6OEDsC72.png)
<!--![](https://i.loli.net/2019/10/02/eZ34TDzAihKalRC.jpg)-->
![](https://i.loli.net/2019/10/02/nSde1pLvZWNPFlJ.jpg)