
FROM python: 3.11 - slim

WORKDIR / app

COPY requirements.txt .

RUN pip install - -no - cache - dir - r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED = 1
ENV PYTHONDONTWRITEBYTECODE = 1

CMD[\python\, \you_see_me.py\]
