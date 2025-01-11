#!/bin/bash
kubectl create ns postgresql
kubectl -n postgresql create secret generic postgresql \
    --from-literal POSTGRES_USER="admin" \
    --from-literal POSTGRES_PASSWORD="GoofyAdmin" \
    --from-literal POSTGRES_DB="dussdb" \
    --from-literal REPLICATION_USER="replicationuser" \
    --from-literal REPLICATION_PASSWORD="replicationPassword"
kubectl -n postgresql apply -f DussDB/postgresql.yaml

kubectl apply -f WebApp/webapp.yaml

kubectl apply -f RentalAppPyServer/rental-server.yaml
# kubectl port-forward svc/grpc-rental-server-svc 50051:50051

# kubectl apply -f nginx-ingress.yaml