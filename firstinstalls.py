import subprocess
import time
import sys
import json

psPath = 'powershell.exe'
summary = []

def refreshenv():
    try:
        refresh = 'refreshenv'
        command1 = refresh.split()
        print('Refreshing the environment. . .')
        output = subprocess.run(command1)
        result = ('-Refreshed the environment')
        print(result)
        summary.append(result)
    except:
        result = ('-Failed to refresh the environment')
        print(result)
        summary.append(result)
        sys.exit(1)

def test(package):
    try:  
        testingPackage = package
        command1 = testingPackage.split()
        print(f'Looking for package {package}. . .')
        output = subprocess.run(command1)
        print(f'Found the package >> {package}')
        result = (f'-Found the package >> {package}')
        summary.append(result)
    except:
        print(f'Failed to find the package >> {package}')
        result = (f'-Failed to find the package >> {package}') 
        summary.append(result)
        sys.exit(1)

def runAPSCommand(command):
    try:
        commandToRun = psPath + ' ' + command
        command1 = commandToRun.split()
        print(f'Running {command}. . .')
        output = subprocess.run(command1, capture_output=True, check=True, text=True)
        print(output.stdout)
        print(output.stderr)
        result = (f'-Ran the PowerShell command >> {command}')
        print(result)
        summary.append(result)
    except:
        result = ('-Failed to run the PowerShell command >> {command}')
        print(result)
        summary.append(result)
        sys.exit(1)
 

def runACommand(command):
    try:
        commandToRun = command
        command1 = commandToRun.split()
        print(f'Running {command}. . .')
        output = subprocess.run(command1, capture_output=True, text=True)
        print(output.stdout)
        print(output.stderr)         
        result = (f'-Ran the command >> {command}')
        print(result)
        summary.append(result)
    except:
        result = (f'-Failed to run the command >> {command}')
        print(result)
        summary.append(result)
        sys.exit(1)

def testAPSCommand(command, check):
    try:
        testingCommand = psPath + ' ' + command
        command1 = testingCommand.split()
        print(f'Testing command {command}. . .')
        output = subprocess.run(command1, capture_output=True, text=True)
        result = str(output.stdout).splitlines()
        outputResult = " ".join(map(str, result))
        if outputResult != check:
            print(f'Command\'{command}\' returned an unexpected value >> \'{outputResult}\'\nExpected >> \'{check}\'')
            result = ('-Tested the PowerShell command >> {command} with the test value >> {check}\nCheck returned with unexpected value >> {outputResult}')
            summary.append(result)
            sys.exit(1)
        else:
            print(f'Command\'{command}\' returned the expected value')
            result = ('-Tested the PowerShell command >> {command} with the test value >> {check}\nCheck returned with an expected value >> {outputResult}')
            summary.append(result)
    except:
        result = ('-Failed to test the PowerShell command >> {command} with the test value >> {check}')
        print(result)
        summary.append(result)
        sys.exit(1)

def testACommand(command, check):
    try:
        testingCommand = command
        command1 = testingCommand.split()
        print(f'Testing command {command}. . .')
        output = subprocess.run(command1, capture_output=True, text=True)
        result = str(output.stdout).splitlines()
        outputResult = " ".join(map(str, result))
        if outputResult != check:
            print(f'Command \'{command}\' returned an unexpected value >> \'{outputResult}\'\nExpected >> \'{check}\'')
            result = ('-Tested the command >> {command} with the test value >> {check}\nCheck returned with an unexpected value >> {outputResult}')
            summary.append(result)
            sys.exit(1)
        else:
            print(f'Command \'{command}\' returned the expected value')
            result = ('-Tested the command >> {command} with the test value >> {check}\nCheck returned with an expected value >> {outputResult}')
            summary.append(result)
    except:
        result = ('-Failed to test the command >> {command} with the test value {check}')
        summary.append(result)
        sys.exit(1)

def install(package):
    try:
        installList = ['choco', 'install', '-y']
        pkg = package.split()
        command1 = (installList + pkg)
        print(f'Installing {package}. . .')
        output = subprocess.run(command1)
        print(f'{package} installed successfully!')
        result = ('-Installed the package >> {package}')
        summary.append(result)
    except:
        result = ('-Failed to install the package >> {package}')
        summary.append(result)
        sys.exit(1)


try:
    testAPSCommand('Get-ExecutionPolicy', 'RemoteSigned')
except:
    try:
        runAPSCommand('Set-ExecutionPolicy RemoteSigned')
    except:
        print('Error setting ExecutionPolicy')
        sys.exit(1)

try:
    test('choco')
except:
    try:
        runAPSCommand('Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://chocolatey.org/install.ps1\'))')
        refreshenv()
    except:
        print('Error installing Chocolatey')
        sys.exit(1)
    finally:
        try:
            test('choco')
        except:
            print('Error installing Chocolatey')
            sys.exit(1)

try:
    test('gh')
except:
    try:
        install('gh')
        refreshenv()
    except:
        print('Error installing GitHub')

try:
    test('git')
except:
    try:
        install('git.install')
        refreshenv()
    except:
        print('Error installing git')

try:
    test('python --version')
except:
    try:
        install('python')
        refreshenv()
    except:
        print('Error installing Python')

try:
    test('notepad++ -systemtray')
except:
    try:
        install('notepadplusplus')
        refreshenv()
    except:
        print('Error installing Notepad++')

try:
    runAPSCommand('(Get-Item "C:\Program Files\Google\Chrome\Application\chrome.exe").VersionInfo')
except:
    try:
        install('googlechrome')
        refreshenv()
    except:
        print('Error installing Google Chrome')

try:
    test('code --version')
except:
    try:
        install('vscode')
        refreshenv()
    except:
        print('Error installing Visual Studio Code')

try:
    with open("file.json", 'w') as f:
        json.dump(summary, f, indent=2)
except:
    print('Error creaeting summary file')

try:
    print('\n'.join(map(str, summary)))
except:
    print('Error printing event summary')
    sys.exit(1)
