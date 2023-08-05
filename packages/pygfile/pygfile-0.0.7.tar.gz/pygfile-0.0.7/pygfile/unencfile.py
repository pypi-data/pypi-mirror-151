import base64
import os
import pickle
import struct
import zlib
import binascii

# 解密
import easygui as eg


class MaliciousCodeError(Exception):
    pass


def main():
    n = eg.enterbox("请输入加密的数据， b' 和 ' 也要带")
    if n != "" or n != None:
        if (n[0] == "b" and n[1] == "'" and n[-1] == "'") or (n[0] == "b" and n[1] == '"' and n[-1] == '"'):
            n = eval(n)  # 如果直接eval，有可能是恶意代码
        else:
            raise MaliciousCodeError()
        try:
            nums = int(eg.enterbox("请输入加密次数"))
        except Exception:
            return
        # 解密开始
        data = n.decode().lstrip("10").rstrip("10")
        data = binascii.unhexlify(data)
        data = zlib.decompress(data)
        for x in range(nums):
            data = pickle.loads(data)

        file_info = data[0]
        file_info = struct.unpack("128sl", file_info)
        print("文件名称："+file_info[0].decode("utf-16"))
        print("文件大小："+str(file_info[1]))
        print()

        s = data[1]
        s = base64.b85decode(s)
        print("文件内容：\n"+s.decode())

        loginname = data[2]
        loginname = base64.a85decode(loginname).decode()
        print("文件创建者："+loginname)

        ip = data[3]
        ip = base64.b16decode(ip).decode()
        print("创建者IP（当时）："+ip)

        result = eg.buttonbox("是否保存文件？（克隆文件）", choices=("保存", "不保存", "保存并打开"))
        if result == "保存":
            d = eg.diropenbox("请选择路径")
            if d != None:
                os.chdir(d)
                with open(file_info[0].decode().strip("\x00"), "w") as f:
                    f.write(s.decode())
                eg.msgbox(title="提示", msg="OK")
        elif result == "保存并打开":
            d = eg.diropenbox("请选择路径")
            if d != None:
                os.chdir(d)
                with open(file_info[0].decode().strip("\x00"), "w") as f:
                    f.write(s.decode())
                os.startfile(file_info[0].decode().strip("\x00"))
                eg.msgbox(title="提示", msg="OK")


if __name__ == "__main__":
    main()
