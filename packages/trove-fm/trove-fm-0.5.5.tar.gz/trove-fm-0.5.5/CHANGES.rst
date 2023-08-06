
==========
Change Log
==========

0.5.5
-----

New
~~~

- First release available on PyPi: https://pypi.org/project/trove-fm/

Changes
~~~~~~~

- Fixed Python build, so that we include exactly the files that we want in the Source and Wheel
  distributions.  (Removed release 0.5.4 from PiPy)
- This release contains a number of internal changes to improve the development workflow


0.5.4
-----

New
~~~

- First release available on PyPi: https://pypi.org/project/trove-fm/

Changes
~~~~~~~

- This release contains a number of internal changes to improve the development workflow


0.5.3
-----

New
~~~

- Add setuptools-scm as a dev dependency

Changes
~~~~~~~

- Move twine to dev dependencies and remove deploy target from pyproject.toml


0.5.2
-----

New
~~~

- Add openapi.json response for root api endpoint
- Enable sphinx-apidoc
- Add Sphinx Napoleon dev dependency
- Add many new tests to test_person.py.
- Add new module trove_fm/tests/models.py to hold class definitions useful
  during testing.  The initial two classes are UserAgent, to store information
  about user-agents, and UsualSuspect, to store information about person
  test fixtures.
- Add regex constraint to Person models to enforce strong passwords
- Add VerificationFailure exception, to handle instances where the user cannot
  be verified, due to some discrepancy in the database.
- Add dirty-equals dependency for unit testing.
- Add AuthFailure Exception, for use with authenticate_account function in
  person repo
- Add exception handling in person routes and person repo
- Add new OAuth2PasswordBearerSecure class for extracting JWT from
  header **or** cookie.  This class replaces the standard
  OAuth2PasswordBearer class from FastAPI.
- Add route to resend verification email.
- Improved logging with loguru. Add run.py to launch uvicorn server with new
  logging config.
- Add account email validation on sign-up.
- Add dependency for ua-parser, to parse User Agent strings
- Moved pytest_addoption() to new conftest.py file, located in the
  project home directory due to how pytest discovers plugins during
  startup.


Changes
~~~~~~~

- Significant changes to the Docs build, including support for providing
  Versions of the documentation on the docs website.
- register_person_credentials in person repo now returns PersonInDB model,
  consistant with the other functions in the repo.
  The person:register-person-credentials route still returns a PersonUnverified
  model in the response.
- Update TestPersonMe class in test_person.py so that it now works with the
  new architecture.
- Update create_authorized_client in conftest.py so that it now works with
  the new architecture.
- Add email_login and verified attributes to PersonInDB model.
- Revise UPDATE_VERIFIED_PERSON_QUERY to set email_address.verified to True.
- Update OAuth2 authorization flow to get JWT from header **or** cookie
- Update person repo to send correct data sets to models.
- Improved exception handling.
- Remove private claim 'username' from JWT and set 'sub' claim to
  username (we don't need both anymore as 'username' was separate from
  'email' in POC, but they're the same thing now).
- Add JWT_ISSUER to config, rather than hard-coding string in JWTMeta
  model.
- Add some documentation about what is in the JWT.
- Add `--branch` option to coverage command for more coverage
- All tests are now run (correctly) from the project home directory
- The preferred method of running the tests is now via the `inv`
  command (from the 'invoke' library).
- Moved configuration for coverage to pyproject.toml.


0.5.1
-----

New
~~~

- Add link to Documentation in README.


Changes
~~~~~~~

- Remove some stragglers from the transition to reStructuredText from
  Markdown.
- Fix erroneous refernce to CRM (as opposed to CMS) throughout (headbang).


0.5.0
-----

New
~~~

- Version 0.5.0 introduces a new architecture for accounts that offers greater support for
  contact management and Customer Relatioship Management (CMS).


0.0.1
-----

New
~~~

- Initial version.
