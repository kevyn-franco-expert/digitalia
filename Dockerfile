FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=ChallengeDigitalia.settings
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "ChallengeDigitalia.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
