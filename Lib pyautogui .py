import pyautogui
print(pyautogui.size())
#pyautogui.moveTo(100,100,duration=1)
x=634; y=159
print(pyautogui.position(x,y))
pyautogui.click(x,y,duration=1)
#pyautogui.hotkey()
pyautogui.hotkey("ctrlleft","a")
pyautogui.hotkey("ctrlleft","c")
pyautogui.click(x,y*2,duration=1)
pyautogui.hotkey("ctrlleft","v")
#apyautogui.hotkey('winleft', 'd')