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
from typing import Optional

from databases import Database
from pydantic import EmailStr

from trove_fm.app.db.repositories.base import BaseRepository
from trove_fm.app.exceptions import AuthFailure, UsernameExists, VerificationFailure
from trove_fm.app.models.person import AppRole, PersonCredentialsCreate, PersonInDB, PersonPublic
from trove_fm.app.services import auth_service


REGISTER_NEW_PERSON_LOGIN_QUERY = """
    WITH new_person AS (
        INSERT INTO person (app_role, name_first, name_last, password, salt)
        SELECT 'guest', :name_first, :name_last, :password, :salt
        RETURNING id, app_role, active, name_first, name_last, password, salt, created_at, updated_at
    ),
    new_person_email AS (
      INSERT INTO email_address (person_id, email_label, email, verified, email_primary, email_login)
      SELECT new_person.id, :email_label, :username, FALSE, TRUE, TRUE FROM new_person
      RETURNING email_label, email, verified, email_login
    )
    SELECT new_person.id, new_person.app_role, new_person.active, new_person_email.email_label,
           new_person_email.email as username, new_person_email.verified, new_person_email.email_login,
           new_person.name_first, new_person.name_last, new_person.created_at, new_person.updated_at,
           new_person.password, new_person.salt
    FROM new_person, new_person_email;
"""

UPDATE_VERIFIED_PERSON_QUERY = """
    WITH updated_email AS (
        UPDATE email_address
        SET verified = TRUE
        WHERE person_id = :id
        AND email_login = TRUE
        RETURNING email as username, email_label, email_login, verified
    ),
    updated_person AS (
        UPDATE person
        SET app_role       = :app_role,
            verified_date  = :verified_date
        WHERE id = :id
        RETURNING id, active, name_first, name_last, app_role, password, salt
    )
    SELECT up.id, up.name_first, up.name_last, up.app_role, up.active, up.password, up.salt,
           ue.username, ue.email_label, ue.email_login, ue.verified
    FROM updated_person up, updated_email ue
"""

GET_PERSON_BY_USERNAME_QUERY = """
    SELECT p.id, p.active, p.name_first, p.name_last, p.app_role, p.password, p.salt, ea.email_label,
           ea.email as username, ea.email_login, ea.verified, p.created_at, p.updated_at
    FROM person p, email_address ea
    WHERE ea.email = :username
    AND ea.person_id = p.id
    AND ea.email_login IS TRUE;
"""

GET_PERSON_BY_ID_QUERY = """
    SELECT p.id, p.active, p.name_first, p.name_last, p.app_role, p.password, p.salt, ea.email_label,
           ea.email as username, ea.email_login, ea.verified, p.created_at, p.updated_at
    FROM person p, email_address ea
    WHERE p.id = :id
    AND ea.person_id = p.id
    AND ea.email_login IS TRUE;
"""

GET_PERSON_BY_EMAIL_QUERY = """
    SELECT p.id, p.active, p.name_first, p.name_last, p.app_role, p.password, p.salt, ea.email_label,
           ea.email as username, ea.email_login, ea.verified, p.created_at, p.updated_at
    FROM person p, email_address ea
    WHERE ea.email = :email
    AND ea.person_id = p.id;
"""


class PersonRepository(BaseRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.auth_service = auth_service
        # This is a useful pattern that we'll take advantage of regularly.
        # By adding the ProfilesRepository as a sub-repo of the PersonRepository,
        # we can insert any profile-related logic directly into our person-related logic.
        # self.profiles_repo = ProfilesRepository(db)

    async def get_person_by_id(self, *, person_id: int, populate: bool = True) -> PersonPublic:
        person_record = await self.db.fetch_one(query=GET_PERSON_BY_ID_QUERY, values={"id": person_id})
        if person_record:
            person = PersonPublic(**dict(person_record._mapping.items()))
            # if populate:
            #     return await self.populate_account(person=person)
            return person
        else:
            return None

    async def get_person_by_email(self, *, email: EmailStr, populate: bool = True) -> PersonInDB:
        """
        The populate parameter is nice, because it means that when we don't need the person's profile or
        actually want to access the person's password and salt - like in our authenticate_account method -
        we can set populate=False and only get the PersonInDB model back.
        """
        # FIXME: Need to account for multiple email addresses per person!!!
        person_record = await self.db.fetch_one(query=GET_PERSON_BY_EMAIL_QUERY, values={"email": email})
        if person_record:
            person = PersonInDB(**dict(person_record._mapping.items()))

            # if populate:
            #     return await self.populate_account(person=person)

            return person
        else:
            return None

    async def get_person_by_username(self, *, username: str, populate: bool = True) -> PersonInDB:
        """
        The populate parameter is nice, because it means that when we don't need the person's profile or
        actually want to access the person's password and salt - like in our authenticate_account method -
        we can set populate=False and only get the PersonInDB model back.
        """
        person_record = await self.db.fetch_one(query=GET_PERSON_BY_USERNAME_QUERY, values={"username": username})

        if person_record:
            person = PersonInDB(**dict(person_record._mapping.items()))

            # if populate:
            #     return await self.populate_account(person=person)

            return person
        else:
            return None

    async def register_person_credentials(self, *, new_person_creds: PersonCredentialsCreate) -> PersonInDB:
        # make sure email isn't already taken
        if await self.get_person_by_email(email=new_person_creds.username):
            raise UsernameExists(f"The username {new_person_creds.username} is already in the database.")

        user_password_update = self.auth_service.create_salt_and_hashed_password(
            plaintext_password=new_person_creds.password
        )
        new_person_creds_params = new_person_creds.copy(update=user_password_update.dict())
        created_creds = await self.db.fetch_one(
            query=REGISTER_NEW_PERSON_LOGIN_QUERY, values=new_person_creds_params.dict()
        )

        # Make sure that when a new person is created, our PersonRepository also creates a profile for that person.
        # Once a person registers with our application, we take the newly created person's id and use it to
        # add an empty profile to our database.
        # If we want to allow users to sign up with additional information, we can pass that along here as well.
        # await self.profiles_repo.create_profile_for_person(
        #     profile_create=ProfileCreate(person_id=created_creds["id"])
        # )

        return PersonInDB(**dict(created_creds._mapping.items()))

    async def verify_new_person_creds(self, username) -> PersonInDB:
        candidate = await self.get_person_by_username(username=username)

        if not candidate:
            raise VerificationFailure(f"Email address {username} not found.")

        if candidate.verified is True:
            raise VerificationFailure(f"The email address {username} has already been verified.")

        person_verified = await self.db.fetch_one(
            query=UPDATE_VERIFIED_PERSON_QUERY,
            values={"id": candidate.id, "app_role": AppRole.customer.value, "verified_date": datetime.now()}
        )

        return PersonInDB(**dict(person_verified._mapping.items()))

    async def authenticate_account(self, *, email: EmailStr, password: str) -> Optional[PersonInDB]:
        # make sure person exists in db
        person = await self.get_person_by_email(email=email, populate=False)

        if not person:
            raise AuthFailure("The username does not exist in the database.")
        if person.verified is False:
            raise AuthFailure("The username provided has not been verified.")
        if not self.auth_service.verify_password(password=password, salt=person.salt, hashed_pw=person.password):
            raise AuthFailure("The password provided does not match the one in the database.")

        return person
