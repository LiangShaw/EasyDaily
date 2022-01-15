'''
Filename: EasyDaily.py
Author: Shaw
My blog: https://liangshaw.github.io/
'''

import pyautogui
import time
#import pyperclip
import pandas as pd
import sys
import warnings

warnings.filterwarnings('ignore')

def mouseClick(x,y,clickTimes=1,lOrR='PRIMARY',hand='right',reTry=1,sleeptime=0.0,interval=0.0,duration=0.0):
    if hand == 'right':
        pass
    else:
        if lOrR == 'left':
            lOrR = 'right'
        elif lOrR == 'right':
            lOrR = 'left'
    pyautogui.click(x,y,clicks=clickTimes,interval=interval,duration=duration,button=lOrR)
    time.sleep(sleeptime)
            
def gain_click_pos(command_dict, max_wait_time,confidence):
    interval_time = 0.02
    
    start_time = time.time()
    # multiple alternative images seperated by comma
    images = [ img.strip() for img in command_dict['img'].split(',') ]
    loc=False
    # img pos
    while time.time() - start_time <= max_wait_time:
        for img in images:
            loc = pyautogui.locateOnScreen(img, confidence=confidence)
            if loc:break
        if loc: break
    if loc:pass
    else: # no img found
        sys.stderr.write(f'Within {max_wait_time}s, Not img found. Exit.\n')
        return False
    
    # default point is at center
    if pd.isna(command_dict['click location X ratio']):
        xratio = 0.5
    else:
        xratio = command_dict['click location X ratio']
    if pd.isna(command_dict['click location Y ratio']):
        yratio = 0.5
    else:
        yratio = command_dict['click location Y ratio']

    click_pos_x = loc.left + xratio * loc.width
    click_pos_y = loc.top + yratio * loc.height
    return  click_pos_x, click_pos_y

def key_board_reference(keyboard):
    # keyboard is one of c('copy','paste','select all','delete','enter') at current
    if keyboard == 'enter':
        pyautogui.press('enter')
    elif keyboard == 'select all':
        pyautogui.hotkey('ctrl','a')
    elif keyboard == 'copy':
        pyautogui.hotkey('ctrl', 'c')
    elif keyboard == 'paste':
        pyautogui.hotkey('ctrl', 'v')
    elif keyboard == 'backspace':
        pyautogui.press('backspace')
    elif keyboard == 'win':
        pyautogui.press('win')
        time.sleep(0.1)
    
def act(command_dict, handmode='right'):
    confidence = 0.8 if pd.isna(command_dict['ImgSimilarity']) else command_dict['ImgSimilarity']
    max_wait_time = 60 if pd.isna(command_dict['max wait time/s']) else command_dict['max wait time/s']
    if command_dict['no action'] == 1:
        # wait for image appearing
        if pd.isna(command_dict['img']):
            sys.stderr.write('No action requires a image as a marker.')
            return False
        start = time.time()
        images = [ img.strip() for img in command_dict['img'].split(',') ]
        while time.time() - start <= max_wait_time:
            for img in images:
                loc = pyautogui.locateOnScreen(img, confidence=confidence)
                if loc:break
            if loc: break
        if loc:pass
        else:
            sys.stderr.write(f'Within {max_wait_time}s, no target img found. Exit\n')
            return False

    if command_dict['left click'] == 1 or command_dict['right click'] == 1 or command_dict['left double click'] == 1:
        click_pos = gain_click_pos(command_dict, max_wait_time, confidence)
        if not click_pos:
            sys.stderr.write('No image found. Exit')
            return False
        else:
            click_x, click_y = click_pos
            # click once in default
            clicktimes = command_dict['click times'] if not pd.isna(command_dict['click times']) else 1
            if command_dict['left click'] == 1:
                mouseClick(click_x, click_y, clickTimes = clicktimes, lOrR = 'left', hand=handmode)
            elif command_dict['left double click'] == 1:
                if handmode == 'right':
                    pyautogui.doubleClick(click_x, click_y, button = 'left')
                else:
                    pyautogui.doubleClick(click_x, click_y, button = 'right')
            else:
                mouseClick(click_x, click_y, clickTimes = clicktimes, lOrR = 'right', hand=handmode)

    if command_dict['input'] == 1:
        if pd.isna(command_dict['input content']):
            sys.stderr.write('No input content set. Skip\n')
        else:
            pyautogui.typewrite(command_dict['input content'])
            
    # add press keyboard afterhere
    if not pd.isna(command_dict['keyboard_value']):
        key_board_reference(command_dict['keyboard_value'])
    return True
    

def read_xlsx_input(xlsxname,sheetname = 'Sheet1'):
    sheet1 = pd.read_excel(xlsxname, sheet_name=sheetname, header=0,index_col=None)
    columns = sheet1.columns
    hand = sheet1['hand'][0]
    print(hand + ' mode start:')
    act_dicts = []
    for acts in sheet1.values:
        if (pd.isna(acts)==1).all():
            break
        act_dicts.append({ k:v for k,v in zip(columns, acts) })
    return act_dicts,hand

def main():
    operation_xlsx = 'operations.xlsx'
    act_dicts, hand = read_xlsx_input(operation_xlsx)
    act_no = 1
    for commdict in act_dicts:
        signal = act(commdict, handmode=hand)
        if signal:
            sys.stdout.write(f'{act_no}. {commdict["img"]} finished.\n')
            act_no += 1
        else:
            sys.stderr.write('Exit. Please Check operations xlsx.\n')
            break
        
'''
act_dict content:

 'img',
 'no action',
 'left click',
 'left double click',
 'right click',
 'click times',
 'keyboard_value',
 'input',
 'input content',
 'wait time/s',
 'click location X ratio',
 'click location Y ratio'
'''

if __name__ == '__main__':
    main()