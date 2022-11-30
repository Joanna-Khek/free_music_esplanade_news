FROM python:3.9

WORKDIR /app

# Install Python dependencies.
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD python main.py