FROM rabbitmq:latest
RUN apt update && apt install -y vim nano
EXPOSE 5672
EXPOSE 15671
EXPOSE 4369
ADD start.sh "/start.sh"

CMD "/start.sh"