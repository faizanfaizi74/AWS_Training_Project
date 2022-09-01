FROM thoom/pyresttest

WORKDIR /app

COPY ./mytests /app

ENTRYPOINT ["pyresttest"]

CMD ["https://6vev67kynl.execute-api.us-east-1.amazonaws.com", "api_test.yml"]

