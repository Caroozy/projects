# A display of little projects:

## All of the samples were developed using Amazons Web services
## mainly ec2 machines with configured security groups to the different projects port routing.


### Projects:

####  Terraform:


    ec2:

      - s3 bucket to store state file and act as backend
      - dynamodb table to manage concurrent read and write capacity
	  - security group for the instance
	  - ec2 instance initialized manually with docker and running a weather app


    vpc:

	  - vpc
	  - private and public subnet
	  - internet gateway
	  - route table


####  Ansible Python weather app deployment with nginx:
    
    - ensure nginx is installed (pointless but done for practice)
    - ensure dependencies and container runtime installed
    - replace running container with given version container image

####  Kubernetes Python weather app deployment with autoscaling:
    
    - initiate kubernetes cluster using kubeadm
    - join nodes to the cluster
    - install pod network
    - install metrics server
    -- create deployment for the app and add horizontal pod scaling to it

####  AWS CodePipeline using CodeCommit -> CodeBuild -> CodeDeploy:

    * full AWS integrated pipeline
    - Codecommit repository triggering pipeline for events
    - build an image and save it as a tar for moving an artifact environments
    - deploy the image by replacing the previously running container with itself

####  Jenkins:

    java:

	- Maven + SonarQube -> JFrog Artifactory (.tar file)

	    * All build steps were made inside a single container build (just for practice)
	    * delivers speedy builds including testing and delivery

	    - clone remote repository development branch
	    - execute maven package with tests and sonarqube scan
	    - upload jar if maven package successful to JFrog artifactory
	    - final image is a runtime environment with the jar
	 
	- Maven + SonarQube -> DockerHub (Container image)

	    - clone remote repository development branch
	    - test source code by building a test container
	    - build a final container image as artifact
	    - push artifact to dockerhub

	python:

	- UnitTest + Selenium -> DockerHub + Deploy manually

	    - clone remote repository development branch
	    - Containerize the application and tests
	    - Run app detached and tests not detached waiting for tests exit status
	    - Push app image to dockerhub
	    - replace running container as deployment
