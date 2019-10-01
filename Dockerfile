FROM python:3.7
COPY . /app
WORKDIR /app
RUN sh -c 'pip3 install flask markdown && unzip source.zip && mv source-master source'
EXPOSE 8080
CMD sh command/start.sh