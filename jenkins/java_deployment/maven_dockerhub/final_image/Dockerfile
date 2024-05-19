FROM ubuntu:22.04 AS build
WORKDIR /app
ADD ./pom.xml .
WORKDIR /app/src
ADD ./src .
WORKDIR /app
RUN apt update && apt install -y maven openjdk-11-jdk
RUN mvn package -DskipTests

FROM ubuntu/jre:17-22.04_41
WORKDIR /app
COPY --from=build /app/target/calc.jar .
CMD java -jar /app/calc.jar
