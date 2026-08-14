from sqlalchemy import URL, make_url

database_driver = "sqlite"
username = None
password = None
host = None
port = None
database = "foods.db"

sqlalchemy_url = URL.create(
    drivername="sqlite+pysqlite",
    database=database
)
url_string = sqlalchemy_url.render_as_string(hide_password=False)
#print(sqlalchemy_url)
#print(type(sqlalchemy_url))
print("Generated url string is:")
print(url_string)

assert make_url(url_string) == sqlalchemy_url

percent_replaced_url = url_string.replace("%", "%%")
assert make_url(percent_replaced_url % {}) == sqlalchemy_url

print(
    f"The SQLAlchemy URL that can be placed in a ConfigParser "
    f"file such as alembic.ini is:\n"
    f"sqlalchemy.url = {percent_replaced_url}"
)
