FROM docker.io/python:latest

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV DEBUG=True

ENV APP_URL=http://localhost:8000

# Configuración de Asterisk AMI
ENV ASTERISK__AMI__HOST=127.0.0.1
ENV ASTERISK__AMI__PORT=5038
ENV ASTERISK__AMI__USERNAME=admin
ENV ASTERISK__AMI__PASSWORD=admin

# Configuración de Asterisk ARI
ENV ASTERISK__ARI__HOST=127.0.0.1
ENV ASTERISK__ARI__PORT=8088
ENV ASTERISK__ARI__USERNAME=admin
ENV ASTERISK__ARI__PASSWORD=admin

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
