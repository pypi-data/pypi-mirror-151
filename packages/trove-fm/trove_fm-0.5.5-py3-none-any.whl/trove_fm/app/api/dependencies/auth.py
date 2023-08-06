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


from typing import Optional

from fastapi import Depends, HTTPException, status

from trove_fm.app.api.dependencies.database import get_repository
from trove_fm.app.config import API_PREFIX, SECRET_KEY
from trove_fm.app.db.repositories.person import PersonRepository
from trove_fm.app.models.person import PersonInDB
from trove_fm.app.services import auth_service, OAuth2PasswordBearerSecure


oauth2_scheme = OAuth2PasswordBearerSecure(tokenUrl=f"{API_PREFIX}/person/login/token/")


async def get_account_from_token(
    *,
    token: str = Depends(oauth2_scheme),
    person_repo: PersonRepository = Depends(get_repository(PersonRepository)),
) -> Optional[PersonInDB]:
    """Return a PersonInDB model if a valid access token is presented with the request

    By injecting the oauth2_scheme as a dependency, FastAPI will inspect the request for
    an Authorization cookie or header, check if the value is Bearer plus some token, and
    return the token as a str. If it doesn't see an Authorization header or cookie, or
    the value doesn't have a Bearer token, it will respond with an HTTP_401_UNAUTHORIZED
    status code.
    """
    try:
        username = auth_service.get_username_from_token(token=token, secret_key=SECRET_KEY)
        person = await person_repo.get_person_by_username(username=username)
    except Exception as e:
        raise e
    return person


def get_current_active_person(current_person: PersonInDB = Depends(get_account_from_token)) -> Optional[PersonInDB]:
    """Attempt to accquire a person's record from the database and return a PersonInDB model to the caller

    If no person with the account presented in the token is found in the database, or
    if the account found has been deactivated, raise an HTTP 401 Unauthorized exception.
    """
    if not current_person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authenticated user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_person.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not an active user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_person
