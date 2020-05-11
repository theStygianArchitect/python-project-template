FROM clearlinux/python:3.7
ENV WORKERS_PER_CORE 1
ENV WEB_CONCURRENCY 2
EXPOSE 8080
RUN swupd bundle-add curl
RUN pip install --upgrade pip
COPY pyproject.toml ./
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN $HOME.poetry/bin/poetry self update
RUN $HOME.poetry/bin/poetry config virtualenvs.create false
RUN $HOME.poetry/bin/poetry install
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]