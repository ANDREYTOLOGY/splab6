FROM alpine
RUN apk add python3
COPY . .
CMD python3 main.py
