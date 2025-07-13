FROM docker.io/python:latest

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV DEBUG=False

ENV APP_URL=http://localhost:8000

# Configuración de Asterisk AMI
ASTERISK__AMI__HOST=172.17.8.100
ENV ASTERISK__AMI__PORT=5038
ENV ASTERISK__AMI__USERNAME=dev_test
ENV ASTERISK__AMI__PASSWORD=veawad72sadwad

# Configuración de Asterisk ARI
ENV ASTERISK__ARI__HOST=127.0.0.1
ENV ASTERISK__ARI__PORT=8088
ENV ASTERISK__ARI__USERNAME=admin
ENV ASTERISK__ARI__PASSWORD=admin

ENV JWT__PRIVATE_KEY=PATH_TO_PRIVATE_KEY
ENV JWT__PUBLIC_KEY=PATH_TO_PUBLIC_KEY
ENV JWT__ALGO=RS256

COPY pyproject.toml .
RUN pip install .

WORKDIR /app
COPY . /app

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
