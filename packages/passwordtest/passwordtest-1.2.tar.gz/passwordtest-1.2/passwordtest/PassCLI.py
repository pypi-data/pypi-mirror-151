import os, sys, time
try:
    from passwordtest.main import PasswordTest
except:
    from main import PasswordTest

class PasswordTest_CLi():
  """docstring for CLi"""
  def __init__(self):
    super(PasswordTest_CLi, self).__init__()
    self.PasswordTest = PasswordTest(active=True)
    self.timeout = 0.2
  def Banner(self):
    print("""

     ==============PASSWORD TEST==============          ********                        
     Menu: 1.Generated PW | press a or 1             ****      ***                
           2.Create by key| press b or 2            ***         ***                     
           3.Test PW      | press t or 12           ***  V.1.2  ***                     
           4.Helper       | press h or 0            ***         ****** *****            
           5.exit program | press e or control+z  ****************************          
     Info:                                        ****** ***   **********  ***         
     Each character has its own value, this       ****** *** ********   *****
     tool only predicts password security risk    ****** *** ********      *****        
     from bruteforce/cracking. The length of      ******   *   ******       ****     
     the password depends on the characters,      *******************         ****       
     used, GPU, and Program used for cracking     Create: LcfherShell          **


     X = Time required in Dictionary attack technique
     Y = Time required in bruteforce attack technique
        """)
  def Exec(self):
    self.Banner()
    session_test = 0
    def Validation(self, text, length, session_test=session_test):
        check_point = 0
        text = str(text)
        if not text:
            check_point +=1 
        if len(text)<length:
            check_point +=1

        if check_point==0:
            session_test = 1
        else:
            print(f"Not a password type, input data length of at least {length}")
            pass
        return session_test

    tests = 0
    creath = 0
    autox = 0
    session =''
    self.sessions = []
    while True:
        choice_command = input('Key Menu :>')
        if str(choice_command) == '1' or choice_command.lower() == 'a':
            for Length_later in self.PasswordTest.choice_langth:
                data = self.PasswordTest.generate_password(Length=Length_later, options = 'upper')
                output = self.PasswordTest.__time__(text=data)
                
                goodtime = self.PasswordTest.Convert_Date(output[0])
                badtime = self.PasswordTest.Convert_Date(output[1])
                getvaluess = self.PasswordTest.Sort_Pw(text=[badtime, goodtime])
                badtime = getvaluess[1]
                goodtime = getvaluess[0]
                security = self.PasswordTest._Score_Point(data)
                print("-----------------------------------------------------------------------")
                print("Password : ",data, "     | Length: ", Length_later)
                print("X Time : ", goodtime, " |Total Test Char:", self.PasswordTest._get_long_shifts_percharacter(output[0], output[1])[0])
                print("Y Time : ", badtime, " |Total Test Char:", self.PasswordTest._get_long_shifts_percharacter(output[0], output[1])[1])
                print('Security Level: ', security)
                print('Percentate: ', self.PasswordTest.Precent_Safe(security, output[0], data), '%')
                print("---------------------------------END-----------------------------------")
            session = f'createpw {autox}'
            autox +=1
            self.sessions.append(session)
        elif str(choice_command) == '2' or choice_command.lower() == 'b':
            data = input('Create Password :>')
            data = str(data)
            if Validation(self, data, 3):
                    for Length_later in self.PasswordTest.choice_langth:
                        if len(data)<Length_later:
                              data = self.PasswordTest.password_map(text=data, lths=Length_later)
                        else:
                            Length_later = len(data )
                        output = self.PasswordTest.__time__(text=data)
                        
                        goodtime = self.PasswordTest.Convert_Date(output[0])
                        badtime = self.PasswordTest.Convert_Date(output[1])
                        getvaluess = self.PasswordTest.Sort_Pw(text=[badtime, goodtime])
                        badtime = getvaluess[1]
                        goodtime = getvaluess[0]
                        security = self.PasswordTest._Score_Point(data)
                        print("-----------------------------------------------------------------------")
                        print("Password : ",data, "     | Length: ", Length_later)
                        print("X Time : ", goodtime, " |Total Test Char:", self.PasswordTest._get_long_shifts_percharacter(output[0], output[1])[0])
                        print("Y Time : ", badtime, " |Total Test Char:", self.PasswordTest._get_long_shifts_percharacter(output[0], output[1])[1])
                        print('Security Level: ', security)
                        print('Percentate: ', self.PasswordTest.Precent_Safe(security, output[0], data), '%')
                        print("---------------------------------END-----------------------------------")
                    session = f'createpw {creath}'
                    creath +=1
                    self.sessions.append(session)
        elif str(choice_command) == '12' or choice_command.lower() == 't':
            data = input('Password Test :>')
            data = str(data)
            if Validation(self, data, 5):
                    output = self.PasswordTest.__time__(text=data)

                    goodtime = self.PasswordTest.Convert_Date(output[0])
                    badtime = self.PasswordTest.Convert_Date(output[1])
                    getvaluess = self.PasswordTest.Sort_Pw(text=[badtime, goodtime])
                    badtime = getvaluess[1]
                    goodtime = getvaluess[0]
                    security = self.PasswordTest._Score_Point(data)
                    print("-----------------------------------------------------------------------")
                    print("Password : ",data, "     | Length: ", len(data))
                    print("X Time : ", goodtime, " |Total Test Char:", self.PasswordTest._get_long_shifts_percharacter(output[0], output[1])[0])
                    print("Y Time : ", badtime, " |Total Test Char:", self.PasswordTest._get_long_shifts_percharacter(output[0], output[1])[1])
                    print('Security Level: ', security)
                    print('Percentate: ', self.PasswordTest.Precent_Safe(security, output[0], data), '%')
                    #optionsz=Security, optionsy=time, optionsx=text
                    print("---------------------------------END-----------------------------------")
                    session = f'testpw {tests}'
                    tests +=1
                    self.sessions.append(session)
        elif str(choice_command) == '0' or choice_command.lower() == 'h':
                print("Usage: H to show help command")
                print("            Menu: 1.Generated PW | press a or 1                    ")
                print("                  2.Create by key| press b or 2                    ")
                print("                  3.Test PW      | press t or 12                    ")
                print("                  4.Helper       | press h or 0                   ")
                print("                  5.exit program | press e or control+z            ")
        elif choice_command.lower() == 'e':
                exit()
        elif choice_command.lower() == 'clear' or choice_command.lower() == 'cls':
                os.system("cls||clear")
                self.Banner()
        elif choice_command.lower() == 'riset':
                self.timeout = 0.2
                self.sessions.clear()
        elif choice_command.lower() == 'show':
                print(self.sessions) 
        time.sleep(self.timeout)



def Mainprogram():
    try:
        PasswordTest_CLi().Exec()
    except:
        pass
    print("Thanks Friends :V")
#data = outh.generate_text()
#data = outh.__time__(text='abcdfga')
#print(data)
#print(outh.Get_Days_Finish(data))


if __name__ == "__main__":
    Mainprogram()
    
 
