import subprocess
import time
import json

summary = ['cat','dog']

with open('Data' + time.strftime("%a%d%b%Y~%H.%M.%S.%p") + ".json", 'w') as f:
    json.dump(summary, f, indent=2)
