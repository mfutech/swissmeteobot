FROM python:3.6-alpine
WORKDIR /usr/src/app
RUN apk add --update --no-cache g++ gcc libxslt-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./SwissMeteoBot.py" ]