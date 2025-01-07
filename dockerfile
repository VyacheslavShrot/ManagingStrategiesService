FROM python:3.11

WORKDIR /ManagingStrategiesService

# Copy Files
COPY . .

# Install Packages
RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "wsgi:app"]
