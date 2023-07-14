FROM python:3.9

WORKDIR /app

ADD requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.7.0/dockerize-linux-amd64-v0.7.0.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.7.0.tar.gz \
    && rm dockerize-linux-amd64-v0.7.0.tar.gz
ENV GITLAB_URL='<your_gitlab_url>'
ENV GITLAB_TOKEN='<your_token>'
ADD . .
EXPOSE 5000


# Run the application
CMD ["dockerize", "-wait", "tcp://db:3306", "-timeout", "1m", "python", "app.py"]