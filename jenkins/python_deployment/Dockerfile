FROM python:3.10-slim AS build
ADD app /app
WORKDIR /app/
ADD ./build_requirements.txt .
RUN pip install --upgrade pip 
RUN pip install -r build_requirements.txt
RUN apt update && apt install -y binutils
RUN pyinstaller --onefile --hidden-import=gunicorn.glogging --hidden-import=gunicorn.workers.sync wsgi_app.py

FROM python:3.10-slim
WORKDIR /app/
COPY --from=build /app/dist/wsgi_app .
ADD templates ./templates
ENTRYPOINT /app/wsgi_app
