FROM python:3

WORKDIR /app

COPY requirements.txt ./

RUN pip install requirements.txt

COPY . .

ENV PORT=80

EXPOSE 80

CMD ["python", "manage.py", "runserver"]

