Authentication
==============

Libreta's authentication mechanism must:

- Allow us to have "anonymous" yet, traceable, users.
- Allow us to stablish, unequivocally and in a secure manner, a user's location
  in a stablishment

For that matter, we'll base the authentication system on two base premises:

- "Anonymous" users don't really exist, we'll force a username/password upon
  each new user and leverage the user creation / login to our internal app mechanism
  We'll have to take in account some attack mitigation system as not having the user
  provide a method of authenticating he's real can be problematic (maybe a
  simple captcha?)
- The stablishment will be the one initiating the auth process.


Login mechanism
----------------

We'll use a graphql-based interface, "hasura".
Hasura works great with JWT, that will be auth system after login.
Login can only be initiated by the stablishment, for that matter we'd need to
send a push notification to the initializing device with the JWT after a
succesfull login


