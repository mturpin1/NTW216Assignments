import subprocess
try:
    command = input('Enter the name of the command you want to run:   ')
    command1 = command.split()
    subprocess.run(command1)
except:
    print('Error')
