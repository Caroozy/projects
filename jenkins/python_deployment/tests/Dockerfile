From joyzoursky/python-chromedriver:3.9-alpine AS build
WORKDIR /test/
COPY test_reach.py test_requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r test_requirements.txt
RUN apk update
RUN apk add binutils
RUN pyinstaller --onefile test_reach.py

From joyzoursky/python-chromedriver:3.9-alpine
COPY --from=build /test/dist/test_reach / 
ENTRYPOINT /test_reach
