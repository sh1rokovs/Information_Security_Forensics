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
        data[0] = emb_len
        step = math.floor((len(data) - 1) / emb_len)
        for i in range(emb_len):
            pos = int(i * step) + 1
            data[pos] = ord(emb_data[i])
        # binary_enc_data = decrypt(data, key)
        # print(binary_enc_data)
        binary_enc_data = ''.join(byte2bin(b) for b in encrypt(data, key))
        # print(binary_enc_data)
        for h in range(image.height):
            for w in range(image.width):
                pixel = image.getpixel((w, h))
                image.putpixel((w, h), (bin2byte(byte2bin(pixel[0])[:-1] + binary_enc_data[h * image.width + w]),
                                        *pixel[1:]))
                # print(image.getpixel((w, h)))
        image.save("emb" + filename, format="png")
        return data


def get_rand_bytes(sed, size):
    random.seed(sed)
    t = bytearray(random.getrandbits(8) for i in range(size))
    return t


def byte2bin(b):
    binary_string = "{:08b}".format(b)
    return binary_string


def bin2byte(bn):
    bt = int(bn, 2)
    return bt


if __name__ == '__main__':
    flag = input("Enter flag: ")
    print(embed_data("SOC_forum.PNG", flag, "SOLAR_SECURITY"))
    print("Done!")
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
