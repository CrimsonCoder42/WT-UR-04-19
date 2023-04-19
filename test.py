import os
import uuid
from datetime import datetime
from typing import Optional, Dict, ForwardRef, Union

from dyntastic import Dyntastic, A
import boto3
from pydantic import Field, typing, EmailStr

from UserRegistrationSE.backend.app.models.enums import countryAbbreviation

from UserRegistrationSE.backend.app.models.main import User,UserProfile,Country,FieldWorkLocation,Entitlement,Organization
from UserRegistrationSE.backend.app.models.enums import countryAbbreviation




class Event_Organization(Dyntastic):
    __table_name__ = "Organization"
    __hash_key__ = "event_id"
    __range_key__ = "timestamp"

    event_id: str
    timestamp: datetime
    data: dict

test_org_name=Event_Organization.query("some_event_id", filter_condition=A.name == "test org")

# Entitlement = ForwardRef('Entitlement')

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


#
# org = User(name="test user 4")
# org.save()


# test=User.get("50f5ef1b-33f1-4429-a390-8fb2fd292c9e")
# print(test)



country_user=Country.get('5fbafd9d-54e8-4882-8d0b-15c7aca33a0e')

print(country_user)

user_field_work_location=FieldWorkLocation(country=country_user,location='Test')
user_field_work_location.save()


mediaU_ent=Entitlement.get('e1bbe1a7-c21e-4632-9c6a-655904269b49')
Entitlement.update_forward_refs()
test_entitlement=Entitlement(name="Developer",subEntitlements={'e1bbe1a7-c21e-4632-9c6a-655904269b49':mediaU_ent})
test_entitlement.save()
Entitlement.update_forward_refs()

entitlement_user=Entitlement.get('1d73ddf1-8bd4-485a-99db-6e0715aacfc9')

fieldWorkLocation_user=FieldWorkLocation.get('45654c98-ffeb-4842-9db8-2f9e5216dcd8')

organization_user=Organization.get('ba851e4e-c693-40fd-b1ef-91fcfbfe87cb')


user_profile=UserProfile(
    user_id="50f5ef1b-33f1-4429-a390-8fb2fd292c9e",
    first_name="2",
    last_name="3",
    email="4@4.com",
    photo="5",
    entitlement=entitlement_user,
    organization=organization_user,
    interests="8",
    country_of_residence=country_user,
    fieldwork_location=fieldWorkLocation_user,
    credentials="11",
    social_media="12")
user_profile.save()
#
#
# Event.query("some_event_id", filter_condition=A.some_field == "foo")
#
# class Event_User(Dyntastic):
#     __table_name__ = "User"
#     __hash_key__ = "event_id"
#     __range_key__ = "timestamp"
#
#     event_id: str
#     timestamp: datetime
#     data: dict


# Event.query("some_event_id", filter_condition=A.some_field == "foo")


test_profile=UserProfile.get('2bb01490-b80d-42af-811c-c45d085202ff')
print(test_profile)

user_id=User.get('test user 3')
print(type(user_id))

print(user_id.id)

    # id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    # user_id: str
    # first_name: str
    # last_name: str
    # email: EmailStr
    # photo: bytes
    # entitlement: Entitlement
    # organization: Organization
    # interests: str
    # country_of_residence: Country
    # fieldwork_location: FieldWorkLocation
    # credentials: str
    # social_media: str


# print(countryAbbreviation)
#
# for countryAbb in countryAbbreviation:
#     print(countryAbb.value)
#     country=Country(country_abbr=countryAbb.value)
#     country.save()
#
#
#
#
# country.save()
