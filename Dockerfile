FROM python:3.11-slim

USER root

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir Flask
RUN pip install uvicorn
RUN pip install -r requirements.txt

EXPOSE 8000

#ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]