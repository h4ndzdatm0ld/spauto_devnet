ARG PYTHON_VER=3.8

FROM python:${PYTHON_VER} AS base

WORKDIR /usr/src/app

RUN pip install -U pip  && \
    curl -sSL https://install.python-poetry.org  | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

# Install project manifest
COPY poetry.lock pyproject.toml ./

# Install production dependencies
RUN poetry install --no-root

############
# Unit Tests
#
FROM base AS test_spauto

COPY . .

RUN poetry install --no-interaction

############
# Runs all necessary linting and code checks
RUN echo 'Running Flake8' && \
    flake8 . && \
    echo 'Running Black' && \
    black --check --diff . && \
    echo 'Running Yamllint' && \
    yamllint . && \
    echo 'Running pydocstyle' && \
    pydocstyle .

#############
FROM base as spauto

WORKDIR /usr/src/app/

COPY --from=test_spauto /usr/src/app /usr/src/app

ENTRYPOINT ["pytest", "--disable-pytest-warnings", "tests"]
