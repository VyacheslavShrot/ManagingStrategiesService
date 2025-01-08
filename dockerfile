FROM python:3.11

WORKDIR /ManagingStrategiesService

# Copy Files
COPY . .

# Install Packages
RUN pip install -r requirements.txt

ENV FLASK_APP=wsgi.py

ENTRYPOINT ["sh", "-c", "flask db migrate && flask db upgrade && gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app"]
