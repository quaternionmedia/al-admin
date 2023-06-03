FROM python

WORKDIR /app

RUN mkdir -p data

COPY pyproject.toml README.md ./
COPY admin admin

RUN pip3 install .[production]

CMD ["uvicorn", "admin.app:app", "--host", "0.0.0.0", "--port", "80"]
