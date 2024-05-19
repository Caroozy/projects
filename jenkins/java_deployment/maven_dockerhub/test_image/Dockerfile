FROM ubuntu:22.04
WORKDIR /app
ARG SONAR_TOKEN
ADD ./pom.xml .
WORKDIR /app/src
ADD ./src .
WORKDIR /app
RUN apt update && apt install -y xvfb maven openjdk-11-jdk
RUN xvfb-run mvn test sonar:sonar \
                    -Dsonar.projectKey=calculator \
                    -Dsonar.host.url=http://172.31.24.106 \
                    -Dsonar.login=${SONAR_TOKEN}
