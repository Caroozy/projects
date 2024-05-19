terraform:

- ec2:

  + configure precreated s3 backend for terraform to keep the state file
     with dynamodb to manage concurrent read write to the state file.

  + create security group inbound http and ssh and outbound all.
 
  + create an instance initialized with docker engine and run a weather app.

  
- vpc:

  + configure precreated s3 backend with dynamodb managing read and write
 
  + create vpc 

  + create public and private subnet

  + create internet gateway

  + create a route table

  + create route table association the public subnet to the internet gateway
