FROM python:3-alpine
RUN apk --update add build-base libzmq musl-dev python3 python3-dev zeromq-dev libxml2-dev libxslt-dev
EXPOSE 8089

ARG BUILD_COMMIT_SHA1
ARG BUILD_COMMIT_DATE
ARG BUILD_BRANCH
ARG BUILD_DATE
ARG BUILD_REPO_ORIGIN
 
ENV BUILD_COMMIT_SHA1=$BUILD_COMMIT_SHA1
ENV BUILD_COMMIT_DATE=$BUILD_COMMIT_DATE
ENV BUILD_BRANCH=$BUILD_BRANCH
ENV BUILD_DATE=$BUILD_DATE
ENV BUILD_REPO_ORIGIN=$BUILD_REPO_ORIGIN

WORKDIR /src
ADD . /src
RUN pip install pip -U;pip install -r requirements.txt

RUN apk del build-base musl-dev python3-dev zeromq-dev

ENTRYPOINT ["locust"]
CMD ["-f", "saturation-load.py"]