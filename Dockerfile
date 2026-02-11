FROM python:3.12

RUN addgroup coder
RUN useradd -g coder coder

COPY . /home/coder/coder-fastapi
WORKDIR /home/coder

RUN pip install -e coder-fastapi[test]

WORKDIR /home/coder/coder-fastapi

ENTRYPOINT ["pytest", "--cov=coderfastapi", "-n", "logical", "-q", "--cov-report", "term-missing"]
