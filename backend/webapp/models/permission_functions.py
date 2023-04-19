from UserRegistrationSE.backend.app.models.main import *
from dyntastic import A


aws_secure = open('aws.json')
aws_data = json.load(aws_secure)


AWS_ACCESS_KEY_ID = aws_data["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = aws_data["AWS_SECRET_ACCESS_KEY"]


##Get sub entitlements
def get_subentitlements(role_id):
    Entitlement.update_forward_refs()
    role_obj=Entitlement.get(role_id)
    sub_ents=role_obj.subEntitlements
    return sub_ents
  
# sub_ents=get_subentitlements(role_id)
# print(sub_ents)

### add_entitlement_to_role
def add_entitlement_to_role(role_id,entitlement_id):
    Entitlement.update_forward_refs()
    #Getting role
    role_obj=Entitlement.get(role_id)
    #Getting entitlement to add
    added_subentitlement=Entitlement.get(entitlement_id)
    
    #Getting current entitlements of role
    pre_entitlements=get_subentitlements(role_id)
    
    #Checking if entitlement already exists in role - we don't want duplicate entries
    if entitlement_id in list(pre_entitlements.keys()):
        print("Entitlement already exists under role. Aborting.")
    
    #Adding entitlement to role if not exists
    else:
        new_sub_entitlements=pre_entitlements
        new_sub_entitlements[entitlement_id]=added_subentitlement        
        role_obj.update(A.subEntitlements.set(new_sub_entitlements))
    
    #print role entilements after operation
    post_sub_entitlements=get_subentitlements(role_id)
    print("post_sub_entitlements")
    print(post_sub_entitlements)    
    
# role_id='1d73ddf1-8bd4-485a-99db-6e0715aacfc9'
# entitlement_id='e1bbe1a7-c21e-4632-9c6a-655904269b49'
# add_entitlement_to_role(role_id,entitlement_id)


### remove_entitlement_from_role
def remove_entitlement_from_role(role_id,entitlement_id):
    Entitlement.update_forward_refs()
    #Getting role
    role_obj=Entitlement.get(role_id)
    #Getting entitlement to add
    #existing_subentitlement=Entitlement.get(entitlement_id)
    
    #Getting current entitlements of role
    pre_entitlements=get_subentitlements(role_id)
    print('pre_entitlements')
    print(pre_entitlements)
    
    #Checking if entitlement already exists in role - we don't want duplicate entries
    if entitlement_id not in list(pre_entitlements.keys()):
        print("Entitlement does not exists under role. Aborting.")
    
    #Adding entitlement to role if not exists
    else:
        pre_entitlements.pop(entitlement_id)
        role_obj.update(A.subEntitlements.set(pre_entitlements))
    #print role entilements after operation
    post_sub_entitlements=get_subentitlements(role_id)
    print("post_sub_entitlements")
    print(post_sub_entitlements)
    
# role_id='1d73ddf1-8bd4-485a-99db-6e0715aacfc9'
# entitlement_id='entitlement_id'
# remove_entitlement_from_role(role_id,entitlement_id)


### create_entitlement

def create_entitlement(name, description):
    Entitlement.update_forward_refs()
    new_entitlement = Entitlement(name=name, description=description)
    new_entitlement.save()
    return
  
  
### delete entitlement
def delete_entitlement(entitlement_id):  
    Entitlement.update_forward_refs()
    
    print("deleting :"+entitlement_id)
    try:
        new_entitlement = Entitlement.get(entitlement_id)
        new_entitlement.delete()
        print("Done")
    except:
        print("Entitlement does not exist")
    
    return
#  delete_entitlement("23b1cdff-1910-42a5-ac44-a02809c00a09")
    
  
### add role to user  
def add_role_to_user(user_id,role_id):
    Entitlement.update_forward_refs()
    user_pre=User.get(user_id)
    role=Entitlement.get(role_id)
    user_pre.entitlement=role
    user_pre.save()

    user_post=User.get(user_id)
    print(user_post)

# user_id='7a22858f-c334-4380-804c-01126e0a05b1' #A random user id
# role_id='1d73ddf1-8bd4-485a-99db-6e0715aacfc9'#Developer
# add_role_to_user(user_id,role_id)



### verify user access
def verify_user_access(user_id,req_ent_name):
    Entitlement.update_forward_refs()
    user_entitlement_lst=[]
    user=User.get(user_id)
    user_entitlements=user.entitlement
    user_entitlement_lst.append(user_entitlements.name)
    
    sub_entitlements=user_entitlements.subEntitlements
    
    for key in sub_entitlements:
        sub_ent=sub_entitlements[key]
        user_entitlement_lst.append(sub_ent.name)
    
    if req_ent_name in user_entitlement_lst:
        print("Access granted")
        return True
    else:
        print("Access denied")
        return False        
    return


# entitlement_name='MediaUpload'
# user_id_entitled='7a22858f-c334-4380-804c-01126e0a05b1'
# user_id_not_entitled='720530be-f7e7-4748-a15e-d16e23f20467'
# verify_user_access(user_id,entitlement_name)
