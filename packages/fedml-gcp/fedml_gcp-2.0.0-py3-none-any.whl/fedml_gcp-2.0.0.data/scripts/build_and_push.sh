#!/usr/bin/env bash
project_name=$1
image=$2
profile_name=$3
KEY_FILE=$4

# chmod +x ${image}/SKLearn/serve
gcloud auth activate-service-account ${profile_name} --key-file=${KEY_FILE}
gcloud auth configure-docker

export KUBECONFIG=kubeconfig.yml
kubectl get deployments
if [ $? -ne 0 ]; then 
    echo "ERROR: kubeconfig.yml doesn't contain correct connection details for Kyma"
    exit 1
fi


docker build -t gcr.io/${project_name}/${image} .
if [ $? -ne 0 ]; then
    echo 'ERROR: docker build failed!'    
    exit 1
fi

docker push gcr.io/${project_name}/${image}
if [ $? -ne 0 ]; then
    echo 'ERROR: docker push failed!'    
    exit 1
fi


kubectl apply -f deployment.yaml

kubectl rollout status deployment/${image}
if [ $? -ne 0 ]; then
    echo 'ERROR: model deployment failed!'    
    exit 1
fi