# 2 Serverless function in YC with trigger
0.0 Get Yc.OAuth token. It is necessary to manage YC resources from CLI. We will use Terrarform to create new S3 bucket

https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token

0.1 Create service account for terrafrom role(name below will be service-account-for-cf)
```
export SERVICE_ACCOUNT=$(yc iam service-account create --name service-account-for-cf \
--description "service account for cloud functions" \
--format json | jq -r .)

# get list of current accounts
yc iam service-account list 

# check variable
echo $SERVICE_ACCOUNT

# also write ID in variable

SERVICE_ACCOUNT_ID="ID FROM OUTPUT ABOVE"
```
0.2 Add role to a created service account
```
echo "export FOLDER_ID=$(yc config get folder-id)" >> ~/.bashrc && . ~/.bashrc 

yc resource-manager folder add-access-binding $FOLDER_ID \
--subject serviceAccount:$SERVICE_ACCOUNT_ID \
--role editor 

```
1. Create ACCESS_KEY and SECRET_KEY for service account to access S3 bucket

```
yc iam access-key create --service-account-name service-account-for-cf
```

You will get: 
```
access_key:
    id: ajefraollq5puj2tir1o
    service_account_id: ajetdv28pl0a1a8r41f0
    created_at: "2021-08-23T21:13:05.677319393Z"
    key_id: BTPNvWthv0ZX2xVmlPIU      < ------------------ It is your ACCESS_KEY
secret: cWLQ0HrTM0k_qAac43cwMNJA8VV_rfTg_kd4xVPi < ------- It is your SECRET_KEY

```
Also add this save them as local variables:

```
ACCESS_KEY=<ACCESS_KEY>
SECRET_KEY=<SECRET_KEY>
```

2. Using terrafrom create a bucket in Yc (file main.tf). PLEASE do NOT forget modify with YOUR ENV!

```
terraform init
terraform plan
terraform apply 
```
3. Add bucket name to your variables

```
BUCKET_NAME=bucket-for-trigger
```
4. Create Serverless function

```
yc serverless function version create \
--function-name my-first-function \
--memory 256m \
--execution-timeout 5s \
--runtime python37 \
--entrypoint index.handler \
--service-account-id $SERVICE_ACCOUNT_ID \
--source-path my-first-function.zip \
--environment ACCESS_KEY=$ACCESS_KEY \
--environment SECRET_KEY=$SECRET_KEY \
--environment BUCKET_NAME=$BUCKET_NAME 

# for check if it is created
yc serverless function version list --function-name my-first-function 

# for manually run this function
yc serverless function invoke <FUNCTION ID>

```

5. Make current function public

```
#make public
yc serverless function allow-unauthenticated-invoke my-first-function 

#get the URL to run in browser
yc serverless function get my-first-function 

# YOU WILL GOT THE LINK, CHECK IT IN YOUR BROWSER
```

6. Create second function that will run after trigger (code: yc-function-with-trigger)

```
yc serverless function create --name my-trigger-function

yc serverless function version create \
--function-name my-trigger-function \
--memory 256m \
--execution-timeout 5s \
--runtime python37 \
--entrypoint index.handler \
--service-account-id $SERVICE_ACCOUNT_ID \
--source-path index.py

yc serverless function version list --function-name my-trigger-function 
```

7. Create trigger

```
yc serverless trigger create object-storage \
--name my-first-trigger \
--bucket-id $BUCKET_NAME \
--events 'create-object' \
--invoke-function-name my-trigger-function \
--invoke-function-service-account-id $SERVICE_ACCOUNT_ID 
```

8. Check everything is working

```
# 1. run first function
# Going on broswer using invoke_url:
yc serverless function get my-first-function 

# 2. see the logs from second function
yc serverless function logs my-trigger-function
 
```
