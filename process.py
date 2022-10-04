from PIL import Image, ImageDraw


def encrypt_to_bin(num):
    res = []
    if num != 0:
        while num > 1:
            res.append(str(num % 2))
            num = num // 2
        res.append('1')
    else:
        res = ['0']
    for i in range(8 - len(res)):
        res.append('0')
    res = res[::-1]
    return res


def encrypt_to_dec(num):
    res = 0
    num = num[::-1]
    for i in range(len(num)):
        res += int(num[i]) * (2**i)
    return res


def change_pixel(r, g, b, bins):
    binr, bing, binb = encrypt_to_bin(r), encrypt_to_bin(g), encrypt_to_bin(b)
    binr[-1] = bins[5]
    bing[-1] = bins[6]
    binb[-1] = bins[7]
    binr[-2] = bins[2]
    bing[-2] = bins[3]
    binb[-2] = bins[4]
    binr[-3] = bins[0]
    bing[-3] = bins[1]
    r2, g2, b2 = encrypt_to_dec(binr), encrypt_to_dec(
        bing), encrypt_to_dec(binb)
    return r2, g2, b2


def change_to_zero(r, g, b):
    binr, bing, binb = encrypt_to_bin(r), encrypt_to_bin(g), encrypt_to_bin(b)
    binr[-1] = '0'
    bing[-1] = '0'
    binb[-1] = '0'
    binr[-2] = '0'
    bing[-2] = '0'
    binb[-2] = '0'
    binr[-3] = '0'
    bing[-3] = '0'
    binb[-3] = '0'
    r2, g2, b2 = encrypt_to_dec(binr), encrypt_to_dec(
        bing), encrypt_to_dec(binb)
    return r2, g2, b2


def decode(r, g, b):
    binr, bing, binb = encrypt_to_bin(r), encrypt_to_bin(g), encrypt_to_bin(b)
    res = [binr[-3], bing[-3], binr[-2], bing[-2],
           binb[-2], binr[-1], bing[-1], binb[-1]]
    return res


def in_pic(text, im1, im2):
    text = text
    length = len(text)

    bins = []
    for i in text:
        res = encrypt_to_bin(ord(i))
        res = res[::-1]
        for j in range(16 - len(res)):
            res.append('0')
        res = res[::-1]
        for j in res:
            bins.append(j)
    sum_length = len(bins)
    i = 0
    while 2**i < sum_length:
        i += 1
    for j in range(2**i - sum_length):
        bins.append('0')
    sum_length = 2**i

    image = Image.open(im1)
    w, h = image.size
    c = 0
    for i in range(w):
        for j in range(h):
            if c > sum_length:
                break
            r, g, b = image.getpixel((i, j))
            r, g, b = change_to_zero(r, g, b)
            image.putpixel((i, j), (r, g, b))
            c += 1

    c = 0
    for i in range(w):
        for j in range(h):
            if c * 8 >= sum_length:
                break
            r, g, b = image.getpixel((i, j))
            r, g, b = change_pixel(r, g, b, bins[c * 8: (c + 1) * 8])

            image.putpixel((i, j), (r, g, b))
            c += 1
    r1, g1, b1 = image.getpixel((w - 1, h - 1))
    r2, g2, b2 = image.getpixel((w - 2, h - 2))
    lennum = encrypt_to_bin(len(text))
    lennum = lennum[::-1]
    for i in range(16 - len(lennum)):
        lennum.append('0')
    lennum = lennum[::-1]
    r2, g2, b2 = change_pixel(r2, g2, b2, lennum[:8])
    r1, g1, b1 = change_pixel(r1, g1, b1, lennum[8:])
    image.putpixel((w - 1, h - 1), (r1, g1, b1))
    image.putpixel((w - 2, h - 2), (r2, g2, b2))
    image.save(im2)


def out_pic(im1):
    image = Image.open(im1)
    w, h = image.size
    r1, g1, b1 = image.getpixel((w - 1, h - 1))
    r2, g2, b2 = image.getpixel((w - 2, h - 2))
    lennum = ''
    for i in decode(r2, g2, b2):
        lennum += i
    for i in decode(r1, g1, b1):
        lennum += i
    lennum = int(encrypt_to_dec(lennum))
    bins = []
    for i in range(w):
        for j in range(h):
            r, g, b = image.getpixel((i, j))
            for q in decode(r, g, b):
                bins.append(q)
    text = ''
    nums = ''
    allnums = []
    for i in range(lennum):
        for j in (bins[i * 16: (i + 1) * 16]):
            nums += j
        text += chr(encrypt_to_dec(nums))
        allnums.append(encrypt_to_dec(nums))
        nums = ''
    return text
