import subprocess

def run_server():
    """
    this will run our 2 server 
    
    One is for API provider flask_server it will provide data 
    Django for our maine logic 
    """
    subprocess.Popen('start cmd /k python flask_server.py', shell=True)
    subprocess.Popen('start cmd /k python manage.py runserver', shell=True)

run_server()
