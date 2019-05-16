FROM python:3.6


RUN pip install boto3 flask numpy opencv-python-headless requests

COPY app app
COPY inference.py ./

ENV FLASK_APP inference.py

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
