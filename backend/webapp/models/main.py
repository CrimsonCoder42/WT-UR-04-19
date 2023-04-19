import os
import uuid
import json
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, ForwardRef, Union

from dyntastic import Dyntastic
import boto3
from pydantic import Field, typing, EmailStr

#from UserRegistrationSE.backend.app.models.enums import countryAbbreviation
from .country_enums import countryAbbreviation
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, MapAttribute, BooleanAttribute
from pynamodb_attributes import UUIDAttribute, UnicodeEnumAttribute

# aws_secure = open('aws.json')
# aws_data = json.load(aws_secure)

# for entry in aws_data:
#     print(f"{entry}: {aws_data[entry]}")

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute

Entitlement = ForwardRef('Entitlement')
EntitlementMap = ForwardRef('EntitlementMap')

class EntitlementConditionMap(MapAttribute):
    attribute_name = UnicodeAttribute()
    attribute_value = UnicodeAttribute()

#TODO: out enums in external files

class ActionTypeEnum(str, Enum):
    read = "read"
    write = "write"
    delete = "delete"

class ObjectTypeEnum(str, Enum):
    all = "*"
    user = "user"
    media = "media"
    entitlement = "entitlement"


class ActionTypeEnumAttribute(UnicodeEnumAttribute):
    def __init__(self, *args, **kwargs):
        super().__init__(enum_type=ActionTypeEnum,*args, **kwargs)
class ObjectTypeEnumAttribute(UnicodeEnumAttribute):
    def __init__(self, *args, **kwargs):
        super().__init__(enum_type=ObjectTypeEnum,*args, **kwargs)



# AWS_ACCESS_KEY_ID = aws_data["AWS_ACCESS_KEY_ID"]
# AWS_SECRET_ACCESS_KEY = aws_data["AWS_SECRET_ACCESS_KEY"]

class Organization(Model):
    class Meta:
        table_name = 'organization'
        region = 'us-east-1'
    def __init__(self, hash_key=None, range_key=None, **args):
        Model.__init__(self, hash_key, range_key, **args)
        if not self.id:
            self.id = str(uuid.uuid4())

    id = UUIDAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    address = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=True)

class Country(Model):
    class Meta:
        table_name = 'country'
        region = 'us-east-1'
    def __init__(self, hash_key=None, range_key=None, **args):
        Model.__init__(self, hash_key, range_key, **args)
        if not self.id:
            self.id = str(uuid.uuid4())

    id = UUIDAttribute(hash_key=True)
    country_abbr: countryAbbreviation

class FieldWorkLocation(MapAttribute):
    class Meta:
        table_name = 'field_work_location'
        region = 'us-east-1'
    # def __init__(self, hash_key=None, range_key=None, **args):
    #     Model.__init__(self, hash_key, range_key, **args)
    #     if not self.id:
    #         self.id = str(uuid.uuid4())
    #
    # id = UUIDAttribute(hash_key=True)
    country: Country
    location = UnicodeAttribute


class EntitlementMap(MapAttribute):
    name = UnicodeAttribute(null=False)
    entitlement = Entitlement

class Entitlement(Model):
    class Meta:
        table_name = 'entitlement'
        region = 'us-east-1'

    # Define the primary key
    def __init__(self, hash_key=None, range_key=None, **args):
        Model.__init__(self, hash_key, range_key, **args)
        if not self.id:
            self.id = str(uuid.uuid4())

    id = UUIDAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    action_type = ListAttribute(of=ActionTypeEnumAttribute,default=[])
    object_type = ListAttribute(of=ObjectTypeEnumAttribute,default=[])
    # conditions = EntitlementConditionMap(null=True)
    # conditions = EntitlementConditionMap(attr_name="conditions", default={})
    conditions = MapAttribute(attr_name="conditions", default={})

    # conditions = ListAttribute(of=EntitlementConditionMap)


    # Define the list of child entitlements
    sub_entitlements = MapAttribute(attr_name="sub_entitlements", default={})

    def add_sub_entitlement(self, sub_entitlement):
        if self.sub_entitlements is None:
            self.sub_entitlements = {}

        sub_entitlement_map = sub_entitlement.attribute_values
        for str_enum in ["action_type", "object_type"]:
            sub_entitlement_map[str_enum] = [x.value for x in sub_entitlement_map[str_enum]]
        sub_entitlement_map["conditions"] = sub_entitlement_map["conditions"].attribute_values
        sub_entitlement_map["id"] = str(sub_entitlement_map["id"])
        self.sub_entitlements.attribute_values[sub_entitlement.id] = sub_entitlement_map
        self.save()

    def remove_sub_entitlement(self, sub_entitlement):
        if self.sub_entitlements is not None:
            self.sub_entitlements.attribute_values.pop(str(sub_entitlement.id), None)
            self.save()
        return

    def delete(self, *args, **kwargs):
        # Delete the entitlement from all parent entitlements
        for parent_entitlement in Entitlement.scan():
            # parent_entitlement = Entitlement.get(parent_entitlement_name.id)
            if parent_entitlement.sub_entitlements is not None and str(self.id) in parent_entitlement.sub_entitlements.attribute_values.keys():
                parent_entitlement.remove_sub_entitlement(self)
                parent_entitlement.save()
        super().delete(*args, **kwargs)

class UserViewIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = "cognito_id-index"
        read_capacity_units = 2
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    cognito_id = UnicodeAttribute(hash_key=True)

class User(Model):

    class Meta:
        table_name = 'user'
        region = 'us-east-1'

    def __init__(self, hash_key=None, range_key=None, **args):
        Model.__init__(self, hash_key, range_key, **args)
        if not self.id:
            self.id = str(uuid.uuid4())

    id = UUIDAttribute(hash_key=True)
    cognito_id_index = UserViewIndex()
    cognito_id = UnicodeAttribute()
    email = UnicodeAttribute()
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)
    newsletter = BooleanAttribute(null=True)
    entitlements = ListAttribute(attr_name="entitlements", default={})
    authToken = UnicodeAttribute(null=True)
    # photo: Optional[bytes]
    # entitlement = Entitlement()
    #organization: Optional[Organization]
    organization = UnicodeAttribute(null=True)
    organization_verified = BooleanAttribute(null=True)
    interests = UnicodeAttribute(null=True)
    #country_of_residence: Optional[Country]
    country_of_residence = UnicodeAttribute(null=True)
    fieldwork_locations_verified: FieldWorkLocation(null=True)
    fieldwork_locations = UnicodeAttribute(null=True)
    #social_media = UnicodeAttribute(null=True)
    linkedin = UnicodeAttribute(null=True)
    facebook = UnicodeAttribute(null=True)
    twitter = UnicodeAttribute(null=True)
    created = UnicodeAttribute(null=True)
    updated = UnicodeAttribute(null=True)
    status = UnicodeAttribute(null=True)
    role = UnicodeAttribute(null=True)

    def add_entitlement(self, entitlement_id):
        if self.entitlements is None:
            self.entitlements = []

        #add if not already in entitlement list
        self.entitlements = list(set(self.entitlements).union({entitlement_id}))
        self.save()







