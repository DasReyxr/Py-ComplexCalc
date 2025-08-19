import pyautogui
print(pyautogui.size())
#pyautogui.moveTo(100,100,duration=1)
x=143; y=100
print(pyautogui.position(x,y))
pyautogui.click(x,y,duration=1)
#pyautogui.hotkey()
pyautogui.hotkey('winleft', '1')
pyautogui.hotkey('alt', 'w')
#pyautogui.hotkey('alt', 'w')
x=143;y=100
pyautogui.click(x,y,duration=1)
#pyautogui.hotkey("ctrlleft","alt","shift","7")
#pyautogui.click(x,y,duration=1)
pyautogui.write("Luis")
x=143;y=225
pyautogui.click(x,y,duration=5)
for i in range(1,50):
    pyautogui.write("Hola")
    pyautogui.hotkey("enter")
    
    i+=1


# pyautogui.hotkey("ctrlleft","c")
# pyautogui.click(x,y*2,duration=1)
# pyautogui.hotkey("ctrlleft","v")
