# PSRemoteExecuter
## _Suitable only for Windows platforms_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This package will help you to execute remote PowerSell script on other Windows platforms in your domain. 

## Features

- Execute local PowerShell scripts
- Execute remote PowerShell scripts (Using invoke-command PS command)


##Using
install PSRemoter using pip:<br>
pip install PSRemoter

powershell=False (default) execute as batch script
```
from psremoter.connector import Execute
exec= Execute(hostname="hostname", username="username" , password='password', domain='myDomain', command="hostname", powershell=True)

#Execute command on remote host
exec.remote_execution()

#Read execution status
print(exec.status) #True

#Read return code
print(exec.return_code) #0 

#Read console output
print(exec.output) #DnsServer01
````
