import subprocess
import time
import sys
import json

psPath = 'powershell.exe'
summary = []

def refreshenv():
    try:
        refresh = psPath + ' ' + 'refreshenv'
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
        result = (f'-Failed to run the PowerShell command >> {command}')
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
            result = (f'-Tested the PowerShell command >> {command} with the test value >> {check}\nCheck returned with unexpected value >> {outputResult}')
            summary.append(result)
            sys.exit(1)
        else:
            print(f'Command\'{command}\' returned the expected value')
            result = (f'-Tested the PowerShell command >> {command} with the test value >> {check}\nCheck returned with an expected value >> {outputResult}')
            summary.append(result)
    except:
        result = (f'-Failed to test the PowerShell command >> {command} with the test value >> {check}')
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
            result = (f'-Tested the command >> {command} with the test value >> {check}\nCheck returned with an unexpected value >> {outputResult}')
            summary.append(result)
            sys.exit(1)
        else:
            print(f'Command \'{command}\' returned the expected value')
            result = (f'-Tested the command >> {command} with the test value >> {check}\nCheck returned with an expected value >> {outputResult}')
            summary.append(result)
    except:
        result = (f'-Failed to test the command >> {command} with the test value {check}')
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
        result = (f'-Installed the package >> {package}')
        summary.append(result)
    except:
        result = (f'-Failed to install the package >> {package}')
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
finally:
    refreshenv()

try:
    test('choco')
except:
    try:
        runAPSCommand('Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://chocolatey.org/install.ps1\'))')
    except:
        print('Error installing Chocolatey')
        sys.exit(1)
    finally:
        refreshenv()
        try:
            test('choco')
        except:
            print('Error installing Chocolatey')
            sys.exit(1)
            refreshenv()        
finally:
    refreshenv()

try:
    test('gh')
except:
    try:
        install('gh')
    except:
        print('Error installing GitHub')
finally:
    refreshenv()

try:
    test('git')
except:
    try:
        install('git.install')
    except:
        print('Error installing git')
finally:
    refreshenv()

try:
    test('python --version')
except:
    try:
        install('python')
    except:
        print('Error installing Python')
finally:
    refreshenv()

try:
    test('notepad++ -systemtray')
except:
    try:
        install('notepadplusplus')
    except:
        print('Error installing Notepad++')
finally:
    refreshenv()

try:
    runAPSCommand('(Get-Item "C:\Program Files\Google\Chrome\Application\chrome.exe").VersionInfo')
except:
    try:
        install('googlechrome')
    except:
        print('Error installing Google Chrome')
finally:
    refreshenv()

try:
    test('code --version')
except:
    try:
        install('vscode')
    except:
        print('Error installing Visual Studio Code')
finally:
    refreshenv()

try:
    with open("Summary" + time.strftime("%a%d%b%Y\'%H.%M.%S%p\'" + ".json"), 'w') as f:
        json.dump(summary, f, indent=2)
except:
    print('Error creating summary file')

try:
    print('\n'.join(map(str, summary)))
except:
    print('Error printing event summary')
    sys.exit(1)
