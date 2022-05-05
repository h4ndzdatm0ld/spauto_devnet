#############
# Dependencies
# This base stage just installs the dependencies required for production
# without any development deps.
ARG PYTHON_VER=3.8

FROM python:${PYTHON_VER} AS base

WORKDIR /usr/src/app

# Install poetry for dep management
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="$PATH:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

# Install project manifest
COPY poetry.lock pyproject.toml ./

# Install production dependencies
RUN poetry install --no-dev --no-root

############
# Unit Tests
#
# This test stage runs true unit tests (no outside services) at build time, as
# well as enforcing codestyle and performing fast syntax checks. It is built
# into an image with docker-compose for running the full test suite.
FROM base AS test_spauto

RUN poetry install --no-interaction --no-root

COPY . .
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

COPY pyproject.toml poetry.lock ./

# Get a copy of all the files from the test stage
COPY --from=test_spauto /usr/src/app /usr/src/app

ENTRYPOINT ["pytest", "--disable-pytest-warnings", "tests"]
