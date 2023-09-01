FROM python:3.11

WORKDIR /app


# Копируем содержимое текущей директории (C0ver_letter_bot) в /app
RUN mkdir /C0ver_letter_bot
WORKDIR /app/C0ver_letter_bot
COPY ./pyproject.toml ./poetry.lock ./.python-version ./Agent ./README.md ./

RUN mkdir /hh
COPY ./hh/__init__.py /app/C0ver_letter_bot/hh

RUN mkdir /tests
COPY ./tests/__init__.py /app/C0ver_letter_bot/tests

RUN pip install poetry


RUN mkdir /main
WORKDIR /app/C0ver_letter_bot/main
COPY ./main/main.py ./main/rezume_parsing.py ./main/vacancy_parsing.py ./main/config.py ./


RUN poetry install


ENTRYPOINT ["poetry", "run", "python", "main.py"]