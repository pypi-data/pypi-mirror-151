#!/bin/sh
kubectl delete namespace kubeflow
microk8s reset
microk8s.disable dashboard dns
sudo snap remove microk8s
