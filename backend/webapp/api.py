import logging
import os
import json
from functools import wraps
from dyntastic import A
from datetime import datetime

import boto3
from flask import Flask, jsonify, request, Response
from flask_cors import CORS


# from UserRegistrationSE.backend.app.models.main import User
# from UserRegistrationSE.backend.cognito_controller import CognitoIdentityProviderWrapper


from models.main import User, Entitlement, ActionTypeEnum, ObjectTypeEnum

from cognito_controller import CognitoIdentityProviderWrapper
from pynamodb.attributes import MapAttribute

# Define the handler function for the AWS Lambda function
import serverless_wsgi

serverless_wsgi.TEXT_MIME_TYPES.append("application/custom+json")


def aws_lambda_handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)


def map_to_dict(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, MapAttribute):
            dictionary[key] = value.as_dict()
    return dictionary


app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app) #comment this on deployment


USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AWS_COGNITO_CLIENT_SECRET")
REGION = os.environ.get("COGNITO_REGION")


logger = logging.getLogger(__name__)
cognito_controller = CognitoIdentityProviderWrapper(
    cognito_idp_client=boto3.client('cognito-idp', region_name='us-east-1'),
    user_pool_id=USER_POOL_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET)


# Authentication decorator
def token_required(f):
    '''
    decorator for routes to require login credentials;
    checks if user with provided token exists in Cognito, if not - raise
    examples of usage:

    @app.route('/')
    @token_required
    def index(user):
        return "This is the main page."
    '''
    pass

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer", "").strip()
        if not token:  # throw error if no token provided
            return Response(
                "Valid token is missing",
                status=401,
            )
        try:
            current_user = cognito_controller.get_user_by_token(access_token=token)
            current_user = {x["Name"]:x["Value"] for x in current_user["UserAttributes"]}
            current_user["AccessToken"] = token
        except:
            return Response(
                "Invalid token",
                status=401,
            )
        return f(current_user, *args, **kwargs)
        # Return the user information attached to the token

    return decorator


def fields_required(required_fields=[]):
    '''
    decorator for routed to require certain fields in payload
    check if request.data contains all requested keys, if not - raise
    examples of usage with @token required decorator:

    @app.route('/_api/v1/user_add_role', methods=['POST'])
    @fields_required(required_fields=["user_id", "role_id"])
    @token_required
    def add_role_to_user(user):
        this line is reached only if valid access token was provided AND
        payload contains both "user_id" and "role_id"
    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.json  # a multidict containing POST data
            if data is not None:
                is_valid, missing_keys = check_in_dct(data, required_fields)
                if not is_valid:
                    return Response(
                        "Missing required fields: " + ", ".join(missing_keys),
                        status=400,
                    )
                ctx = f(*args, **kwargs)
                return ctx
        return decorated_function
    return decorator

def check_in_dct(dict_to_check, list_of_keys):
    missing_keys = []
    for key in list_of_keys:
        if dict_to_check.get(key) is None:
            missing_keys.append(key)
    return len(missing_keys) == 0, missing_keys


@app.route('/')
def index():
    return "This is the main page."

@app.route('/_api/v1/user/verify', methods=['GET'])
@token_required
def verify_user(user):
    return jsonify(map_to_dict(user))


@app.route('/_api/v1/signup', methods=['POST'])
def signup():
    '''
    on signup,three processes should be done:
    1. generate user in UserPool
    2. generate user in DynamoDB
    3. generate user_profile associated with user in DynamoDB
    '''
    data = request.json  # a multidict containing POST data
    if data is not None:
        is_valid, missing_keys = check_in_dct(data, ["email", "first_name", "last_name", "newsletter"])
        if not is_valid:
            return Response(
                "Missing required fields: " + ", ".join(missing_keys),
                status=400,
            )
        response = cognito_controller.sign_up_user(user_name=data["email"], password=data["password"],
                                                   user_email=data["email"])
        if response['alreadyExist']:
            return Response(
                "User already exists",
                status=400,
            )
        user = User(cognito_id=response["UserSub"], email=data["email"],
                    first_name=data["first_name"], last_name=data["last_name"],
                    newsletter=data["newsletter"])

        user.save()
        return jsonify({"message": 'check your email for registration confirmation link'})

    # return jsonify(aws_controller.get_items())

@app.route('/_api/v1/user/new', methods=['POST'])
@token_required
def create_user(user):
    '''
    this route creates new User in DynamoDB, associated with corresponding User in Cognito
    ! NB ! don't use with signup route! Use this route when creation user on Cognito is handled via front-end
    '''
    user = User(cognito_id=user["sub"], email=user["email"])

    user.save()
    return jsonify({"message": 'check your email for registration confirmation link'})

    # return jsonify(aws_controller.get_items())

@app.route('/_api/v1/signup/confirm', methods=['POST'])
def signup_confirm():
    data = request.json  # a multidict containing POST data
    if data is not None:
        try:
            cognito_controller.confirm_user_sign_up(user_name=data["email"],
                                                    confirmation_code=data["confirmation_code"])
            return jsonify({'message': 'you are successfully signed up!'})
        except Exception as e:
            print(f"Exception is {e}")
            return Response(
                "Invalid email/code",
                status=400,
            )

#TODO: query for DynamoDB does not work appropriately; we ned to know id in DB to filter overt it, which makes no sence
@app.route('/_api/v1/delete_user', methods=['DELETE'])
@token_required
def delete_user(user):
    '''
    route to delete user allows two scenario:
    1. user wants to delete themselves: only token provided - always allow
    2. user wants to delete other user: provided own token and user to delete - check permission
    '''

    # if data.get("User") is None: #scenario1:
    #     pass
    try:
        user = get_id_from_cognito_id(user['sub'])
        if user is None:
            logger.error("User does not exist")
            return Response(
                "User does not exist",
                status=400,
            )
        user.delete()
        cognito_controller.delete_user(access_token=user["AccessToken"])
        return jsonify({'message': 'Your account was successfully deleted'})
    except:
        return Response(
            "Cannot delete user",
            status=400,
        )

@app.route('/_api/vi/signup/resend-code', methods=['POST'])
def signup_resend_code():
    data = request.json  # a multidict containing POST data
    if data is not None:
        try:
            cognito_controller.resend_confirmation(user_name=data["email"])
            return jsonify({'message': 'confirmation code resent'})
        except:
            return Response(
                "Invalid email/code",
                status=400,
            )

    # return jsonify(aws_controller.get_items())



# Johann routes
@app.route('/_api/v1/signin', methods=['POST'])
def signin():
    data = request.json  # a multidict containing POST data
    if data is not None:
        response = cognito_controller.start_sign_in_basic(user_name=data["email"], password=data["password"])
        if response['success']:
            user = cognito_controller.get_user_by_token(access_token=response["AuthenticationResult"]["AccessToken"])
            # success.authToken probably something like this
            return jsonify({'access_token': response["AuthenticationResult"]["AccessToken"],
                            'refresh_token': response["AuthenticationResult"]["RefreshToken"],
                            'id_token': response["AuthenticationResult"]["IdToken"],
                            'user_id': user["Username"]
                            }
                           )
        else:
            return Response(
                response['error'],
                status=400,
            )


# TODO: provide error-code in case of failure. jsonify will return 200;
@app.route('/_api/v1/signout', methods=['POST'])
def signout():
    data = request.json  # a multidict containing POST data
    if data is not None:
        # TODO: should be an access_token instead?
        success = cognito_controller.sign_out(access_token=data["AccessToken"])
        if success:
            return jsonify({'message': 'you are successfully signed out!'})
        return Response(
            "Error",
            status=400,
        )


@app.route('/_api/v1/refresh_token', methods=['POST'])
def refresh_token():
    data = request.json
    if data is not None:
        try:
            #TODO: check, should we pass that in headers?
            user_name=data["user_id"]
            refresh_token=data["refresh_token"]
            response = cognito_controller.refresh_token(user_name=user_name, refresh_token=refresh_token)
            return jsonify({'access_token': response["AuthenticationResult"]["AccessToken"],
                            'id_token': response["AuthenticationResult"]["IdToken"],
                            }
                           )
        except:
            return Response(
                "Something went wrong",
                status=400,
            )
    return Response(
        "Error",
        status=400,
    )

def get_id_from_cognito_id(cognito_id):

    # Entitlement.update_forward_refs()
    print("Get id from cognito")

    #output = User.query(A.cognito_id == user['sub'], index="cognito_id-index")
    output = User.cognito_id_index.query(cognito_id)
    try:
        user = output.next()
        return user
    except:
        return None
    entry_array = []

@app.route('/_api/v1/get_user', methods=['GET'])
@token_required
def get_user(user):
    print(request.headers)
    print(user)
    print("\n\n\n")

    user = get_id_from_cognito_id(user['sub'])
    if user is not None:
        user_info = user.attribute_values
        user_info.pop("id")
        return jsonify(map_to_dict(user_info))

    else:
        return Response(
                "User not found",
                status=404,
            )

@app.route('/_api/v1/get_alt_user', methods=['GET'])
@fields_required(required_fields=["email"])
@token_required
def get_alt_user(user):
    print(request.headers)
    print(f"USER: {user}")
    data = request.json
    print(data)

    user_id = ""
    user_info = User.scan()
    print(type(user_info))
    for user_info in User.scan():
        try:
            print(f"user_email: {user_info.email}")
        except Exception as e:
            print("bad entry")    
        if data["email"] == user_info.email:
            print("found it")
            user_id = user_info.id
      
    
    if user_id:    
        return jsonify(user_id=user_id)
    else:
        return jsonify(user_id="")

    # user = get_id_from_cognito_id(user['sub'])
    # if user is not None:
    #     user_info = user.attribute_values
    #     user_info.pop("id")
    #     return jsonify(map_to_dict(user_info))
    # else:
    #     return Response(
    #             "User not found",
    #             status=404,
    #         )

@app.route('/_api/v1/get_all_users', methods=['GET'])
@token_required
def list_users(user):
    #TODO: check permission, whether user is eligible to list all users (admin or super admin role)
    
    # Get all users in the users database
    #TODO: Add "number of submitted observations" and "last active" when available
    users = User.scan(attributes_to_get =
        [
            'cognito_id',
            'first_name',
            'last_name',
            'email',
            'organization',
            'created',
            'status',
            'role'
        ])
    user_list = []

    # Loop through all users in the users database
    for user in users:
        user_info = user.attribute_values
        user_list.append(map_to_dict(user_info))
    
    # Return the list of users
    return jsonify(user_list)


@app.route('/_api/v1/update_user', methods=['POST'])
@token_required
def update_user(user):
    """


        This is expected from the User class

        id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        cognito_id: str
        first_name: str
        last_name: str
        email: EmailStr
        entitlementDict: Optional[Dict[str, Entitlement]]

        authToken: Optional[str]
        photo: Optional[bytes]
        entitlement: Optional[Entitlement]
        organization_verified: Optional[Organization]
        organization_cust: Optional[str]
        interests: Optional[str]
        #country_of_residence: Optional[Country]
        country_of_residence: Optional[str],
        fieldwork_location_verified: Optional[FieldWorkLocation]
        fieldwork_location: Optional[str]
        #social_media: Optional[str]
        linkedin: Optional[str],
        facebook: Optional[str],
        twitter: Optional[str]

        This is expected from front end class
        {
            "first_name": "Melinda",
            "last_name": "Marcus",
            "organization": "San Diego Zoo",
            "position": "Director",
            "role": "Contributor",
            "interests": "Big Cats",
            "country_of_residence": "United States of America",
            "fieldwork_locations": "San Diego, California, USA",
            "linkedin": "https://linkedin.com/mmarcus",
            "facebook": "https://facebook.com/mmarcus",
            "twitter": "https://facebook.com/mmarcus","
        } (edited)

    """

    success = False
    return_json = "{}"

    # Get original user data (need to work on the Auth piece here)
    data = request.json  # a multidict containing POST data
    ### Need to verify some data back
    try:
        # Setup current time
        update_time =  datetime.now().strftime("%B %d, %Y at %H:%M")

        # Get current user information:
        user = get_id_from_cognito_id(user['sub'])

        # Get user information based off the now found id
        user_info = User.get(user.id)
        
        # Loop through json data that has been given and update each field
        for i in data.keys():
            # Keys that we do not want to update this way.
            if i == "id" or i == "cognito_id" or i == "created" or i == "updated" or i == "email":
                continue

            function_name = f"user_info.update(actions=[User.{i}.set(data[i])])"
            result = eval(function_name)

        # Add on the updated time :)
        function_name = f"user_info.update(actions=[User.updated.set(update_time)])"
        result = eval(function_name)

        success = True

        # get user data again and return it
        return_json = get_user()

    except Exception as e:
        print(f"Error in update_user: {e}")


    if success:
        return return_json
    else:
        return jsonify({"message": 'An error occurred while editing your user profile.'})


#Entitlements: Johann's functions on routes:
@app.route('/_api/v1/create_entitlement', methods=['POST'])
@token_required
def create_entitlement(user):
    print("DEBUG")
    #TODO: check permission, whether user is eligible to perform operations on entitlements
    data = request.json
    print(data)
    if not data.get("action_type") is None:
        try:
            action_type = [ActionTypeEnum[x] for x in data["action_type"]]
        except:
            return Response(
            f"invalid action type. Possible values: {', '.join([e.value for e in ActionTypeEnum])}",
            status=400,
            )
    else:
        action_type = []
    if not data.get("object_type") is None:
        try:
            object_type = [ObjectTypeEnum[x] for x in data["object_type"]]
        except:
            return Response(
                f"invalid object type. Possible values: {', '.join([e.value for e in ObjectTypeEnum])}",
                status=400,
            )
    else:
        object_type=[]
    try:
        entitlement = Entitlement(name=data["name"], description=data.get("description"),
                                  action_type=action_type,
                                  object_type=object_type,
                                  conditions=data.get("conditions", {})
                                  )
        entitlement.save()
        return jsonify({"message": "created"})
    except:
        return Response(
            "something went wrong",
            status=400,
        )


@app.route('/_api/v1/get_entitlement', methods=['GET'])
@fields_required(required_fields=["entitlement_name"])
@token_required
def get_entitlement(user):
    entitlement_id=""
    #TODO: check permission, whether user is eligible to perform operations on entitlements
    data = request.json
    print(f"data is {data}")
    #entitlement = Entitlement.get(data["entitlement_id"])
    entitlement = Entitlement.scan()
    for entitlement in Entitlement.scan():
        print(f"entitlement: {entitlement.name}")
        if data["entitlement_name"] == entitlement.name:
            print("found it")
            entitlement_id = entitlement.id
    
    if entitlement_id:    
        return jsonify(entitlement_id=entitlement_id)
    else:
        return jsonify(entitlement_id="")



@app.route('/_api/v1/delete_entitlement', methods=['DELETE'])
@fields_required(required_fields=["entitlement_id"])
@token_required
def delete_entitlement(user):
    #TODO: check permission, whether user is eligible to perform operations on entitlements
    data = request.json
    try:
        entitlement = Entitlement.get(data["entitlement_id"])
        entitlement.delete()
        return jsonify({"message": "deleted"})
    except:
        return Response(
            "something went wrong",
            status=400,
        )

@app.route('/_api/v1/add_subentitlement', methods=['POST'])
@fields_required(required_fields=["parent_entitlement_id", "child_entitlement_id"])
@token_required
def add_subentitlement_to_entitlement(user):
    #TODO: check permission, whether user is eligible to add permission to user, whose id is provided
    # Entitlement.update_forward_refs()
    data = request.json
    try:
        parent_entitlement = Entitlement.get(data["parent_entitlement_id"])
    except:
        return Response(
            "Entitlement that you try attach to does not exist",
            status=400,
        )
    try:
        child_entitlement = Entitlement.get(data["child_entitlement_id"])
    except:
        return Response(
            "Entitlement that you try to attach does not exist",
            status=400,
        )
    try:
        parent_entitlement.add_sub_entitlement(child_entitlement)
        parent_entitlement_post = Entitlement.get(data["parent_entitlement_id"])
        return jsonify(map_to_dict(parent_entitlement_post.attribute_values))
    except:
        return Response(
            "Something went wrong",
            status=400,
        )

def get_all_values(nested_dictionary, object_type_list,action_type_list, conditions_dict):
    for key, value in nested_dictionary.items():
        if key == "object_type":
            for item in value:
                # Convert string from database into an Enum value
                ObjectTypeEnumKey = item.split('.')[0]
                object_type = ObjectTypeEnum(ObjectTypeEnumKey).value
                print(f"Object type: {object_type}")
                if object_type not in object_type_list:
                    object_type_list.append(object_type)
            continue
        if key == "action_type":
            print("found action_type")
            print(f"the value is {value}")
            for action_type in value:
                print(f"found {action_type}")
                action_type_list.append(action_type)
        if key == "conditions":
            print("found condition")
            print(value)
            print(type(value))
            if len(value) > 0:
                conditions_dict = conditions_dict.update(value) 
            continue    
        if type(value) is dict:
            get_all_values(value,object_type_list, action_type_list, conditions_dict)
        else:
            print(key, ":", value)
    

@app.route('/_api/v1/check_access', methods=['POST'])
@fields_required(required_fields=["permission"])
@token_required
def check_access(user):

    response_dict = {}
    response_dict["constraints"] = {}
    data = request.json
    print(data)
    user = get_id_from_cognito_id(user['sub'])
    if user is not None:
        user_info = user.attribute_values
        #test_dict = map_to_dict(user_info)
        entitlement_list = user_info["entitlements"]

        for entitlement_id in entitlement_list:
            action_type_list=[]
            conditions_dict={}
            object_type_list = []
            print(f"ENTITLEMENT {entitlement_id}")
            role = Entitlement.get(entitlement_id)
            entitlement_found = (map_to_dict(role.attribute_values))
            print(entitlement_found)
    
    
    
            get_all_values(entitlement_found,object_type_list, action_type_list,conditions_dict)
            print(f"object_type {object_type_list}")
            print(f"action_type_list {action_type_list}")
            print(f"conditions_dict {conditions_dict}")
        
            #  Test actions
            if data["object_type"] in object_type_list:
                print(f"passed object_type_test {data['object_type']}")
                if data["permission"] in action_type_list:
                    print("TRUE!!!!")
                    response_dict[data["permission"]] = "True"
                    # Test to see if conditions exist for this Role. If a role has NO conditions
                    # Need to make it as broad as possible
                    if conditions_dict != {}:
                        print(f"ADDING CONDITIONS {conditions_dict}")
                        response_dict["constraints"] = response_dict["constraints"] | conditions_dict
                    else:
                        response_dict["constraints"] = {}
                else:
                    if response_dict[data["permission"]] != "True":
                        print("SETTING TO FALSE")
                        response_dict[data["permission"]] = "False"

            else:
                response_dict[data["permission"]] = "False"

        # test to see if we have empty constraints:
        if not response_dict["constraints"]:
            print("REMOVING")
            del response_dict["constraints"]
        print(f"Response Dict : {response_dict}")
        return jsonify(response_dict)
        #return jsonify(map_to_dict(user_info))
        #return{}
    else:

        return Response(
            "Responding: check_data",
            status=404
        )


@app.route('/_api/v1/user_add_role', methods=['POST'])
@fields_required(required_fields=["user_id", "role_id"])
@token_required
def add_role_to_user(user):
    #TODO: check permission, whether user is eligible to add permission to user, whose id is provided
    # Entitlement.update_forward_refs()
    data = request.json
    try:
        user_pre = User.get(data["user_id"])
    except:
        return Response(
            "User does not exists",
            status=400,
        )
    try:
        role = Entitlement.get(data["role_id"])
    except:
        return Response(
            "entitlement does not exists",
            status=400,
        )

    user_pre.add_entitlement(entitlement_id=data["role_id"])
    user_post = User.get(data["user_id"])
    return jsonify(map_to_dict(user_post.attribute_values))


#TODO:
# add verification of user_access
# add delition of entitlement from User by request
# add validation of user's entitlements on requesting user's info


# ### verify user access
# def verify_user_access(user_id, req_ent_name):
#     Entitlement.update_forward_refs()
#     user_entitlement_lst = []
#     user = User.get(user_id)
#     user_entitlements = user.entitlement
#     user_entitlement_lst.append(user_entitlements.name)
#
#     sub_entitlements = user_entitlements.subEntitlements
#
#     for key in sub_entitlements:
#         sub_ent = sub_entitlements[key]
#         user_entitlement_lst.append(sub_ent.name)
#
#     if req_ent_name in user_entitlement_lst:
#         print("Access granted")
#         return True
#     else:
#         print("Access denied")
#         return False
#     return


if __name__ == '__main__':
    app.run(host='0.0.0.0')
