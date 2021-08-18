import socket
import os

# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '127.0.0.1'  
# 서버에서 지정해 놓은 포트 번호입니다. 
PORT = 9999       



while True:        
    
    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    client_socket.connect((HOST, PORT))
    
    # 메시지를 수신합니다. 
    filename = client_socket.recv(1024).decode('utf-8')
    print('filename:', filename)
    if not filename:
        break
    data = client_socket.recv(1024)
    data_transferred = 0
    with open(filename, 'wb') as f: #현재dir에 filename으로 파일을 받는다
        try:
            while data: #데이터가 있을 때까지
                f.write(data) #1024바이트 쓴다
                data_transferred += len(data)
                data = client_socket.recv(1024) #1024바이트를 받아 온다
        except Exception as ex:
            print(ex)
        print('파일 %s 받기 완료. 전송량 %d' %(filename, data_transferred))

        
  
# 소켓을 닫습니다.
client_socket.close()

    
