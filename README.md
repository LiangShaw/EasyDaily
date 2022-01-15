# EasyDaily
用 pyautogui 写的 RPA 脚本

## Prerequisites:
- python 3.5 以上版本
- pyautogui, pandas 库  

## Userguide:
- "img" 里要指定图像名称，多个图像请以 ","(注意英文半角) 分隔。当指定多个图像时，默认从前到后依次在屏幕上寻找，找到后即终止，进行后续操作。图像保存格式一律为 <font color='red'>PNG</font> 格式。
- "no action" 相当于wait， 需要指定图像。当屏幕中出现图像时，"no action" 停止，进行后续操作。往往用来等待上一步操作后图像的出现。
- "no action", "left click", "left double click", "right click", "input" 候选框中 "1" 代表执行操作，"0" 代表不执行，不选时默认为 "0" 。当选中多个操作时，默认先后顺序为：no action → left click → left double click → right click → input → keyboard_value。然而这样在很多时候操作没有意义，不建议同行指定多个非 "no action" 命令。
- "max wait time" 默认是 60S ，当到达等待时间耗尽时，屏幕上仍未找到图像，程序终止。
- "click location X ratio", "click location Y ratio"，分别代表: 相对于图像，从左到右、从上到下鼠标点击位置。默认是图像中心 (Xratio=0.5, Yratio=0.5)。设置范围目前限制在 (-2, 2) 。
- "ImgSimilarity" 表示识别图像的可信度，范围在0~1之间。默认是 0.8。当有多个符合条件的图像出现时， 左上角 图像优先级最高，可通过提高可信度增加图像选择的准确度。尽量保证图像唯一性。如图像背景颜色可能会变动，可调低可信度以获取图像。
- 在不同操作行之间，不要插入空行。扫描到空行时，认为后续没有操作，程序终止。
-	不要对文件头、Sheet1 名字 随意进行改动（除非自己改脚本）
-	左右手设置：左击/右击都是基于鼠标的设置。在默认情况下是右手用户，如果是左手用户，将hand一栏 'right' 改为'left'即可。
