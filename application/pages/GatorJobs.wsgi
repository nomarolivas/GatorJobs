import sys
sys.path.insert(0, '/var/www/csc648-02-sp22-team05/application/pages')

activate_this = '/home/user/MyEnv/bin/activate_this.py'
exec(open("/home/user/MyEnv/bin/activate_this.py").read(), dict(__file__="/home/user/MyEnv/bin/activate_this.py"))


from app import app as application
