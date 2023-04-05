import pyautogui
import win32gui
import datetime
import time
import home_assistant_requests as ha
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_clock_and_process():
    # Finds the game window and gets its size
    window = pyautogui.getWindowsWithTitle('DREDGE')[0]
    game_screen_size = win32gui.GetWindowRect(window._hWnd)

    # Exact clock coordinates on screen
    # The default resolution is 1920x1080
    region_width = 63
    region_height = 25
    region_x = (game_screen_size[2] - game_screen_size[0]) // 2 - region_width // 2
    region_y = 37

    # Captures the clock and processes it
    capture = pyautogui.screenshot(region=(game_screen_size[0]+region_x, game_screen_size[1]+region_y, region_width, region_height))
    recognized_text = pytesseract.image_to_string(capture, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789:')
    return recognized_text

skip_6 = False
skip_17 = False
skip_18 = False
skip_20 = False

while True:
    clock = capture_clock_and_process().rstrip()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f'{clock} | {current_time}')
    # Around 06:00, the lights are change to white, turned back on and slowly gets brighter
    if clock >= "06:00" and skip_6 == False:
        ha.light_post_all_thread(ha.entities_list, 255, 'white', 5)
        print('6 AM')
        skip_6 = True
        
    # Around 17:30, the lights are slowly dimmed
    if clock >= "17:30" and skip_17 == False:
        ha.light_post_all_thread(ha.entities_list, 100, 'white', 5)
        skip_17 = True
        print('17:30 PM')
        
    # Around 18:30, the lights are slowly changed to blue
    if clock >= "18:30" and skip_18 == False:
        ha.light_post_all_thread(ha.entities_list, 255, 'blue', 5)
        skip_18 = True
        print('18:30 PM')
        
    # Around 20:00, the lights are slowly dimmed
    if clock >= "20:00" and skip_20 == False:
        ha.light_post_all_thread(ha.entities_list, 100, 'blue', 5)
        skip_20 = True
        print('20:00 PM')
    # Around 21:00, the lights are slowly turned off
    if clock >= "21:00":
        ha.light_post_off_all_thread(ha.entities_list, 0)                    
        skip_6 = False
        skip_17 = False
        skip_18 = False
        skip_20 = False
        print('21:00 PM')
        
    # Read clock every 2 seconds
    time.sleep(2)
