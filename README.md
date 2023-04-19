# UserRegistrationSE
# This is a module for users authentication and authorization

# Description

This module uses[AWS Cognito](https: // aws.amazon.com/cognito /) to authenticate users, which is connected to backend based on[Flask]('https://flask.palletsprojects.com/en/2.2.x/). Back-end uses [AWS DynamoDB](https://aws.amazon.com/dynamodb/) (noSQL database) to store users' information.


AWS cognito operations are held using `boto3`, having examples from [here](https: // github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/cognito/cognito_idp_actions.py
)(see `congito_conroller` for details)

Connection with DataBase is done with wrapper[Dyntastic](https: // pypi.org/project/dyntastic /) which allows to map Model classes to Tables


To run application:

 - clone this repo
 - get dependencies(`pip install -r requirements.txt`)(highly recommended to do that in a virtual environment)
 - set up environment variables:
   - AWS_ACCESS_KEY_ID
   - AWS_COGNITO_DOMAIN
   - AWS_COGNITO_CLIENT_SECRET
   - AWS_SECRET_ACCESS_KEY
   - COGNITO_APP_CLIENT_ID
   - COGNITO_REGION
   - COGNITO_USER_POOL_ID
 - python `backend/webapp/api.py`
# WT-UR-04-19
