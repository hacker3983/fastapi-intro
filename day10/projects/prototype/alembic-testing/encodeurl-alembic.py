# Escaping syntactically significant characters
import urllib.parse
from sqlalchemy import URL

password = "P@assw%rd"
escaped_password = urllib.parse.quote_plus(password)
print("Generated escaped password with urllib:")
print(escaped_password)

# URL quoting with sqlalchemy
encoded_string = URL.create(
        "some_db",
        username="john",
        password=password,
        host="host"
).render_as_string(hide_password=False)
print("Generated url with sqlalchemy:")
print(encoded_string)

print("Generated password for config parser file:")
config_pwd = escaped_password.replace("%", "%%")
print(config_pwd)
