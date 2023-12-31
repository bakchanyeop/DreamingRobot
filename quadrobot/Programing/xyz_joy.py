##################################################
##    꿈꾸는 로봇 Quadruped Robot Program          #
##  https://www.youtube.com/@Dreamingrobot       #
## https://github.com/bakchanyeop/DreamingRobot/ #
##################################################
## 저작권은 꿈꾸는 로봇 에 있습니다                                                         #
## Copyright(C) 2023. DreamingRobot-BAKCHANYEOP. All rights reserved.#


from dynamixel_sdk import *
import time
import math
import pygame
import threading


a_leg=13
b_leg=13
shder=3.5 #sholder cm(new)


    
def CTD(data):
    degrees=round((data/300)*1023)
    return degrees


# 사용할 포트와 프로토콜 버전 설정
PORT = '/dev/ttyUSB0'
BAUDRATE = 1000000
PROTOCOL_VERSION = 1.0




# 모터 ID와 모터의 최대, 최소 각도 설정
ID = [13, 17, 18, 10, 12, 2]
MIN_ANGLE = 0
MAX_ANGLE = 1023



index=0
# 포트 열기
portHandler = PortHandler(PORT)
portHandler.openPort()

# 포트 설정
packetHandler = PacketHandler(PROTOCOL_VERSION)
#packetHandler.setBaudRate(BAUDRATE)

portHandler.setBaudRate(BAUDRATE)



def on_key(event):
    print('Key Pressed:', event.name)

# 모터 초기 설정
for id in ID:

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, id, 24, 1) # 모터 회전 가능하도록 설정
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, id, 32, 22) # 모터 최소 speed
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, id, 6, MIN_ANGLE) # 모터 최소 각도 설정
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, id, 8, MAX_ANGLE) # 모터 최대 각도 설정
    print('seeeeeeeet')

# groupSyncWrite 객체 생성
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, 30, 4)

Center_Data=CTD(150)


################

# 초기화
pygame.init()
pygame.joystick.init()



# 조이스틱 개수 확인
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joystick detected.")
    exit()

# 첫 번째 조이스틱 가져오기
joystick = pygame.joystick.Joystick(0)
joystick.init()

# 인터럽트 함수
def perform_interrupt(direction):
    print("Interrupt occurred! Direction: {}".format(direction))
    # 여기에 인터럽트 동작을 수행하는 코드를 추가하세요

# 이벤트 처리 스레드



def event_thread():
    
    global my_walk 
    global my_walk_1
    global delay ##초기 상태
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:  # 조이스틱 축 움직임 이벤트
                axis = event.axis
                value = event.value

                if axis == 0:  # X 축 (좌우)
                    if value < -0.5:
                        perform_interrupt("Left")
                        my_walk = [(0, 5, 15),(0, 4, 18),(0, 2, 18),(0, 0, 18),(0, 5, 15),(0, 4, 18)]
                        my_walk_1 =[(0, -5, 15),(0, -4, 18),(0, -2, 18), (0, 0, 18),(0, -5, 15),(0, -4, 18)]
                        delay=0.03
                    elif value > 0.5:
                        perform_interrupt("Right")
                        my_walk_1= [(0, 5, 15),(0, 4, 18),(0, 2, 18),(0, 0, 18),(0, 5, 15),(0, 4, 18)]
                        my_walk =[(0, -5, 15),(0, -4, 18),(0, -2, 18), (0, 0, 18),(0, -5, 15),(0, -4, 18)]
                        delay=0.03
                elif axis == 1:  # Y 축 (전후)
                    if value < -0.5:
                        perform_interrupt("Forward")        
                        my_walk = [(2,0,18),(-2,0,18),(-6,0,18), (3,0,15),(2,0,18),(-2,0,18)]
                        my_walk_1 = [(2,0,18),(-2,0,18),(-6,0,18), (3,0,15),(2,0,18),(-2,0,18)]
                        delay=0.01
                    elif value > 0.5:
                        perform_interrupt("Backward")
                        my_walk = [(2,0,18),(-3,0,15),(-3,0,18), (-1,0,18),(2,0,18),(-3,0,15)]
                        my_walk_1 =  [(2,0,18),(-3,0,15),(-3,0,18), (-1,0,18),(2,0,18),(-3,0,15)]
                        delay=0.01
                else:
                    print("stop")
                    my_walk = [(0,0,18),(0,0,18),(0,0,18), (0,0,18),(0,0,18),(0,0,18)]
                    my_walk_1 = [(0,0,18),(0,0,18),(0,0,18), (0,0,18),(0,0,18),(0,0,18)]
            elif event.type == pygame.JOYBUTTONDOWN:  # 조이스틱 버튼 누름 이벤트
                button = event.button
                print("Button {} pressed".format(button))
                # 여기에 버튼 누름 이벤트를 처리하는 코드를 추가하세요
                if button == 1:
                    print("stop")
                    my_walk = [(0,0,18),(0,0,18),(0,0,18), (0,0,18),(0,0,18),(0,0,18)]
                    my_walk_1 = [(0,0,18),(0,0,18),(0,0,18), (0,0,18),(0,0,18),(0,0,18)]##초기 상태
            
            elif event.type == pygame.JOYBUTTONUP:  # 조이스틱 버튼 떼기 이벤트
                button = event.button
                print("Button {} released".format(button))
                my_walk = [(0,0,18),(0,0,18),(0,0,18), (0,0,18),(0,0,18),(0,0,18)]
                my_walk_1 = [(0,0,18),(0,0,18),(0,0,18), (0,0,18),(0,0,18),(0,0,18)]
                # 여기에 버튼 떼기 이벤트를 처리하는 코드를 추가하세요
my_walk = [(0,0,18),(0,0,18),(0,0,18), (0,0,18),(0,0,18),(0,0,18)]
my_walk_1 = [(0,0,18),(0,0,18),(0,0,18), (0,0,18),(0,0,18),(0,0,18)]
delay=0.01
# 이벤트 처리 스레드 시작
event_thread = threading.Thread(target=event_thread)
event_thread.daemon = True
event_thread.start()




# 메인 루프
while (1):
    


     
    count=4    
    for count in range(0,count):
    
##################


        x, y, z = my_walk[count]        
      
        W=math.atan(x/z)*180/3.14
        S=(math.atan(3.5/z)-math.atan((3.5+y)/z))*180/3.14
        A=math.sqrt(x**2+y**2)
        L=math.sqrt(z**2+A**2)
        C=math.acos((13**2+13**2-L**2)/(2*13*13))*180/3.14



        S_out=S        	
        C_Degree=C
        walk_deg=W      
##################        
     
        
        print('OutPut')

    

        
        x, y, z = my_walk_1[count+2]        
      
        W=math.atan(x/z)*180/3.14
        S=(math.atan(3.5/z)-math.atan((3.5+y)/z))*180/3.14
        A=math.sqrt(x**2+y**2)
        L=math.sqrt(z**2+A**2)
        C=math.acos((13**2+13**2-L**2)/(2*13*13))*180/3.14

        
        S_out_1=S        
        C_Degree_1=C
        walk_deg_1=W        

        w_offset=4





####################
        #dxl_addparam_result = groupSyncWrite.addParam(groupSyncWrite, 13, 50)
       # dxl_addparam_result = groupSyncWrite.addParam(groupSyncWrite, 2, 50)
       # dxl_addparam_result = groupSyncWrite.addParam(groupSyncWrite, 1, 50)

        print(my_walk)
        print(my_walk_1)

        time.sleep(0.09)
        dxl_goal_position=Center_Data-CTD(S_out)
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(13, param_goal_position) # 어깨 관절 모터 각도 추가


        dxl_goal_position=Center_Data+CTD(S_out_1)
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(2, param_goal_position) # 어깨 관절 모터 각도 추가

        dxl_goal_position=Center_Data+CTD(S_out_1)
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(1, param_goal_position) # 어깨 관절 모터 각도 추가


        dxl_goal_position=Center_Data-CTD(S_out)
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(4, param_goal_position) # 어깨 관절 모터 각도 추가




        

##########################
        print('1STEP')
        dxl_goal_position=Center_Data+int((CTD(180)-CTD(C_Degree))/2)-CTD(int(walk_deg)-w_offset)
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(17, param_goal_position) # 모터 각도 추가
    #    print(param_goal_position)


        dxl_goal_position=Center_Data-int((CTD(180)-CTD(C_Degree))/2)+CTD(int(walk_deg)-w_offset)
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(15, param_goal_position) # 모터 각도 추가
##########################



        dxl_goal_position=Center_Data+int((CTD(180)-CTD(C_Degree_1))/2)-CTD(int(walk_deg_1)-w_offset)
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(10, param_goal_position) # 모터 각도 추가


        dxl_goal_position=Center_Data-int((CTD(180)-CTD(C_Degree_1))/2)+CTD(int(walk_deg_1)-w_offset)
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(3, param_goal_position) # 모터 각도 추가
##########################


        print('2STEP')
        dxl_goal_position=Center_Data-(CTD(180)-CTD(C_Degree))
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)),     DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(18, param_goal_position)
        print('SAME')
    #    print(dxl_goal_position)

        dxl_goal_position=Center_Data+(CTD(180)-CTD(C_Degree)) #-60 offset
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)),     DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(16, param_goal_position)
  #      print(dxl_goal_position)
##########################


        dxl_goal_position=Center_Data-(CTD(180)-CTD(C_Degree_1)) #-60 offset
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)),     DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(12, param_goal_position)


        dxl_goal_position=Center_Data+(CTD(180)-CTD(C_Degree_1))
        param_goal_position =[DXL_LOBYTE(DXL_LOWORD(dxl_goal_position)),     DXL_HIBYTE(DXL_LOWORD(dxl_goal_position)),DXL_LOBYTE(DXL_HIWORD(dxl_goal_position)), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position))]
        dxl_addparam_result = groupSyncWrite.addParam(5, param_goal_position)
##########################


        dxl_comm_result = groupSyncWrite.txPacket() # 모터 각도 한 번에 설정
        print("설정!!")
        time.sleep(delay) ###time.sleep(0.01)
        groupSyncWrite.clearParam()




# 포트 닫기
portHandler.closePort() 


# 종료
pygame.quit()
######

