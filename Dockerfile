FROM python:3.7
COPY . /app
WORKDIR /app
RUN bash -c 'if [[ ! -f "/app/config.json" ]]; then cp /app/config.example.json /app/config.json; fi'
RUN bash -c 'pip3 install --default-timeout=3600 flask markdown -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com'
EXPOSE 8080
CMD sh command/start.sh