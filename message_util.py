import json
import struct


# client version uses socket instead connection
def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = json.dumps(msg, ensure_ascii=False).encode('utf-8')
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recv_all(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    coded_data = recv_all(sock, msglen)
    return json.loads(coded_data, encoding='utf-8')


def recv_all(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
