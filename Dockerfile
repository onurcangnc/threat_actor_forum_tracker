FROM python:3.11-slim

WORKDIR /app

COPY monitor_forums.py .

RUN pip install requests

CMD ["python", "monitor_forums.py"]
