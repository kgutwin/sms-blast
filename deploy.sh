#!/bin/bash

set -e

if [[ -z $1 ]]; then
    echo Usage: $0 leaderkey
    exit 1
fi

STACK_NAME=sms-blast
CFTEMPLATES=$(aws s3api list-buckets --output text --query 'Buckets[*].[Name]' \
                  | egrep '^cf-templates' | head -1)

#sam build
sam package \
    --s3-bucket $CFTEMPLATES \
    --output-template-file packaged-template.yml
aws cloudformation deploy \
    --stack-name $STACK_NAME \
    --template-file packaged-template.yml \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
    --parameter-overrides "LeaderKey=$1"

aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs' \
    --output text
