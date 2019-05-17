# This is the link to download Python 3.6.7 from Python.org
# See https://www.python.org/downloads/
$pythonUrl = "https://www.python.org/ftp/python/3.6.7/python-3.6.7-amd64.exe"

# This is the directory that the exe is downloaded to
$tempDirectory = "C:\temp_provision\"

# Installation Directory
# Some packages look for Python here
$targetDir = "C:\Python36"

# create the download directory and get the exe file
$pythonNameLoc = $tempDirectory + "python367.exe"
New-Item -ItemType directory -Path $tempDirectory -Force | Out-Null
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
(New-Object System.Net.WebClient).DownloadFile($pythonUrl, $pythonNameLoc)

# These are the silent arguments for the install of python
# See https://docs.python.org/3/using/windows.html
$Arguments = @()
$Arguments += "/i"
$Arguments += 'InstallAllUsers="1"'
$Arguments += 'TargetDir="' + $targetDir + '"'
$Arguments += 'DefaultAllUsersTargetDir="' + $targetDir + '"'
$Arguments += 'AssociateFiles="1"'
$Arguments += 'PrependPath="1"'
$Arguments += 'Include_doc="1"'
$Arguments += 'Include_debug="1"'
$Arguments += 'Include_dev="1"'
$Arguments += 'Include_exe="1"'
$Arguments += 'Include_launcher="1"'
$Arguments += 'InstallLauncherAllUsers="1"'
$Arguments += 'Include_lib="1"'
$Arguments += 'Include_pip="1"'
