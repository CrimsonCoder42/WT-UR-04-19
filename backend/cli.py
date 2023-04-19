import sys
import requests
import re
import argparse
import pathlib
import json
from getpass import getpass
from enum import Enum
#from app.models.main import User, Entitlement, ActionTypeEnum, ObjectTypeEnum

"""
This program is to allow an API call for system administrators in order to 
run existing API calls
"""
class ActionTypeEnum(str, Enum):
    read = "read"
    write = "write"
    delete = "delete"

class ObjectTypeEnum(str, Enum):
    all = "*"
    user = "user"
    media = "media"
    entitlement = "entitlement"

def config_arguments(usage=None):
    """

    :param usage:  This gets passed to argparse to allow for usage to be shown)
    :return: parser :  Argparse object
    """

    parser = argparse.ArgumentParser(usage=usage)
    # g1 = parser.add_argument_group(title='add || remove ', description='One of these options must be chosen.')
    # group = g1.add_mutually_exclusive_group(required=True)
    # group.add_argument("-a","--add_clone", action="store_true",required=False,
    #                    help="Create a new clone")
    # group.add_argument("-r","--remove_clone", action="store_true", required=False,
    #                    help="remove a clone")
    # group.add_argument("-l","--list", action="store_true", required=False,
    #                    help="List current clones")
    # parser.add_argument("-d", "--debug", action="store_true", required=False,
    #                     help="Send debug statements to the screen and to syslog (if allowed)")
    # parser.add_argument("-f","--file",required=False,help="JSON file required for program to run")
    # parser.add_argument("-c", "--clone", required=True, help="Name of clone suffix")
    # parser.add_argument("-u", "--user", required=True, help="API login for NetApp filer")
    # parser.add_argument("-p", "--password", required=True, help="API password for NetApp filer")
    # parser.add_argument("--checkstep", action="store_true", help="Option to enable step checks in program when running manually")

    parser.add_argument("-u", "--user", required=True, help="user name to allow CLI actions")
    parser.add_argument("-c", "--config", required=True, help="Configuration file for cli")
    parser.add_argument("-f", "--file", required=False, help="Load file to manage commands")
    parser.add_argument("-t", "--test", required=False, action='store_true', help="testing:  skip password entry")
    parser.add_argument('argv', nargs='*')  # Grabs remaining text and puts it in 'argv' 
    return parser

def evaluate_file(file_name,header,config_file):
    print("evaluating file")
    if pathlib.Path(file_name).is_file:
        count = 0
        with open(file_name) as fp:
            lines = fp.readlines()
            for line in lines:
                count += 1
                #  Check to see if line starts with a #
                if line == '\n':
                    print("empty line")
                    continue
                if line[0] == '#':
                    print(f"skipping {line}")
                    continue
                
                print("Line{}: {}".format(count, line.strip()))
                command = line.split()
                print(command)
                evaluate_command(command,header, config_file)

def get_authorization(options, passwd, config_file):
    """
    This function logs into the system and gets the authorization token
    :param options: argparse object containing the command line arguments
    :param passwd:  string containing the user password
    :config_file: dictionary object containing configuration file information
    """

    header = {"accept": "application/json"}
   

    url = f"http://{config_file['host']}{config_file['version']}/signin"
    print(url)
    body = {
        "email":"adakopyan@gmail.com",
        "password":"!Test12456!"
    }
    print(body)
    response = requests.post(url,json=body, verify=False, headers=header)
    
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    #print(result)
    return result

def test_get_user(config_file, header):
    """
    This is just a test function to get a specific user
    """

    url = f"http://{config_file['host']}{config_file['version']}/get_user"
    print(url)
    response = requests.get(url, verify=False, headers=header)
    
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    print(result)

def evaluate_actions_objects_and_conditions(command):
    """
    This function simply evaluates the actions, objects and conditions of given command
    """

    # make a pattern
    pattern = "^[A-Za-z0-9_]*$"



 

    approved_actions = []
    approved_objects = []
    approved_conditions = {}
    for entry in command:
        if entry.find('name=') != -1:
            print(f"name: {entry}")
            name_list = entry.split('=')
            name = name_list[1]
            if not bool(re.match(pattern,name)):
                print("cannot use this name")

        elif entry.find('action') != -1:       
            action_list = entry.split('=')
            action=action_list[1]
            if action in list(ActionTypeEnum):
                print(f"{action}: {ActionTypeEnum[action].value}")
                action_value = ActionTypeEnum[action].value
                if action_value not in approved_actions:
                    approved_actions.append(action_value)
            else:
                print("not in ActionTypeEnum")    
        elif entry.find('object=') != -1:       
            object_list = entry.split('=')
            object=object_list[1]
            if object in list(ObjectTypeEnum):
                print(f"{object}: {ObjectTypeEnum[object].value}")
                object_value = ObjectTypeEnum[object].value
                if object_value not in approved_objects:
                    approved_objects.append(object_value)
            else:
                print("not in ActionTypeEnum")
        elif entry.find('=') != -1:  
            print(f"condition: {entry}")     
            condition_list = entry.split('=')
            condition=condition_list[1]
            if not bool(re.match(pattern,condition)):
                print("cannot use this condition.  It has special characters")
            approved_conditions[condition_list[0]]=condition_list[1]
    print(f"name: {name}")                          
    print(approved_actions)
    print(approved_objects)
    print(approved_conditions)
    return name, approved_actions, approved_objects, approved_conditions

def create_entitlement(command,header,config_file):
    """
    This function will call the create header process
    """

    print("Running create_entitlement")
    name, approved_actions, approved_objects, approved_conditions = evaluate_actions_objects_and_conditions(command)
    if len(approved_actions) < 1 or len(approved_objects) <1:
        print("Need at least one action and object")
    if len(approved_actions) >3:
        print("Too many actions")



    url = f"http://{config_file['host']}{config_file['version']}/create_entitlement"
    print(url)

    body = { 
        "name" : name,
        "action_type" : approved_actions,
        "object_type" : approved_objects,
        "conditions" : approved_conditions
    }

    print(body)
    print(header)

    
    response = requests.post(url, json=body,verify=False, headers=header)
    
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    print(f"result is {result}")


def delete_entitlement(command,header,config_file):
    """
    This function deletes an existing role
    """        
    print("Running delete role")
    name, approved_actions, approved_objects, approved_conditions = evaluate_actions_objects_and_conditions(command)
    print(name)
    entitlement_id_dict = get_entitlement_id(name,header, config_file)
    print(entitlement_id_dict)
    if entitlement_id_dict["entitlement_id"] == "":
        print(f"Entitlement {name} not found in database")
        exit(1)
    if len(entitlement_id_dict) > 1:
        print(f"Too many entitlements with the same name.  You will have to contact the system administrator to edit directly")
        exit(1)


    url = f"http://{config_file['host']}{config_file['version']}/delete_entitlement"
    print(url)

    print(entitlement_id_dict)
    print(header)

    
    response = requests.delete(url, json=entitlement_id_dict,verify=False, headers=header)
    
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    print(f"result is {result}")

    return result    

def evaluate_entitlement_names(command):
    """
    This function simply evaluates the actions, objects and conditions of given command
    """

    # make a pattern
    pattern = "^[A-Za-z0-9_]*$"

    entitlement_name=""
    subentitlement=""
    for entry in command:
        if entry.find('entitlement_name=') != -1:
            print(f"name: {entry}")
            entitlement_list = entry.split('=')
            entitlement_name = entitlement_list[1]

        elif entry.find('subentitlement=') != -1:
            print(f"subentitlement: {entry}")
            subentitlement_list = entry.split('=')
            subentitlement = subentitlement_list[1]
       
    print(f"entitlement_name: {entitlement_name}")                          
    print(f"subentitlement: {subentitlement}")
    return entitlement_name, subentitlement

def evaluate_user_and_entitlement_id(command):
    """
    This function simply evaluates the actions, objects and conditions of given command
    """

    # make a pattern
    pattern = "^[A-Za-z0-9_]*$"

    entitlement_name=""
    user_email=""
    for entry in command:
        if entry.find('entitlement_name=') != -1:
            print(f"name: {entry}")
            entitlement_list = entry.split('=')
            entitlement_name = entitlement_list[1]

        elif entry.find('user_email=') != -1:
            print(f"subentitlement: {entry}")
            user_list = entry.split('=')
            user_email = user_list[1]
       
    print(f"entitlement_name: {entitlement_name}")                          
    print(f"user__email: {user_email}")
    return entitlement_name, user_email

def add_entitlement_to_entitlement(command, header, config_file):
    """
    This function adds an entitlement ot another entitlement
    """
    entitlement_name, subentitlement = evaluate_entitlement_names(command)
    print (entitlement_name)
    print(subentitlement)

    
    entitlement_id_dict = get_entitlement_id(entitlement_name,header, config_file)
    subentitlement_id_dict = get_entitlement_id(subentitlement,header, config_file)
    print(entitlement_id_dict)
    print(subentitlement_id_dict)
    if entitlement_id_dict['entitlement_id'] =='':
        print("No entitlement match.  cannot continue")
        exit(1)
    if subentitlement_id_dict['entitlement_id'] == '':
        print("No subentitlement match.  cannot continue")
        exit(1)

    url = f"http://{config_file['host']}{config_file['version']}/add_subentitlement"
    print(url)
    
    body = {
        "parent_entitlement_id": entitlement_id_dict["entitlement_id"],
        "child_entitlement_id": subentitlement_id_dict["entitlement_id"]
        }

    print(body)

    response = requests.post(url, json=body,verify=False, headers=header)
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    print(f"result is {result}")
    
def remove_entitlement_from_entitlement(command, header, config_file):
    """
    This function adds an entitlement ot another entitlement
    """
    entitlement_name, subentitlement = evaluate_entitlement_names(command)
    print (entitlement_name)
    print(subentitlement)

    
    entitlement_id_dict = get_entitlement_id(entitlement_name,header, config_file)
    subentitlement_id_dict = get_entitlement_id(subentitlement,header, config_file)
    print(entitlement_id_dict)
    print(subentitlement_id_dict)
    if entitlement_id_dict['entitlement_id'] =='':
        print("No entitlement match.  cannot continue")
        exit(1)
    if subentitlement_id_dict['entitlement_id'] == '':
        print("No subentitlement match.  cannot continue")
        exit(1)

    url = f"http://{config_file['host']}{config_file['version']}/add_subentitlement"
    print(url)
    
    body = {
        "parent_entitlement_id": entitlement_id_dict["entitlement_id"],
        "child_entitlement_id": subentitlement_id_dict["entitlement_id"]
        }

    print(body)

    response = requests.post(url, json=body,verify=False, headers=header)
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    print(f"result is {result}")

def get_entitlement_id(name, header, config_file):

    url = f"http://{config_file['host']}{config_file['version']}/get_entitlement"
    print(url)

    body = { 
        "entitlement_name" : name
    }
    print(body)
    print(header)

    
    response = requests.get(url, json=body,verify=False, headers=header)
    
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    print(f"result is {result}")

    return result

def get_user_id(email, header, config_file):

    url = f"http://{config_file['host']}{config_file['version']}/get_alt_user"
    print(url)

    body = { 
        "email" : email
    }
    print(body)
    print(header)

    
    response = requests.get(url, json=body,verify=False, headers=header)
    
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    print(f"result is {result}")

    return result







def evaluate_command(command,header,config_file):
    """
    This function evaluates the parsed commands
    :parameter command : this is a list of strings that should correlate to a proper command
    return: 
    """

    # if command[0] == "create":
    #     pass
    # elif command[0] == "delete":
    #     pass
    # elif command[0] == "update":
    #     pass
    # elif command[0] == "add":
    #     pass
    # elif command[0] == "remove":
    #     pass

    if command[0] == "entitlement":
        entitlement_commands(command,header,config_file)
    if command[0] == "user":
        user_commands(command, header, config_file)
    else:
        print("Not a valid command, skipping")

def entitlement_commands(command,header,config_file):
    if command[1] == "create":
        create_entitlement(command,header,config_file)
    elif command[1] == "delete":
        delete_entitlement(command,header,config_file)
    elif command[1] == "add":
        add_entitlement_to_entitlement(command, header, config_file)
    elif command[1] == "remove":
        #remove_entitlemenent_from_entitlement(command, header, config_file)
        pass

    else:
        pass

def add_entitlement_to_user(command, header, config_file):
    """
    This command adds an entitlement to a specific user
    """

    entitlement_name, user_email = evaluate_user_and_entitlement_id(command)
    print(entitlement_name)
    print(user_email)   
    entitlement_id_dict = get_entitlement_id(entitlement_name,header, config_file)
    print(entitlement_id_dict)
    user_id_dict = get_user_id(user_email, header, config_file)
    print(user_id_dict)

    url = f"http://{config_file['host']}{config_file['version']}/user_add_role"
    print(url)

    body = { 
        "user_id" : user_id_dict["user_id"],
        "role_id" : entitlement_id_dict["entitlement_id"] 
    }
    print(f"body is : {body}")
    #print(header)

    
    response = requests.post(url, json=body,verify=False, headers=header)
    
    print(f"response is : {response.text}")
    result = json.loads(response.text)
    print(f"result is {result}")

    return result



def user_commands(command,header,config_file):
    if command[1] == "add":
        add_entitlement_to_user(command,header,config_file)
    elif command[1] == "remove":
        #remove_entitlement_from_user(command,header,config_file)
        pass



def main(argv):
    """
    :param argv: Command Line arguments object
    :return N/A
    """

    parser = config_arguments()
    options = parser.parse_args()

    if options.test:
        passwd = "test"
    else:    
        print("Please enter user password ")
        passwd = getpass()

    if pathlib.Path(options.config).is_file:
        cf = open(options.config)
        try:
            config_file = json.load(cf)
            print(config_file)
        except Exception as e:
            print(f"Error: json cannot load config file due to {e}")
    else:
        print("Config file cannot be read")
        exit(1)    

    authorization = get_authorization(options, passwd, config_file)

    # creating header for all commands
    access_token = f"Bearer {authorization['access_token']}"
    header = {
        "accept": "application/json",
        "Authorization": access_token
    }
    print(f"\n\n\nheader is {header}")

    #test_get_user(config_file, header)

    if options.file:
        evaluate_file(options.file,header,config_file)
    else:
        pass
        #evaluate_command(options.argv)    

if __name__ == "__main__":
    main(sys.argv[1:])
