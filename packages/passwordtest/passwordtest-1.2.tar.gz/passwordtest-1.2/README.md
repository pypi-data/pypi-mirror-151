# PY-passwordtest <small class='version_passwordtest'>V.1</small>
<p>This script is to measure password security from Brute Force and Dictionary (worldlist) attacks, by calculating the number, location, and character level. the longer and more varied the character of the password, the harder it is to crack</p>

### Installation

- Pip

  ```python -V```

  - Windows:
  
    `python -m pip install passwordtest`
  
  - Unix or Mac:
  
    `pip install passwordtest`
  
- GIT

  - Windows, Unix and Mac:
  
    ````
       git clone https://github.com/LcfherShell/passwordtest
       cd passwordtest
       python -m pip install . or python setup.py
    ````
### Usage Example

    1. from passwordtest.main import PasswordTest
    
    2. password = 'Hello'
    
    3. passwordtest = PasswordTest(active=True)#call class
    
    4. required_time = PasswordTest.__time__(text=data) #getting time
    
    5. sorttime = passwordtest.Sort_Pw(text=[required_time[0], required_time[1]) #sorttime by min and max
    
    6. badtime = sorttime[1] #time late
    
    7. goodtime = sorttime[0] #fastest time
    
    8. goodtime = passwordtest.Convert_Date(goodtime)#covert to time
    
    9. security = passwordtest._Score_Point(password)##get score point
    
    10.Precent =passwordtest.Precent_Safesecurity(security, badtime, password)#get percent security
    
    11.print(goodtime, security, Precent)

### Shell Demo

``open commandprompt and type
  passwordtest
``
## 
📫Bug reports: **LCFHERSHELL@TUTANOTA.COM**
<h3 align="left">Sociall Media:</h3>
<p align="left">
  <small>
    <a href="https://twitter.com/lcfershell" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="lcfershell" height="30" width="40" /></a>
    <a href="https://stackoverflow.com/users/18267661" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/stack-overflow.svg" alt="18267661" height="30" width="40" /></a>
    <a href="https://instagram.com/@lcfhershell" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="@lcfhershell" height="30" width="40" /></a>
    <a href="https://medium.com/@alfiandecker2" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/medium.svg" alt="@alfiandecker2" height="30" width="40" /></a>
    <a href="https://www.hackerrank.com/@alfiandecker2" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/hackerrank.svg" alt="@alfiandecker2" height="30" width="40" /></a>
 </small>
</p>
