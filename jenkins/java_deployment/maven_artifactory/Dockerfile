FROM ubuntu:22.04 AS build
RUN apt update && apt install -y openjdk-11-jdk maven xvfb git curl
WORKDIR /
RUN curl -fL https://install-cli.jfrog.io | sh
RUN git clone --branch development http://172.31.26.112/root/calculator.git
WORKDIR /calculator
ARG JFROG_TOKEN=$JFROG_TOKEN
ARG SONAR_TOKEN=$SONAR_TOKEN
RUN xvfb-run mvn package sonar:sonar \
                    -Dsonar.projectKey=calculator \
                    -Dsonar.host.url=http://172.31.24.106 \
                    -Dsonar.login=${SONAR_TOKEN}
RUN jf rt upload --url http://172.31.26.212/artifactory --access-token ${JFROG_TOKEN} target/calc.jar calculator

FROM ubuntu/jre:11-22.04_11
WORKDIR /app
COPY --from=build /calculator/target/calc.jar /app/
CMD java -jar /app/calc.jar
