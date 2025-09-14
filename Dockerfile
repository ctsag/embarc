FROM python:3.13-slim AS builder

RUN mkdir /app
WORKDIR /app
 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
 
RUN pip install --upgrade pip
 
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt



FROM python:3.13-slim

ENV SECRET_KEY='+nu-j#eduxif!@awsb5ribcwy!0tpwpo2-b=8#g$49e4knw3dk'
ENV DEBUG=True
ENV ALLOWED_HOSTS=localhost

RUN useradd -m -r appuser && mkdir /app && chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
WORKDIR /app

COPY --chown=appuser:appuser . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/embarc
USER appuser

RUN python manage.py makemigrations adventures
RUN python manage.py migrate

EXPOSE 8001
 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
