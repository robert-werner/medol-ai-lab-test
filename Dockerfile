FROM python:3.12-slim

ADD . /opt/medol
=

RUN cd /opt/medol && pip install --no-cache-dir -e .

CMD ["fastapi", "run", "--port", "8080", "/opt/medol/app/main.py"]