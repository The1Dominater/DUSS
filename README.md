# Final Project Team 101
### Members: Dominic Galgano
### Goals
 - Build a working rental ski shop service portal
 - Demonstrate datacenter computing knowledge
    - Kubernetes/cluster deployment and management
    - HTTP vs gRPC
    - Dataframes vs SQL
    - Load Balancing, scaling, and resource utilization
### Description
Stakeholders:
 - Ski/Snowboard shops
 - Equipment renters
 - Investors in Shop
The shop can have multiple terminal interfaces open sends data to a database. Data will mostly be text info about renters.

Functionally Features:
 - Submit a reservation to the shop using their online website 
 - View the shop's selection of ski goods
 - Find reservations and customers using RentalApp
 - Calculate customers age, DIN, and total bill based on information provided during reservation 

### Operations Guide
1. Deploy a k8s cluster
    - Initiate kubernetes cluster(I used the default one provided with docker desktop)
    - Apply the service, ingress, deployment, and statefulset yaml files for each application
        - setup_cluster.sh contain all the commands I used to run this
        - nginx may need addition file applied using: `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml`

2. Create a reservation
    - This is the most developed feature, which uses a pod containing a flask webserver to server content to the user can be accessed by going to `localhost` but NOT `127.0.0.1` for reasons I could not determine
    - Users need to login to access this page(they can create an account using the sign-up page if needed)
    - When a user inputs information, the flask web app does a backend check on the inputs and adds them to the
      postgreSQL database if they meet the requirements

3. Fullfil a reservation
    - Using the locally run rentalApp, the employees can retrieve customer's reservations from the cluster pod containing the database
    - Employees can use three main functions CalculateAge, CalculateDIN, and CalculateTotal, which uses gRPC protocols to interact with a cluster based server for rental calculations
        - I was unable to get this to work through the nginx ingress controller so I just used `kubectl port-forward svc/grpc-rental-server-svc 50051:50051`
  labels:

4. Manage cluster
    - Admin's can monitor cluster information using the Grafana dashboard, which is provided data by Prometheus running on the cluster by going to localhost:3000
        - This is not automated in my files but can be achieved by following this tutorial: https://www.youtube.com/watch?v=dzBGhlF4M1U
    - Admin's automatically have loads distrubuted between pods in the cluster using nginx proxy
