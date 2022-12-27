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
    image = Image.open(filename)
    im_size = image.width * image.height
    emb_len = len(emb_data)

    if im_size >= emb_len * 8:
        data = get_rand_bytes(key, math.floor(im_size / 8))
        step = (len(data) - emb_len) / emb_len

        for i in range(emb_len):
            pos = int(i * step)
            data[pos] = ord(emb_data[i])
            binary_enc_data = ''.join(byte2bin(b) for b in encrypt(data, key))
            for w in range(image.width):
                for h in range(image.height):
                    pixel = image.getpixel((w, h))
                    image.putpixel((w, h), (bin2byte(byte2bin(pixel[0])[:-1] + binary_enc_data[h * image.width + w]),
                                            *pixel[1:]))

        image.save("emb" + filename, format="png")
        return data


def decode_data(filename, key):
    image = Image.open(filename)
    im_size = image.width * image.height
    binary_enc_data = ''

    for h in range(image.height):
        for w in range(image.width):
            pixel = image.getpixel((w, h))
            binary_enc_data += byte2bin(pixel[0])[-1:]
            enc_data = bytearray(math.floor(im_size / 8))
            for i in range(len(enc_data)):
                enc_data[i] = bin2byte(binary_enc_data[i * 8:(i + 1) * 8])
                dec_data = decrypt(enc_data, key)
                emb_len = dec_data[0]
                dec_text = ''
                step = math.floor((len(dec_data) - 1) / emb_len)
                for i in range(emb_len):
                    pos = int(i * step) + 1
                    dec_text += chr(dec_data[pos])
                return dec_text


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
    dec_data = decode_data("SOC_forum.PNG", "SOLAR_SECURITY")
    print("Flag: ", dec_data)
