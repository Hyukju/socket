import socket
import argparse
import buffer
import os 
def run_client(host, port, server_image_dir, save_dir):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with s:
        sbuf = buffer.Buffer(s)
        
        sbuf.put_utf8(server_image_dir)

        count = 0
        while True:
            received = sbuf.get_utf8()

            if received == 'END':
                print()
                break
            elif 'Error' in received:
                print(received)
                break
            else:
                count += 1
                file_name = received
                file_size = int(sbuf.get_utf8())
                print(f'{count}. {file_name}, file size: ', file_size )

                with open(os.path.join(save_dir,file_name), 'wb') as f:
                    remaining = file_size
                    while remaining:
                        chunk_size = 4096 if remaining >= 4096 else remaining
                        chunk = sbuf.get_bytes(chunk_size)
                        if not chunk: break
                        f.write(chunk)
                        remaining -= len(chunk)
                    if remaining:
                        print('File incomplete.  Missing',remaining,'bytes.')
                    else:
                        print(f'File received successfully.')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Echo client -p port -i host -s sever image directory -d save directory")
    parser.add_argument('-i', help="host_ip", required=True)
    parser.add_argument('-p', help="port_number", required=True)    
    parser.add_argument('-s', help="server image directory", required=True)
    parser.add_argument('-d', help="save directory", required=True)

    args = parser.parse_args()
    run_client(host=args.i, port=int(args.p), server_image_dir=args.s, save_dir=args.d)