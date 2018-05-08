import radio
from microbit import *

#设定接口地址，接口地址为16进制数据
PCA9685_ADDRESS = 0x40
MODE1 = 0x00
PRESCALE = 0xFE
M1A = 0x1
M2B=0x4
S1 = 0x01
S2 = 0x02
S3 = 0x03
initialized = False

#对接口进行初始化
def initPCA9685():
    global initialized
    i2c.write(PCA9685_ADDRESS, bytes([MODE1, MODE1]))#对串脚的输入方式为i2c.write且输入的数据形式为字节串
    setFreq(50)
    for idx in range(16):
        setPwm(idx, 0, 0)
    initialized = True

def setFreq(freq):
    prescaleval = 25000000
    prescaleval /= freq
    prescaleval -= 1
    prescale = int(prescaleval)
    oldmode = MODE1
    newmode = (oldmode & 0x7F)| 0x10
    i2c.write(PCA9685_ADDRESS, bytes([MODE1, newmode]))
    i2c.write(PCA9685_ADDRESS, bytes([PRESCALE, prescale]))
    i2c.write(PCA9685_ADDRESS, bytes([MODE1, oldmode]))
    i2c.write(PCA9685_ADDRESS, bytes([MODE1, oldmode | 0xa1]))

def setPwm(channel, on, off):#对串口进行参数设置（important
    if channel < 0 or channel > 15:
        return
    buf = []#由于数据都要以字节串的形式输入，故先写入列表再统一转为字节串
    buf.append(0x06 + 4 * channel)
    buf.append(on & 0xff)
    buf.append((on >> 8) & 0xff)
    buf.append(off & 0xff)
    buf.append((off >> 8) & 0xff)
    buf = bytes(buf)
    i2c.write(PCA9685_ADDRESS, buf)

def Servo(index,degree):#对舵机进行设置，参数为舵机序号、旋转角度
    if not initialized:
        initPCA9685()
    v_us = (degree * 1800 / 180 + 600)
    value = int(v_us * 4096 / 20000)
    setPwm(index + 7, 0, value)

def MotorRun(index, speed):#对直流电机进行设置，参数为电机序号、速度
    if not initialized:
        initPCA9685()
    speed = speed * 16
    if speed >= 4096:
        speed = 4095
    if speed <= -4096:
        speed = -4095
    pp = (index - 1) * 2
    pn = (index - 1) * 2 + 1
    if speed >= 0:
        setPwm(pp, 0, speed)
        setPwm(pn, 0, 0)
    else:
        setPwm(pp, 0, 0)
        setPwm(pn, 0, -speed)

def MotorRunDual(motor1, speed1, motor2, speed2):#同时对两个电机进行参数输入
    MotorRun(motor1, speed1)
    MotorRun(motor2, speed2)

radio.on()#打开无线电接收器
while True:
    if radio.receive()=='0':#收到打开小花的无线电指令
        Servo(S1, 750)#控制3个舵机运动
        sleep(1000)
        Servo(S2, 800)
        sleep(1000)
        Servo(S3, 900)
        sleep(1000)
    elif radio.receive() == 'A':#收到向前走的指令
        MotorRunDual(M1A, -100, M2B, 100)
        sleep(2000)
        MotorRunDual(M1A, 0, M2B, 0)
    elif radio.receive()=='B':#收到向后走的指令
        MotorRunDual(M1A, 100, M2B, -100)
        sleep(2000)
        MotorRunDual(M1A, 0, M2B, 0)
    elif radio.receive()=='C':
        MotorRunDual(M1A, -100, M2B, 0)
        sleep(2000)
        MotorRunDual(M1A, 0, M2B, 0)
    elif radio.receive()=='D':
        MotorRunDual(M1A, 0, M2B, 100)
        sleep(2000)
        MotorRunDual(M1A, 0, M2B, 0)
    elif radio.receive()=='1':#收到关闭小花的无线电指令
        Servo(S1, 0)
        sleep(1000)
        Servo(S2, 450)
        sleep(1000)
        Servo(S3, 600)
        sleep(1000)
