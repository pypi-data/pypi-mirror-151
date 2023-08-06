#!/usr/bin/env bash
image=$1
full_link=$2
profile_name=$3

chmod +x ${image}/SKLearn/serve

export KUBECONFIG=kubeconfig.yml
kubectl get deployments
if [ $? -ne 0 ]; then 
    echo "ERROR: kubeconfig.yml doesn't contain to correct connection details for Kyma"
    exit 1
fi

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${image}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${image}" > /dev/null
    if [ $? -ne 0 ]
    then
        echo 'Error creating repository'
        exit 1
    fi
fi

# Get the region defined in the current configuration (default to us-west-2 if none defined)
region=$(aws configure get region)

# Get the account number associated with the current IAM credentials
account=$(aws sts get-caller-identity --query Account --output text)
if [ $? -ne 0 ]
then
    exit 255
fi

aws ecr get-login-password --region ${region}  --profile ${profile_name} | docker login --username AWS --password-stdin "${account}".dkr.ecr."${region}".amazonaws.com
if [ $? -ne 0 ]; then
    echo 'ERROR: docker login aws failed!'    
    exit 1
fi

#get login command form ECR and execute it directly. and store password as secret.
kubectl delete secret "${profile_name}-aws-ecr" --ignore-not-found
password=$(aws ecr get-login-password --region ${region} --profile ${profile_name})
kubectl create secret docker-registry "${profile_name}-aws-ecr" --docker-server="${account}".dkr.ecr."${region}".amazonaws.com --docker-username='AWS' --docker-password=${password}
if [ $? -ne 0 ]; then
    echo "ERROR: couldn't create secret in Kyma!"  
    exit 1
fi

aws ecr get-login-password --region ${region} --profile ${profile_name} | docker login --username AWS --password-stdin ${full_link}
docker build -t ${image} ${image}
if [ $? -ne 0 ]; then
    echo 'ERROR: docker build failed!'    
    exit 1
fi

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"
docker tag ${image} ${fullname}
if [ $? -ne 0 ]; then
    echo 'ERROR: docker tag failed!'    
    exit 1
fi

docker push ${fullname}
if [ $? -ne 0 ]; then
    echo 'ERROR: docker push failed!'    
    exit 1
fi


kubectl apply -f ${image}/deployment.yaml

kubectl rollout status deployment/${image}
if [ $? -ne 0 ]; then
    echo 'ERROR: model deployment failed!'    
    exit 1
fi