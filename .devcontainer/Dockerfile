FROM mcr.microsoft.com/devcontainers/python:0-3.11

USER vscode
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version=0.12.17
ENV PATH "/home/vscode/.poetry/bin:$PATH"
