
ARG PYTHON_VER
FROM python:${PYTHON_VER}-alpine


ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apk --no-cache upgrade && \
    apk add --no-cache --virtual .build-deps \
        build-base \
        musl-dev  && \
    apk --update --no-progress add git zsh postgresql-client curl

# I like a nice shell in my contaners
RUN mkdir -p /root/.antigen
RUN curl -L git.io/antigen > /root/.antigen/antigen.zsh
COPY development/.zshrc /root/.zshrc
# Set up ZSH as (we just need to start it, it'll initialise our setup itself)
RUN /bin/zsh /root/.zshrc


WORKDIR /source
# Copy in the source code ans install poetry
COPY . /source/

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.2
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install --no-ansi

# Now clean up the image by remving the gcc/package build dependencies
RUN apk del .build-deps

COPY development/entrypoint.sh /opt/entrypoint.sh
RUN ["chmod", "+x", "/opt/entrypoint.sh"]
ENTRYPOINT ["/opt/entrypoint.sh"]
