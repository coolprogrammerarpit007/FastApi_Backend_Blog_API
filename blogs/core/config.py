from datetime import datetime,date
import secrets

SECRET_KEY = "16WYzL4LdIwl9PK2ht7IqtzPUB0oYupeqWS_QDgk9Qs"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# To generate secrete key

# print(secrets.token_urlsafe(32))