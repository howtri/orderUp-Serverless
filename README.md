# orderUp-Serverless
A webapp to create and manage group food orders primarily using AWS API Gateway, Lambda, and DynamoDB.

# Architecture
/create path to accept POST requests to start group orders which returns the URL to modify and view the order
/order/{id} to accept GET and POST requests to modify and view the groups order

The API GW routes will be linked with the Lambda PROD alias which will be linked to the most recent stable version

DynamoDB schema
primary key = id | owner | restauraunt | restauraunt_link | orders
orders for the start will be a json dump that will be extended to accept an order like
{<name> : {main : <meal>, sides: <sides>}, <name> : {}}

May add some AWS CodePipeline experimentation in with CodeBuild and CodeDeploy. CICD with CW Events.


