FROM python:3.7
COPY . /app
WORKDIR /app
RUN sh -c 'pip3 install --default-timeout=3600 flask markdown'
EXPOSE 8080
CMD sh command/start.sh