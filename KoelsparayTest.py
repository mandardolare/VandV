import can
import time

recvid=0x7e0

cmd1003 = [2, 16, 3, 0, 0, 0, 0, 0]
testerPresent=[2, 62, 0, 0, 0, 0, 0, 0]

rpm=[3, 34, 16, 89, 0, 0, 0, 0]
battery=[3, 34, 16, 13, 0, 0, 0, 0]
PID1420=[3, 34, 20, 32, 0, 0, 0, 0]
PID1123=[3, 34, 17, 35, 0, 0, 0, 0]
PID1222=[3, 34, 18, 34, 0, 0, 0, 0]
PID122B=[3, 34, 17, 43, 0, 0, 0, 0]

cmd2701 = [2, 39, 1,0, 0, 0, 0, 0]
#cmd2702 = [145,18,29,140,248,179, 46,42] 
cmd2702=[16 ,10, 39, 2, 229, 165, 63, 19]

startroutine=[16,17,49,1,0,24,0,0]
requestroutine=[4, 49, 3,0, 24, 0, 0, 0]

count = 1
count120 = 13

bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)


testerPresentreply=can.Message(arbitration_id=0x07E8,
                      data=[0x02, 0x7e, 0x00, 0x00, 0x00, 0x00,0xAA,0xAA],
                      is_extended_id=False)

rpmreply=can.Message(arbitration_id=0x07E8,
                      data=[0x05, 0x62, 0x10, 0x59, 0x00, 0x00, 0xAA, 0xAA],
                      is_extended_id=False)

PID1420reply=can.Message(arbitration_id=0x07E8,
                      data=[0x05, 0x62, 0x14, 0x20, 0x0D, 0x13, 0xAA, 0xAA],
                      is_extended_id=False)

PID1123reply=can.Message(arbitration_id=0x07E8,
                      data=[0x05, 0x62, 0x11, 0x23, 0x0C, 0x38, 0xAA, 0xAA],
                      is_extended_id=False)

PID1222reply=can.Message(arbitration_id=0x07E8,
                      data=[0x05, 0x62, 0x12, 0x22, 0x0C, 0x16, 0xAA, 0xAA],
                      is_extended_id=False)

PID122Breply=can.Message(arbitration_id=0x07E8,
                      data=[0x05, 0x62, 0x11, 0x2B, 0x0C, 0x16, 0xAA, 0xAA],
                      is_extended_id=False)

batteryreply=can.Message(arbitration_id=0x07E8,
                      data=[0x05, 0x62, 0x10, 0x0D, 0x02, 0x58, 0xAA, 0xAA],
                      is_extended_id=False)



reply1003= can.Message(arbitration_id=0x07E8,
                      data= [0x06, 0x50, 0x03, 0x00, 0x32, 0x01, 0xEA, 0xAA],
                      is_extended_id=False)

"""
reply2701 = can.Message(arbitration_id=0x07E8,
                      data=[0x10, 0x0A, 0x67, 0x01 , 0xFD , 0x16 , 0x65,  0xEE],  
                      is_extended_id=False) 

reply2701fw = can.Message(arbitration_id=0x07E8,
                      data=[0x21, 0xB1, 0xEA, 0x58 , 0x59 , 0xAA , 0xAA,  0xAA],  
                      is_extended_id=False)

"""

reply2701 = can.Message(arbitration_id=0x07E8,
                      data=[0x10, 0x0A, 0x67, 0x01 , 0x30, 0x2A, 0x93 ,0x13],  
                      is_extended_id=False) 


reply2701fw = can.Message(arbitration_id=0x07E8,
                      data=[0x21,0x47,0x83,0xDB,0x00,0xAA,0xAA,0xAA],  
                      is_extended_id=False)


flowcontrol= can.Message(arbitration_id=0x07E8,
                      data=[0x30, 0x00, 0x01, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA],
                      is_extended_id=False) 

reply2702= can.Message(arbitration_id=0x07E8,
                      data=[0x02, 0x67, 0x02, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA],
                      is_extended_id=False) 

startroutinereply= can.Message(arbitration_id=0x07E8,
                      data=[0x04, 0x71, 0x01, 0x05, 0x10, 0xAA, 0xAA, 0xAA],
                      is_extended_id=False) 

flowcontrolroutine= can.Message(arbitration_id=0x07E8,
                      data=[0x30, 0x00, 0x00, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA],
                      is_extended_id=False)

requestroutinereply= can.Message(arbitration_id=0x07E8,
                      data=[0x05, 0x71, 0x03, 0x05, 0x10, 0x00, 0xAA, 0xAA],
                      is_extended_id=False) 


while True:    
    try:
       a= bus.recv()
     #  print(a)
       getdata=list(a.data)
       print(getdata)
       if a.arbitration_id == recvid: 
         if getdata== testerPresent:
               bus.send(testerPresentreply)
         elif getdata==rpm:
               bus.send(rpmreply) 
         elif getdata==battery:
               bus.send(batteryreply) 
                     
         elif getdata==PID1420:
               bus.send(PID1420reply)            
         elif getdata==PID1123:
               bus.send(PID1123reply) 
         elif getdata==PID1222:
               bus.send(PID1222reply)    
         elif getdata==PID122B:
               bus.send(PID122Breply)                 



         elif getdata== cmd1003:
               bus.send(reply1003)
         elif getdata== cmd2701:
               bus.send(reply2701) 
               time.sleep(0.05)
               bus.send(reply2701fw)  
               
         elif getdata== cmd2702:
               time.sleep(0.01)
               bus.send(flowcontrol)               
               time.sleep(0.09)
               bus.send(reply2702)      
         elif getdata== startroutine:              
               print("data matched startroutine ")
               bus.send(flowcontrolroutine)
               time.sleep(0.5)
               bus.send(startroutinereply)  
                
         elif getdata== requestroutine:                   
               print("data matched startroutine ")
               count= count+1   
               print(count)   
               bus.send(requestroutinereply)
               time.sleep(0.2)  
         if count>=count120:
                print("count reached")    
                bus.send(can.Message(arbitration_id=0x07E8,
                      data=[0x10, 0x25, 0x71, 0x03, 0x00, 0x18, 0x02, 0x00],
                      is_extended_id=False)) 
                time.sleep(0.2)
                bus.send(can.Message(arbitration_id=0x07E8,
                      data=[0x21, 0x00, 0x00, 0x0A, 0x00, 0xFA, 0xAA, 0xAA],
                      is_extended_id=False)) 
                
                

                """
                bus.send(can.Message(arbitration_id=0x07E8,
                      data=[0x22, 0x00, 0x00, 0x0C, 0xD0, 0x00, 0x00, 0x0C],
                      is_extended_id=False)) 
                
                bus.send(can.Message(arbitration_id=0x07E8,
                      data=[0x23, 0xCE, 0x00, 0x00, 0x0C, 0xA4, 0x00, 0x00],
                      is_extended_id=False)) 
                
                bus.send(can.Message(arbitration_id=0x07E8,
                      data=[0x24, 0x0C, 0xA3, 0x00, 0x00, 0x0C, 0xA8, 0x00],
                      is_extended_id=False))
                
                bus.send(can.Message(arbitration_id=0x07E8,
                      data=[0x25, 0x00, 0x0C, 0xA1, 0xAA, 0xAA, 0xAA, 0xAA],
                      is_extended_id=False))
                
                """      
                count=0
         

            



    except can.CanError: 
        print("Message NOT sent")    