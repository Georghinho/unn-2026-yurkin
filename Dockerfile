FROM python:3.14-slim

WORKDIR /app

COPY bot/ bot/

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "bot"]
