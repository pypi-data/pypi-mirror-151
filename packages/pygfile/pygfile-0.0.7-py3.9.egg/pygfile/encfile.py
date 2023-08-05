import struct
import pickle
import base64
import binascii
# 所有加密模块
import easygui as eg
import os
import socket
# 压缩数据
import zlib


def main():
    file = eg.fileopenbox("请选择加密的文件")
    if file != None:
        try:
            nums = int(eg.enterbox("请输入加密次数，默认是：1"))
        except Exception:
            return
        r = []
        f = open(file, "r", encoding="utf-8")
        i = f.read()
        f.close()
        i = i.strip()

        name = os.path.basename(file)
        size = len(i)
        enc = struct.pack("128sl", name.encode("utf-16"), size)
        r.append(enc)

        try:
            enc = base64.b85encode(i.encode())
            r.append(enc)
        except Exception:
            enc = base64.b85encode(i)
            r.append(enc)

        loginname = os.getlogin()
        loginname = base64.a85encode(loginname.encode())
        r.append(loginname)

        ip = socket.gethostbyname(socket.gethostname())
        ip = base64.b16encode(ip.encode())
        r.append(ip)

        enc_over = r
        for x in range(nums):
            enc_over = pickle.dumps(enc_over)
        enc_over = zlib.compress(enc_over)
        enc_over = "10" + binascii.hexlify(enc_over).decode() + "10"
        enc_over = enc_over.encode()
        print(enc_over)


if __name__ == "__main__":
    main()
