# coding=utf-8
  
def sendMessage(conn,message):
    conn.send(str(send_data(message)))
 
def parse_data(msg):
    if(len(msg)<1):
         return ''
    code_length = ord(msg[1]) & 127
    print 'code_length:' ,code_length
  
    if code_length == 126:
        masks = msg[4:8]
        data = msg[8:]
    elif code_length == 127:
        masks = msg[10:14]
        data = msg[14:]
    else:
        masks = msg[2:6]
        data = msg[6:]
  
    i = 0
    raw_str = ''
  
    for d in data:
        raw_str += chr(ord(d) ^ ord(masks[i%4]))
        i += 1     
    return raw_str
     
def send_data(raw_str):
    back_str = []
  
    back_str.append('\x81')
    data_length = len(raw_str)
  
    if data_length < 125:
        back_str.append(chr(data_length))
    else:
        back_str.append(chr(126))
        back_str.append(chr(data_length >> 8))
        back_str.append(chr(data_length & 0xFF))
  
    back_str = "".join(back_str) + raw_str
    return back_str
