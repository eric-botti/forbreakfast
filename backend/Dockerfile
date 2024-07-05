FROM python:3.11.5-slim

COPY . .

RUN pip install -r requirements.txt && pip install -e .

ENTRYPOINT ["fastapi", "run", "app.py", "--port", "5230"]
