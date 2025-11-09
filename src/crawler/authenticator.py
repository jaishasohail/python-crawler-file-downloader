_session(auth_config, logger) -> requests.Session
Creates a configured requests.Session instance.
Supported auth_config keys:

login_url(string, optional): URL to POST credentials to.

username / password(string, optional): Credentials for login.

username_field / password_field(string): Names of form fields.

headers(dict): Extra headers to attach to the session.

cookies(dict): Extra cookies to attach to the session.

extra_payload(dict): Additional key/value pairs to include in login payload.

timeout(int): Timeout for the login request.

Scraper Module
