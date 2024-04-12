from Lib import __lib_kafka__ as kafka
import importlib



importlib.reload(kafka)


kafka.execute_console_command('git fetch')

kafka.execute_console_command('git stash')

kafka.execute_console_command('git pull --rebase')

kafka.execute_console_command('git stash pop')