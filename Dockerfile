FROM python:3.7
COPY . /app
WORKDIR /app
RUN sh -c 'pip3 install flask markdown && wget https://github.com/oi-archive/source/archive/master.zip && unzip master.zip && mv source-master source'
EXPOSE 8080
CMD sh command/start.sh