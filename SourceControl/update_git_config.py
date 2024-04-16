## Git Config update 
import importlib
from Lib import __lib_kafka__ as kafka

importlib.reload(kafka)

kafka.execute_console_command('git config lfs.activitytimeout 60')
kafka.execute_console_command('git config pull.rebase true')
kafka.execute_console_command('git config lfs.https://gitlab.cinamon.me/cinev/CINEVStudio.git/info/lfs.locksverify true')
