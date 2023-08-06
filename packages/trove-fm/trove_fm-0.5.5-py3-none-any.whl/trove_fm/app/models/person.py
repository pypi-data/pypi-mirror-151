"""
TroveFM is an online store and headless CMS.

Copyright (C) 2022  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import constr, EmailStr, root_validator


from trove_fm.app.models.core import CoreModel, DateTimeModelMixin, IDModelMixin


class AppRole(str, Enum):
    admin = "admin"        # Full priviledges
    customer = "customer"  # Browse/Search inventory and place orders
    power = "power"        # Manage users, issue refunds, run reports, manage inventory
    guest = "guest"        # No priviledges
    staff = "staff"        # Manage time, modify/process orders
    vendor = "vendor"      # Supply compliance/quality assurance data, Check inventory


class PersonBase(CoreModel):
    """
    Leaving off password and salt from base model
    """
    active: bool = False
    username: Optional[EmailStr]
    email_label: Optional[str]
    name_first: Optional[str]
    name_last: Optional[str]


class PersonCreate(CoreModel):
    """
    Used when creating a person through the CMS interface
    """
    # TODO: Implement the admin interface that will use this.
    employee: bool = False
    name_first: Optional[str]
    name_last: Optional[str]
    company_id: Optional[int]
    email: Optional[EmailStr]


class PersonCredentialsCreate(CoreModel):
    """
    Used when creating a person (or login) through the app sign-up page
    """
    name_first: Optional[str]
    name_last: Optional[str]
    username: EmailStr
    email_label: str
    password: constr(min_length=16, max_length=100, regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).*$')

    @root_validator(pre=True)
    def check_for_name(cls, values) -> str:
        name_first, name_last = values.get("name_first"), values.get("name_last")
        if name_first == '' and name_last == '':
            raise TypeError("First Name and Last Name cannot both be blank.  Please provide at least one.")
        return values


class PersonUnverified(PersonBase):
    username: EmailStr
    link_expiration: datetime
    message: str
    help_message: str


class PersonUpdate(CoreModel):
    """
    Persons are allowed to update their email and/or username
    """
    username: Optional[EmailStr]


class PersonPasswordUpdate(CoreModel):
    """
    Persons can change their password
    """
    password: constr(min_length=16, max_length=100, regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).*$')
    salt: str


class PersonInDB(IDModelMixin, DateTimeModelMixin, PersonBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """
    app_role: AppRole
    email_login: bool
    verified: bool
    password: str
    salt: str


class PersonPublic(IDModelMixin, DateTimeModelMixin, PersonBase):
    pass
    # profile: Optional[ProfilePublic]
