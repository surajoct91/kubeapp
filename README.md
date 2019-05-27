This application is a small simple Python flask + MySQL that gives the value of last name from a prepopulated first name field search if it exists.

This also has been packaged as Helm charts for individual application and can be directly run using help install with tiller by running mysql package first and then the webapp package.

There are 2 ways to run this using kubectl and minikube. First is individually getting into each microservice layer folder and starting them one by one and another one is running from a single file from the application directory.

===========

Pre-requisites:

1) You need minikube installed + any driver (here its virtualbox) to run the kubernetes cluster.

2) You need to get the minikube clusters docker context before building any images using the following command from the terminal:

~# eval $(minikube docker-env)

Note: this is valid for the running terminal and will need to be done if you open up a new one to run commands.

3) Create pythonapp and mysql database docker container images from the DockerFiles directory like:

# ~/DockerFiles/mysql# docker build -t appmysql .

# ~/DockerFiles/application# docker build -t pythonapp .

===============
Option - 1: Running as individual step by step service:

1) ~# minikube start --vm-driver=virtualbox
* minikube v1.1.0 on linux (amd64)
* Creating virtualbox VM (CPUs=2, Memory=2048MB, Disk=20000MB) ...
* Configuring environment for Kubernetes v1.14.2 on Docker 18.09.6

	
2) ~# eval $(minikube docker-env)

3) Build mysql Docker image using the name "appmysql"

# ~/DockerFiles/mysql# docker build -t appmysql .

4) Similarly build the pythonapp image  "pythonapp"

:~/DockerFiles/application# docker build -t pythonapp .

5) Apply secrets to be used from the root directory:

~/# kubectl apply -f secret.yml

6) Apply Persistent volume for Mysql DB:

~/mysql# kubectl apply -f pv-persistent-mysql-volumeclaim.yml

7) Apply mysqlDB's deployment file:

~/mysql# kubectl apply -f deployment.yml

8) Apply MySQLDB's service file

~/mysql# kubectl apply -f service.yml 

9) Now move to the webapp directory and apply the deployment for the python app:

~/webapp# kubectl apply -f deployment.yml

10) Similarly deploy the service:

~/webapp# kubectl apply -f service.yml


11) List the services and get the minikube's ip and NodePort using which you can browse in the browser: 

~/webapp# kubectl get svc
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP   10.96.0.1     <none>        443/TCP          20m
mysql-app    ClusterIP   None          <none>        3306/TCP         59s
python-app   NodePort    10.104.98.1   <none>        5000:30331/TCP   16s

~/webapp# minikube service python-app --url
http://192.168.99.105:30331



12) The Database only has 2 values in the First Name column for the purpose of demonstration: 

    a) Suraj and b) Steve 

You should get the values for last name for these 2 above values and for anything else it should say not found in the database.

===================

Option - 2: This whole thing can be done via a single yml file from the application directory under root: 

~/application# kubectl apply -f webapp.yml 
secret/mysql-pass created
persistentvolumeclaim/mysql-pv-claim created
deployment.apps/apache-mysql created
service/mysql-app created
deployment.apps/webapp created
service/python-app created


~/application# kubectl get svc
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          28m
mysql-app    ClusterIP   None             <none>        3306/TCP         12s
python-app   NodePort    10.108.136.171   <none>        5000:32730/TCP   12s
root@laptop46:~/application# minikube service python-app --url
http://192.168.99.105:32730


================
