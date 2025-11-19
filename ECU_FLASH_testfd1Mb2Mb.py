import ctypes
from ctypes import *
import time

sendID=0x18DAF100
recivedID=0x18DA00F1

#sendID= 0x7E8
#recivedID=0x7E0
delaytime=0.05
pcan = ctypes.windll.LoadLibrary("PCANBasic.dll")
livepara=0
# Constants from PCANBasic.h
PCAN_USBBUS1 = 0x51
PCAN_MESSAGE_EXTENDED = 0x02
PCAN_MESSAGE_FD = 0x04
PCAN_ERROR_OK = 0x00000
PCAN_MESSAGE_BRS = 0x08 
PCAN_ISO_CAN_FD = 0x03
#PCAN_ISOFD_STANDARD = 0x01B
PCAN_PARAMETER_ON = 1
iso_mode = c_byte(PCAN_PARAMETER_ON)
result = pcan.CAN_SetValue(PCAN_USBBUS1,PCAN_ISO_CAN_FD, byref(iso_mode), sizeof(iso_mode))
recivedata=[] 
# Define the TPCANMsgFD structure
class TPCANMsgFD(Structure):
    _fields_ = [
        ("ID", c_uint),
        ("MSGTYPE", c_ubyte),
        ("DLC", c_ubyte),
        ("DATA", c_ubyte * 64),
        ("BRS", c_ubyte),
        ("ESI", c_ubyte),
    ]
 
class TPCANTimestampFD(Structure):
    _fields_ = [
        ("microseconds", c_uint64),
        ("millis", c_uint64),
        ("millis_overflow", c_uint64)
    ]
# Initialize CAN FD with bitrate string


bitrate = b"f_clock_mhz=80,nom_brp=8,nom_tseg1=15,nom_tseg2=4,nom_sjw=1,data_brp=2,data_tseg1=15,data_tseg2=4,data_sjw=1" #500/2mb
#bitrate = b"f_clock_mhz=80,nom_brp=16,nom_tseg1=15,nom_tseg2=4,nom_sjw=1,data_brp=2,data_tseg1=15,data_tseg2=4,data_sjw=1" #250kbp
#bitrate = b"f_clock_mhz=80,nom_brp=4,nom_tseg1=15,nom_tseg2=4,nom_sjw=1,data_brp=2,data_tseg1=15,data_tseg2=4,data_sjw=1" #1mbp
status = pcan.CAN_InitializeFD(PCAN_USBBUS1, bitrate)
 
def send_data():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data = [ 0x10, 0x00, 0x00,0x00, 0x01, 0x2F, 0x59, 0x02, 0xFF, 0x21, 0x35, 0x64, 0x50, 0x20, 0xC9, 0x00,               
        0x50, 0x04, 0x03, 0x00, 0x50, 0x04, 0x09, 0x00, 0x50, 0x04, 0x5B, 0x00,
        0x50, 0x22, 0x69, 0x00, 0x50, 0x06, 0x27, 0x00, 0x50, 0x32, 0x60, 0x00,
        0x50, 0x32, 0x62, 0x00, 0x50, 0x00, 0x87, 0x00, 0x50, 0x08, 0x06, 0x00,
        0x50, 0x04, 0x80, 0x00, 0xAF, 0x22, 0x6A, 0x00, 0x50, 0x32, 0x63, 0x00]
 
      data2= [0x21,0x50, 0x32, 0x64, 0x00, 0x50, 0x32, 0x65, 0x00, 0x50, 0x06, 0x50, 0x00, 0xAF, 0x01, 0x93, 0x00, 0xAF, 0x13, 0x00, 0x00,
     0x50, 0x13, 0x01, 0x00, 0x50, 0x13, 0x02, 0x00, 0x50, 0x13, 0x03, 0x00, 0x50, 0x06, 0x15, 0x00,
     0xAF, 0x16, 0x15, 0x00, 0x50, 0x06, 0x17, 0x00, 0x50, 0x06, 0x16, 0x00, 0x50, 0x06, 0x55, 0x00,
     0x50, 0x32, 0x67, 0x00, 0x50, 0x32, 0x68, 0x00, 0x50, 0x32, 0x69 ]
  
      data3=  [0x22,0x00, 0x50,0x05, 0x01 ,0x00 ,0x50, 0x02, 0x17, 0x00, 0x50, 0x01, 0x18, 0x00, 0xAF, 0x04, 0x87, 0x00, 0x50, 0x04, 0x89, 0x00,
      0x50, 0x02, 0x19, 0x00, 0x50, 0x03, 0x80, 0x00, 0xAF, 0x21, 0x22, 0x00, 0xAF, 0x21, 0x27, 0x00,
      0xAF, 0x21, 0x35, 0x00, 0x50, 0x02, 0x01, 0x00, 0x50, 0x06, 0x2D, 0x00, 0x50, 0x02, 0x61, 0x00,
      0x50, 0x02, 0x62, 0x00, 0x50, 0x06, 0x1A, 0x00, 0x50, 0x32 ] 
      
      data4= [0x23,0x0D, 0x00,0x50, 0x32, 0x0E, 0x00,0x50, 0x06, 0x2F, 0x00, 0x50, 0x32, 0x6A, 0x00, 0x50, 0x32, 0x6B, 0x00, 0x50, 0x03, 0x36, 0x00,
     0x50, 0x03, 0x35, 0x00, 0x50, 0x13, 0x39, 0x00, 0x50, 0x06, 0x8B, 0x00, 0x50, 0x06, 0x01, 0x00,
     0x50, 0x32, 0x6F, 0x00, 0x50, 0x32, 0x70, 0x00, 0xAF, 0x32, 0x71, 0x00, 0x50, 0x32, 0x72, 0x00,
     0x50, 0x32, 0x73, 0x00, 0x50, 0x32, 0x74, 0x00, 0x50]
      
      data5= [0x24,0x32, 0x75, 0x00, 0x50,0x32, 0x76, 0x00,0x50, 0x32, 0x77, 0x00, 0x50, 0x32, 0x78, 0x00, 0x50, 0x06, 0x0D, 0x00, 0x50, 0x06, 0x1C, 0x00,
     0x50, 0x32, 0x79, 0x00, 0x50, 0x32, 0x01, 0x00, 0x50, 0x32, 0x7A, 0x00, 0x50, 0x32, 0x08, 0x00,
     0x50, 0x32, 0x09, 0x00, 0x50, 0x01, 0x91, 0x00, 0x50, 0x32, 0x7B, 0x00, 0x50, 0x06, 0x06, 0x00,
     0x2F]


      msg.DATA = (c_ubyte * 64)(*data + [0x00] * (64 - len(data)))
    #for i in range(msg.DLC):
    #    msg.DATA[i] = i + 1
    # Send the message
      time.sleep(delaytime)
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg))
      time.sleep(delaytime)
    #   msg.DATA = (c_ubyte * 64)(*data2 + [0x00] * (64 - len(data2)))
    #   result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
    #   msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
    #   result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg))
    #   msg.DATA = (c_ubyte * 64)(*data4 + [0x00] * (64 - len(data4)))
    #   result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg))
    #   msg.DATA = (c_ubyte * 64)(*data5 + [0x00] * (64 - len(data5)))
    #   result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg))

      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)


def send_data_2():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data = [ 0x10, 0x00, 0x00,0x00, 0x01, 0x2F, 0x59, 0x02, 0xFF, 0x05, 0x04, 0x00, 0x50, 0x04, 0x04, 0x00,               
        0x50, 0x04, 0x03, 0x00, 0x50, 0x04, 0x09, 0x00, 0x50, 0x04, 0x5B, 0x00,
        0x50, 0x22, 0x69, 0x00, 0x50, 0x06, 0x27, 0x00, 0x50, 0x32, 0x60, 0x00,
        0x50, 0x32, 0x62, 0x00, 0x50, 0x00, 0x87, 0x00, 0x50, 0x08, 0x06, 0x00,
        0x50, 0x04, 0x80, 0x00, 0xAF, 0x22, 0x6A, 0x00, 0x50, 0x32, 0x63, 0x00]
 
      data2= [0x21,0x50, 0x32, 0x64, 0x00, 0x50, 0x32, 0x65, 0x00, 0x50, 0x06, 0x50, 0x00, 0xAF, 0x01, 0x93, 0x00, 0xAF, 0x13, 0x00, 0x00,
     0x50, 0x13, 0x01, 0x00, 0x50, 0x13, 0x02, 0x00, 0x50, 0x13, 0x03, 0x00, 0x50, 0x06, 0x15, 0x00,
     0xAF, 0x16, 0x15, 0x00, 0x50, 0x06, 0x17, 0x00, 0x50, 0x06, 0x16, 0x00, 0x50, 0x06, 0x55, 0x00,
     0x50, 0x32, 0x67, 0x00, 0x50, 0x32, 0x68, 0x00, 0x50, 0x32, 0x69 ]
  
      data3=  [0x22,0x00, 0x50,0x05, 0x01 ,0x00 ,0x50, 0x02, 0x17, 0x00, 0x50, 0x01, 0x18, 0x00, 0xAF, 0x04, 0x87, 0x00, 0x50, 0x04, 0x89, 0x00,
      0x50, 0x02, 0x19, 0x00, 0x50, 0x03, 0x80, 0x00, 0xAF, 0x21, 0x22, 0x00, 0xAF, 0x21, 0x27, 0x00,
      0xAF, 0x21, 0x35, 0x00, 0x50, 0x02, 0x01, 0x00, 0x50, 0x06, 0x2D, 0x00, 0x50, 0x02, 0x61, 0x00,
      0x50, 0x02, 0x62, 0x00, 0x50, 0x06, 0x1A, 0x00, 0x50, 0x32 ] 
      
      data4= [0x23,0x0D, 0x00,0x50, 0x32, 0x0E, 0x00,0x50, 0x06, 0x2F, 0x00, 0x50, 0x32, 0x6A, 0x00, 0x50, 0x32, 0x6B, 0x00, 0x50, 0x03, 0x36, 0x00,
     0x50, 0x03, 0x35, 0x00, 0x50, 0x13, 0x39, 0x00, 0x50, 0x06, 0x8B, 0x00, 0x50, 0x06, 0x01, 0x00,
     0x50, 0x32, 0x6F, 0x00, 0x50, 0x32, 0x70, 0x00, 0xAF, 0x32, 0x71, 0x00, 0x50, 0x32, 0x72, 0x00,
     0x50, 0x32, 0x73, 0x00, 0x50, 0x32, 0x74, 0x00, 0x50]
      
      data5= [0x24,0x32, 0x75, 0x00, 0x50,0x32, 0x76, 0x00,0x50, 0x32, 0x77, 0x00, 0x50, 0x32, 0x78, 0x00, 0x50, 0x06, 0x0D, 0x00, 0x50, 0x06, 0x1C, 0x00,
     0x50, 0x32, 0x79, 0x00, 0x50, 0x32, 0x01, 0x00, 0x50, 0x32, 0x7A, 0x00, 0x50, 0x32, 0x08, 0x00,
     0x50, 0x32, 0x09, 0x00, 0x50, 0x01, 0x91, 0x00, 0x50, 0x32, 0x7B, 0x00, 0x50, 0x06, 0x06, 0x00,
     0x2F]




    #  msg.DATA = (c_ubyte * 64)(*data + [0x00] * (64 - len(data)))
    #for i in range(msg.DLC):
    #    msg.DATA[i] = i + 1
 
    # Send the message
    #  time.sleep(0.5)
    #  result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg))
      time.sleep(delaytime)
      msg.DATA = (c_ubyte * 64)(*data2 + [0x00] * (64 - len(data2)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(delaytime)
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg))
      time.sleep(delaytime)
      msg.DATA = (c_ubyte * 64)(*data4 + [0x00] * (64 - len(data4)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg))
      time.sleep(delaytime)
      msg.DATA = (c_ubyte * 64)(*data5 + [0x00] * (64 - len(data5)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg))

      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)


def send_data_3():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [ 0x30, 0x00, 0x01,0x00, 0x00, 0x00, 0x00, 0x00]         

      data4 = [0x02 ,0x76 ,0x01,0xAA ,0xAA ,0xAA ,0xAA ,0xAA]    
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.9)
      #msg.DATA = (c_ubyte * 64)(*data4 + [0x00] * (64 - len(data4)))
      #result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
  
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)


def send_data_4():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [ 0x00, 0x02, 0x50,0x03, 0x00, 0x00, 0x00, 0x00]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.3)

      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)

def send_data_5():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [ 0x00, 0x02, 0x50,0x02, 0x00, 0x00, 0x00, 0x00]         
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.4)

      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)

def send_data_6():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [0x00, 0x0A, 0x67, 0x01, 0xAE, 0x48, 0xD9, 0xA3, 0x97, 0xA2, 0x3A, 0xF3]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.1)
      
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)

def send_data_7():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [ 0x00,0x02, 0x67, 0x02, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.1)   

      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)

DLC_TO_LEN_FD = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 12,
    10: 16,
    11: 20,
    12: 24,
    13: 32,
    14: 48,
    15: 64
}

def send_data_8():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [0x00,0x05, 0x71, 0x01, 0xFF, 0x00, 0x00, 0xAA, 0xAA]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.1)
      
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)


def send_data_9():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [0x00,0x04, 0x74, 0x20, 0x0F, 0xFF, 0xAA, 0xAA]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.2)
      
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)


def send_data_10():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
      data3 = [ 0x30, 0x00, 0x01,0x00, 0x00, 0x00, 0x00, 0x00]   
      data4 = [0x00,0x02, 0x76, 0x01, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.8)
      msg.DATA = (c_ubyte * 64)(*data4 + [0x00] * (64 - len(data4)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(0.03)


def send_data_11():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [0x00,0x01, 0x77, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.1)
      
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)

def send_data_12():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [0x00,0x05, 0x71, 0x01, 0x02, 0x02, 0x00, 0xAA, 0xAA]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.1)
      
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)

def send_data_13():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0
        
      data3 = [0x00,0x02, 0x51, 0x01, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]         
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.08)
      
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)

def send_data_14():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0

      if livepara==1:  
       data3 = [0x00,0x05, 0x62, 0x10, 0x0D, 0x02, 0x62, 0xAA, 0xAA]       
      else:
       data3 = [0x00,0x05, 0x62, 0xfe, 0x92, 0x00, 0x62, 0xAA, 0xAA] 
         
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.08)
      
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)

def send_data_15():
    def get_error_text(err):
     buffer = ctypes.create_string_buffer(256)
     pcan.CAN_GetErrorText(err, 0x09, buffer)  # LANG_ENGLISH
     return buffer.value.decode()
 
    if status != PCAN_ERROR_OK:
     print("Initialization failed.")
     print("Error:", get_error_text(status))
    else:
      print("PCAN Initialized.")
      time.sleep(delaytime)
    # Create message
      msg = TPCANMsgFD()
      msg.ID = sendID
      if sendID == 0x7E8:
        msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS 
      else:
           msg.MSGTYPE = PCAN_MESSAGE_FD | PCAN_MESSAGE_BRS | PCAN_MESSAGE_EXTENDED
      msg.DLC = 0x0f
      msg.BRS = 1  # Bit Rate Switching
      msg.ESI = 0

      data3 = [0x00,0x02, 0x7e, 0x00, 0x00, 0x00, 0x00, 0xAA, 0xAA] 
        
      msg.DATA = (c_ubyte * 64)(*data3 + [0x00] * (64 - len(data3)))
      result = pcan.CAN_WriteFD(PCAN_USBBUS1, byref(msg)) 
      time.sleep(0.08)
      
      print(msg)
      if result == PCAN_ERROR_OK:
         print("Message sent successfully.")
      else:
         print(f"Failed to send message. Error: {result}")
      time.sleep(delaytime)








msg = TPCANMsgFD()
timestamp = TPCANTimestampFD()
while True:
         recivedata.clear()
         result = pcan.CAN_ReadFD(PCAN_USBBUS1, byref(msg), byref(timestamp))
         if result == PCAN_ERROR_OK and msg.ID==recivedID:
             print("\n--- CAN FD Message Received ---")
           #  print(f"ID     : 0x{msg.ID:X}")
           #  print(f"Length : {msg.DLC} bytes")
           #  print(f"Type   : {'FD' if msg.MSGTYPE & PCAN_MESSAGE_FD else 'Standard'}")
           #  print(f"BRS    : {msg.BRS}")
           #  print(f"ESI    : {msg.ESI}")
           #  print(f"Data   : {[msg.DATA[i] for i in range(msg.DLC)]}")
             actual_length = DLC_TO_LEN_FD.get(msg.DLC, 0)
           #  print(f"Data   : {[msg.DATA[i] for i in range(actual_length)]}")
             for i in range(actual_length):
              recivedata.append(msg.DATA[i])
            # print("recivedata ",recivedata)
             if recivedata[0]==16 and recivedata[7]==17 and recivedata[8]==34 and recivedata[9]==51:
                send_data_3()
             if recivedata[0]==0 and recivedata[1]==3 and recivedata[2]==25:
                print("got 19 02 ff")
                send_data()
             if recivedata[0]==48 and recivedata[1]==0 and recivedata[2]==1 : 
                 print("got 30 00 01")
                 send_data_2()
             if recivedata[1]==2 and recivedata[2]==16 and recivedata[3]==3  : 
                 print("1003")
                 send_data_4()   
          #   if recivedata[0]==16 and recivedata[7]==18 and recivedata[8]==17 and recivedata[9]==18 : 
          #      print("got 30 00 01")
          #      send_data_3()  
             if recivedata[1]==2 and recivedata[2]==16 and recivedata[3]==2  : 
                 print("got 1002")
                 send_data_5()
             if recivedata[1]==2 and recivedata[2]==39 and recivedata[3]==1 : 
                 print("got 2701")
                 send_data_6()   
             if recivedata[1]==10 and recivedata[2]==39 and recivedata[3]==2  : 
                 print(" * * * got 2702")
                 send_data_7()    
             if recivedata[1]==6 and recivedata[2]==49 and recivedata[3]==1 and recivedata[4]==255: 
                 print("got 3101")
                 send_data_8()  
             if recivedata[1]==11 and recivedata[2]==52 and recivedata[4]==68: 
                 print("got 3401")
                 send_data_9() 
             if recivedata[0]==16 and recivedata[6]==54: 
                 send_data_10()  
             if recivedata[0]==0 and recivedata[1]==1 and recivedata[2]==55: 
                 print("got 3701")
                 send_data_11()    
             if recivedata[0]==0 and recivedata[1]==6 and recivedata[2]==49 and recivedata[3]==1 and recivedata[4]==2: 
                 print("got 31010202")
                 send_data_12()      
             if recivedata[1]==2 and recivedata[2]==17 and recivedata[3]==1: 
                 print("got 1101")
                 send_data_13()   
             if recivedata[2]==34 and recivedata[3]==16 and recivedata[4]==13: 
                 print("got 100D battery vtg")
                 send_data_14()  
                 livepara=0    
             if recivedata[2]==34 and recivedata[3]==254 and recivedata[4]==146: 
                 print("got fe92 exhaust")
                 livepara=1
                 send_data_14()  
             if recivedata[0]==0 and recivedata[1]==2 and recivedata[2]==62 and recivedata[3]==0: 
                 print("got 3e00")
                 send_data_15()   
                           

            