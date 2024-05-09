import importlib
from Lib import __lib_kafka__ as kafka
importlib.reload(kafka)


username = kafka.get_git_username()

kafka.unlock_user_assets(username)