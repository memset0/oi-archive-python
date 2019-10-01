FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip3 install flask markdown
EXPOSE 8080
CMD sh command/start.sh