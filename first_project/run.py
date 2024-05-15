import os,socket

# install_cmd = "pip install -r requirements.txt"

# os.system(install_cmd)

hostname = socket.gethostname()

ip = socket.gethostbyname(hostname)

port = 8181

command = "python manage.py runserver "+str(ip)+":"+str(port)

os.system(command)