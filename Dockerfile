FROM alpine:3.7

RUN apk add --no-cache python3

RUN pip3 install robobrowser

COPY get_urls.py /workspace/

ENTRYPOINT ["/usr/bin/python3.6", "/workspace/get_urls.py"]
