###########################################################################################################
#   OAuth2 login example with GitHub application
#
#   Based on workflow shown here: https://requests-oauthlib.readthedocs.io/en/latest/examples/github.html
###########################################################################################################
import time
from requests_oauthlib import OAuth2Session

# Credentials you get from registering a new GitHub application
client_id = '32f6db7d9f22b54ddd4d'
client_secret = '865c88d20cb9f2caf9d49591128d9027d16591a4'
print('clinet_id::::::::: ',client_id)
print('client_secret::::: ',client_secret)
print(' ')



# OAuth endpoints given in the GitHub API documentation
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url              = 'https://github.com/login/oauth/access_token'


github = OAuth2Session(client_id)
print('github:::::::: ',github)
print(' ')


# Redirect user to GitHub for authorization
authorization_url, state = github.authorization_url(authorization_base_url)
print( 'Please go here and authorize,', authorization_url)
print(' ')

# Get the authorization verifier code from the callback url
redirect_response = input('Paste the full redirect URL here:')
print('')


# Fetch the access token
github.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

# Fetch a protected resource, i.e. user profile
r = github.get('https://api.github.com/user')
print('Protected Resource Content:::::: ', r.content)


time.sleep(10)
