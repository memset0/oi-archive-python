FROM python:3.7
COPY . /app
WORKDIR /app
RUN sh -c 'pip3 install --default-timeout=3600 flask markdown'
RUN sh -c 'if [[ ! -f "/app/config.json" ]]; then cp /app/config.example.json /app/config.json; fi'
EXPOSE 8080
CMD sh command/start.sh