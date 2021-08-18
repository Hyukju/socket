import socket
import os


# 접속할 서버 주소입니다. 여기에서는 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다. 
HOST = '127.0.0.1'
# 클라이언트 접속을 대기하는 포트 번호입니다.   
PORT = 9999        

IMAGE_DIR = 'C:\\Users\\hyukj\\Desktop\\projects\\dataset\\20210730_pill20_100_ro20_45_pill20\\yolov4_20pills_1000'

# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 포트 사용중이라 연결할 수 없다는 
# WinError 10048 에러 해결를 위해 필요합니다. 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다. 
# PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.  
server_socket.bind((HOST, PORT))

# 서버가 클라이언트의 접속을 허용하도록 합니다. 
server_socket.listen()


file_list = os.listdir(IMAGE_DIR)


for filename in file_list:
    
    # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다. 
    client_socket, addr = server_socket.accept()

    # 접속한 클라이언트의 주소입니다.
    print('Connected by', addr)

    print('filename: ', filename)
    # 메시지를 전송합니다. 
    client_socket.sendall(filename.encode('utf-8'))
    
    data_transferred = 0
    print("파일 %s 전송 시작" %filename)
    with open(os.path.join(IMAGE_DIR, filename), 'rb') as f:
        try:
            data = f.read(1024) #1024바이트 읽는다
            while data: #데이터가 없을 때까지
                data_transferred += client_socket.send(data) #1024바이트 보내고 크기 저장
                data = f.read(1024) #1024바이트 읽음
            
        except Exception as ex:
            print(ex)
    # 소켓을 닫습니다.
    client_socket.close()
    print("전송완료 %s, 전송량 %d" %(filename, data_transferred))


server_socket.close()