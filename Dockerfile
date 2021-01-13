FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install
COPY . /app
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]
