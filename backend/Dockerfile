FROM python:3.9

WORKDIR /app

ADD requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ADD . .
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]