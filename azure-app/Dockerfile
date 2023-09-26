FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

## If using open source models, load them here in Docker build
# RUN python install.py

EXPOSE 80

ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=80", "--server.address=0.0.0.0"]

