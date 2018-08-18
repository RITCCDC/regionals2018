# RIT CCDC 2018 Practice Infrastructure

This repository contains Ansible playbooks to automatically deploy the Infrastructure
used during the 2018 NECCDC regional competition.

## WinRM setup

Run these commands on the Windows hosts in order to enable WinRM.
```
PS> Enable-PSRemoting -Force
PS> Set-Item wsman:\localhost\client\trustedhosts *
PS> winrm set winrm/config/client/auth '@{Basic="true"}'
PS> winrm set winrm/config/service/auth '@{Basic="true"}'
PS> winrm set winrm/config/service '@{AllowUnencrypted="true"}'
```
Make sure to run these commands as Administrator.

These playbooks require [Selenium](https://pypi.org/project/selenium/) and [geckodriver](https://github.com/mozilla/geckodriver/releases).
