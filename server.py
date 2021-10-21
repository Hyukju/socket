import socket
import os
import argparse
import buffer

def run_server(host, port):
    s = socket.socket()
    s.bind((host, port))
    s.listen(10)
    print("Waiting for a connection.....")
    print(f"Running on {host}:{port}")
    
    while True:
        try:
            conn, addr = s.accept()
            print("Got a connection from ", addr)
            connbuf = buffer.Buffer(conn)
           
            image_dir = connbuf.get_utf8()

            if not os.path.exists(image_dir):
                msg = f"Error:: No '{image_dir}' directory in server"
                print(msg)
                connbuf.put_utf8(msg)
            else:
                file_list = os.listdir(image_dir)

                if len(file_list) == 0:
                    msg = f"Error:: No image files in '{image_dir}'"
                    print(msg)
                    connbuf.put_utf8(msg)

                print(f"Searching image files in 'image_dir'")
            
                for count, file_name in enumerate(file_list):
                    
                    connbuf.put_utf8(file_name)

                    file_size = os.path.getsize(os.path.join(image_dir,file_name))
                    connbuf.put_utf8(str(file_size))

                    with open(os.path.join(image_dir, file_name), 'rb') as f:
                        connbuf.put_bytes(f.read())
                    print(f'{count+1}. File Sent:: ', os.path.join(image_dir, file_name))
                
                connbuf.put_utf8('END')
            conn.close()
            print('Clinet ', addr, 'connection closed.')            
            print(f"Server running on {host}:{port}")
        except Exception as e:
            print(e)
            
if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Echo server -p port -i host")
    parser.add_argument('-i', help="host_ip", required=False, default=socket.gethostbyname(socket.gethostname()))
    parser.add_argument('-p', help="port_number", required=False, default=5000)    

    args = parser.parse_args()
    run_server(host=args.i, port=int(args.p))
