import radio
from microbit import *

radio.on()#打开无线电发射器
while True:
    #通过加速度检测器获取加速度信息，用于感应操作器的操作
    left=accelerometer.get_x()
    forward=accelerometer.get_z()
    flower_open=0
    flower_close=0
    flower_open=button_a.get_presses()
    flower_close=button_b.get_presses()
    if abs(forward)*2/3>=abs(left):#如果前倾大于左倾，这是为了保证不会同时进行前进和转弯
        if forward < -360:
            radio.send('A')#发射信号
            display.show(Image.ARROW_N)#显示箭头
        elif forward > 360:
            radio.send('B')
            display.show(Image.ARROW_S)
        else:
            radio.send('stop')
            display.show(Image.SQUARE)
    else:
        if left > 360:
            radio.send('C')
            display.show(Image.ARROW_E)
        elif left < -360:
            radio.send('D')
            display.show(Image.ARROW_W)
        else:
            display.show(Image.SQUARE)
    if flower_open==1:
        radio.send('0')
        display.show(Image.BUTTERFLY)
    elif flower_close==1:
        radio.send('1')
        display.show(Image.SQUARE_SMALL)
    sleep(800)
    display.clear()
