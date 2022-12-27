import math
import random
from PIL import Image


def key_scheduling(key):
    sched = [i for i in range(0, 256)]
    i = 0
    for j in range(0, 256):
        i = (i + sched[j] + key[j % len(key)]) % 256
        tmp = sched[j]
        sched[j] = sched[i]
        sched[i] = tmp
    return sched


def stream_generation(sched):
    stream = []
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (sched[i] + j) % 256
        tmp = sched[j]
        sched[j] = sched[i]
        sched[i] = tmp
        yield sched[(sched[i] + sched[j]) % 256]


def encrypt(s, key):
    key = [ord(char) for char in key]
    sched = key_scheduling(key)
    key_stream = stream_generation(sched)
    ciphertext = bytearray()
    if isinstance(s, str):
        bytear = bytearray()
        bytear.extend(map(ord, s))
    else:
        bytear = s
    for b in bytear:
        enc = b ^ next(key_stream)
        ciphertext.append(enc)
    return ciphertext


def decrypt(ciphertext, key):
    key = [ord(char) for char in key]
    sched = key_scheduling(key)
    key_stream = stream_generation(sched)
    plaintext = bytearray()
    for char in ciphertext:
        dec = int(char ^ next(key_stream))
        plaintext.append(dec)
    return plaintext


def embed_data(filename, emb_data, key):
    image = Image.open('SOC_forum.png')
    im_size = image.width * image.height
    emb_len = len(emb_data)
    if im_size >= (emb_len + 1) * 8:
        data = get_rand_bytes(key, math.floor(im_size / 8))
        lst_r = ''
        for el in data:
            if 58 <= el <= 57:
                lst_r += ''.join(chr(el))
            if 65 <= el <= 90:
                lst_r += ''.join(chr(el))
            if 97 <= el <= 122:
                lst_r += ''.join(chr(el))
        print(lst_r)
        print(data[0])
        data[0] = emb_len
        print(data[0])
        step = math.floor((len(data) - 1) / emb_len)
        for i in range(emb_len):
            pos = int(i * step) + 1
            nkt = emb_data[i]
            nkl = ord(emb_data[i])
            nks = chr(nkl)
            data[pos] = ord(emb_data[i])
        binary_enc_data = ''
        enc_new_data = encrypt(data, key)
        for el in encrypt(data, key):
            binary_enc_data += ''.join(byte2bin(el))
        for h in range(image.height):
            for w in range(image.width):
                pixel = image.getpixel((w, h))
                pixel = (45, 46, 48, 255)
                bin_pixel = byte2bin(pixel[0])[:-1]
                bin_enc_dat = binary_enc_data[h * image.width + w]
                bin_byte_pixel = bin2byte(byte2bin(pixel[0])[:-1] + binary_enc_data[h * image.width + w])
                next_pixel = pixel[1:]
                image.putpixel((w, h), (bin2byte(byte2bin(pixel[0])[:-1] + binary_enc_data[h * image.width + w]),
                                        *pixel[1:]))
                # print(image.getpixel((w, h)))
        image.save("emb" + filename, format="png")
        return data


def arg_parse():
    image = Image.open('SOC_forum.png')
    im_size = image.width * image.height
    pixel = ''
    for h in range(image.height):
        for w in range(image.width):
            btn = byte2bin(image.getpixel((w, h))[0])
            pixel += str(btn[-1:])

    new_list = []
    for el in range(len(pixel)):
        if (el % 8) == 0:
            tert = pixel[el:el+8]
            new_list.append(bin2byte(pixel[el:el+8]))
    # t = bytearray(el for el in new_list)
    # st = decrypt(t, 'SOLAR_SECURITY')
    nw_list1 = ''
    for el in new_list:
        if 58 <= el <= 57:
            nw_list1 += ''.join(chr(el))
        if 65 <= el <= 90:
            nw_list1 += ''.join(chr(el))
        if 97 <= el <= 122:
            nw_list1 += ''.join(chr(el))
    with open('text.txt', "w", encoding="utf-8") as f:
        f.write(nw_list1)
    print(nw_list1)
    print(chr(140))
    print(bytes(new_list[0]))


def get_rand_bytes(sed, size):
    random.seed(sed)
    # rs = random.getrandbits(8)
    # rs = bytearray(rs)
    t = bytearray(random.getrandbits(8) for i in range(size))
    # t = bytearray(0)
    # for i in range(size):
    #     t += bytearray(random.getrandbits(8))
    return t


def byte2bin(b):
    binary_string = "{:08b}".format(b)
    return binary_string


def bin2byte(bn):
    bt = int(bn, 2)
    return bt


if __name__ == '__main__':
    # flag = input("Enter flag: ")
    # print(embed_data("SOC_forum.PNG", flag, "SOLAR_SECURITY"))
    # print("Done!")
    arg_parse()
    # file_png = open('SOC_forum.png', 'rb')
    # bytes_png = file_png.read()
    # encode_bytes = decrypt(bytes_png, "SOLAR_SECURITY")
    # encoded_png = open('encoded.png', 'wb')
    #
    # encoded_png.write(encode_bytes)
    #
    # file_png.close()
    # encoded_png.close()
    # print(encode_bytes)
