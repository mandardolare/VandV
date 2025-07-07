import can
import time

recvid=0x7e0
bus = can.interface.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000)

cmd1003 = [2, 16, 3, 0, 0, 0, 0, 0]

reply1003= can.Message(arbitration_id=0x07E8,
                      data= [0x06, 0x50, 0x03, 0x00, 0x32, 0x01, 0xEA, 0xAA],
                      is_extended_id=False)

requestroutinereply= can.Message(arbitration_id=0x07E8,
                      data=[0x04, 0x71, 0x01, 0x04, 0x06, 0x00, 0x00, 0x00],
                      is_extended_id=False) 

requestroutinereply2= can.Message(arbitration_id=0x07E8,
                      data=[0x04, 0x71, 0x02, 0x04, 0x06, 0x00, 0xAA, 0xAA],
                      is_extended_id=False) 

requestroutinereply3= can.Message(arbitration_id=0x07E8,
                      data=[0x04, 0x71, 0x03, 0x04, 0x06, 0x00, 0xAA, 0xAA],
                      is_extended_id=False) 


reply2701= can.Message(arbitration_id=0x07E8,
                      data=[0x06, 0x67, 0x01, 0xAF, 0x7E, 0xA1, 0x48, 0x00],
                      is_extended_id=False)

reply2702= can.Message(arbitration_id=0x07E8,
                      data=[0x02, 0x67, 0x02, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA],
                      is_extended_id=False) 

reply3E= can.Message(arbitration_id=0x07E8,
                      data=[0x02, 0x7E, 0x00, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA],
                      is_extended_id=False)





while True:
  a= bus.recv()
  getdata=list(a.data)
  print(getdata)
  if a.arbitration_id == 2016 and getdata[0]== 2 and getdata[1]==62 and getdata[2]== 0: 
    bus.send(reply3E)
  if a.arbitration_id == 2016 and getdata[0]== 2 and getdata[1]==16 and getdata[2]== 3: 
    bus.send(reply1003)
  if a.arbitration_id == 2016 and getdata[0]== 2 and getdata[1]==39 and getdata[2]== 1: 
    bus.send(reply2701)  
  if a.arbitration_id == 2016 and getdata[0]== 6 and getdata[1]==39 and getdata[2]== 2: 
    bus.send(reply2702)   
  if a.arbitration_id == 2016 and getdata[0]== 4 and getdata[1]==49 and getdata[2]== 1 and getdata[3]==4 : 
    bus.send(requestroutinereply)  
  if a.arbitration_id == 2016 and getdata[0]== 4 and getdata[1]==49 and getdata[2]== 2 and getdata[3]==4: 
    bus.send(requestroutinereply2)  
  if a.arbitration_id == 2016 and getdata[0]== 4 and getdata[1]==49 and getdata[2]== 3 and getdata[3]==4: 
    bus.send(requestroutinereply3)    
               
             
       