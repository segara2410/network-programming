import argparse, random, socket, zen_utils
import sys, random, multiprocessing, ctypes

HOST = "127.0.0.1"
PORT = 1060

final_value = multiprocessing.Value(ctypes.c_int, 0)

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def worker(address, i, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    for ii in data:
        ii = ii.strip()
        len_msg = b"%03d" % (len(ii),) 
        msg = len_msg + bytes(ii, encoding="ascii")
        sock.sendall(msg)
        len_msg = recvall(sock, 3)
        message = recvall(sock, int(len_msg))
        message = str(message, encoding="ascii")
    print(f'thread {i} result:', message)
    final_value.value += int(message)
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='multi-threaded client')
    parser.add_argument('-j', metavar='jobs', type=int, default=4,
                    help='jobs (default 4)')
    args = parser.parse_args()
    NUMJOBS = args.j

    f = open("input.txt")
    data = f.readlines()
    f.close()

    address = (HOST, PORT)
    jobs = []
    for i in range(NUMJOBS):
        p = multiprocessing.Process(target=worker, args=(address, i, data))
        jobs.append(p)
    print("JOBS:", len(jobs))

    for p in jobs:
        p.start()

    for p in jobs:
        p.join()
    
    print('\nfinal value: ', final_value.value)
    print('final value /', NUMJOBS, ': ', final_value.value // NUMJOBS)

# vim:sw=4:ai
