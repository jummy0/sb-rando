import random
from sb_types import *

table_adapt_decor = (
    0x99, 0x93, 0x94, 0x92,
    0x28, 0x97, 0x96, 0x90,
    0x27, 0x98, 0x95, 0x91,
    0x26, 0x24, 0x25, 0x23,

    0x99, 0x93, 0x94, 0x92,
    0x28, 0x97, 0x96, 0x90,
    0x27, 0x98, 0x95, 0x91,
    0x26, 0x24, 0x25, 0x9c,

    0x4b, 0x4b, 0x9b, 0x9b,
    0x4b, 0x4b, 0x9b, 0x9b,
    0x4a, 0x4a, 0x9a, 0x9a,
    0x4b, 0x4b, 0x9b, 0x9b,

    0x9d, 0x9d, 0x9d, 0x9d,
    0x6d, 0x6d, 0x6d, 0x6d,
    0x6c, 0x6c, 0x6c, 0x6c,
    0x6b, 0x6b, 0x6b, 0x6b,

    0xca, 0xca, 0x8a, 0x8a,
    0xca, 0xca, 0x8a, 0x8a,
    0xca, 0xca, 0x8a, 0x8a,
    0xca, 0xca, 0x8a, 0x8a,

    0x11b, 0x11b, 0x11b, 0x11b,
    0x106, 0x106, 0x106, 0x106,
    0x107, 0x107, 0x107, 0x107,
    0x105, 0x105, 0x105, 0x105,

    0x169, 0x167, 0x168, 0x160,
    0x165, 0x161, 0x163, 0x15d,
    0x166, 0x162, 0x164, 0x15e,
    0x15f, 0x15b, 0x15c, 0x155,

    0x183, 0x183, 0x182, 0x182,
    0x18a, 0x18a, 0x188, 0x188,
    0x18b, 0x18b, 0x189, 0x189,
    0x18d, 0x18d, 0x18c, 0x18c,

    0xfb, 0xfe, 0xfe, 0xfe,
    0xfb, 0x102, 0x104, 0x102,
    0xfb, 0x101, 0x103, 0x101,
    0xfb, 0xfa, 0x100, 0xfa,

    # new defs start here

    # x, D, U, UD,
    # R, DR, UR, UDR,
    # L, DL, UL, UDL,
    # LR, DLR, ULR, UDLR

    # house
    0xc1, 0xc1, 0xba, 0xba,
    0xc4, 0xc4, 0xba, 0xba,
    0xc5, 0xc5, 0xba, 0xba,
    0xc1, 0xc1, 0xba, 0xba
)

len_table_adapt_decor = len(table_adapt_decor)

table_adapt_fromage = (
    -1, 0x109, 0x108, 0x10c,
    0x10b, 0x111, 0x10f, 0x113,
    0x10a, 0x110, 0x10e, 0x112,
    0x10d, 0x115, 0x114, 0x116
)

table_adapt_grotte = (
    -1, 0x11e, 0x11d, 0x121,
    0x120, 0x126, 0x124, 0x128,
    0x11f, 0x125, 0x123, 0x127,
    0x122, 0x12a, 0x129, 0x12b
)


def is_right_border(decor, x, y, dx, dy):
    if not 0 <= x < MAXCELX or not 0 <= y < MAXCELY:
        return True
    icon = decor[(x + dx) * MAXCELY + y + dy]
    if (icon < 0x182 or icon > 0x104) and icon != 400:
        if icon < 250 or icon > 260:
            icon = decor[x * MAXCELY + y]
            if icon == -1:
                return False
            if not icon in (32, 33, 34):
                if icon == 92 or icon == 68:
                    return dy != -1
                if icon == 317:
                    return dy != 1
                if icon in (19, 21, 25, 26, 28):
                    return dy != 1
                if icon == 27:
                    return dx == 0
                if 0x2c < icon < 0x30:
                    return dy != 1
                if icon in (0xf, 0x10, 0x4b, 0x59, 0x5a, 0x9b):
                    b_var = dx == -1
                else:
                    if not icon in (17, 18, 74, 87, 88, 154):
                        if icon in (76, 77, 199, 200):
                            return dx == 0
                        if 109 < icon < 126:
                            return False
                        if icon == 126:
                            return dx == 1
                        if icon == 129:
                            return dx == -1
                        if icon == 132:
                            return dy == 1
                        if icon == 135:
                            return dy == -1
                        if 138 < icon < 144:
                            return False
                        if icon == 138:
                            return dy == -1
                        if icon == 202:
                            return False
                        if icon in (107, 108, 109, 157):
                            return dx != 0
                        if 157 < icon < 0xb6 or icon in [0x135, 0x136] or 0x199 < icon < 0x1a5:
                            return dy == 1
                        if icon == 0xb6 or icon == 0xb7:
                            return dy != 0
                        if 0x14d < icon < 0x151:
                            return dy != 0
                        if 0xf9 < icon < 0x105 or 0x107 < icon < 0x11b or icon in [0x17a, 0x194, 0x19a]:
                            return False
                        if icon < 0x1a5 or icon > 0x1b8:
                            return True
                        return dy != 0
                    b_var = dx == 1
                if not b_var:
                    return dy != 1
        else:
            icon = decor[x * MAXCELY + y]
            if 0xf9 < icon < 0x105:
                return True
        return False
    icon = decor[x * MAXCELY + y]
    if (icon < 0x182 or icon > 0x18d) and icon != 0x190:
        return False
    return True


def is_fromage(decor, x, y):
    if not 0 <= x < MAXCELX or not 0 <= y < MAXCELY:
        return False
    i = x * MAXCELY + y
    return 0xf5 < decor[i] < 0xfa or decor[i] == 0x153


def is_grotte(decor, x, y):
    if not 0 <= x < MAXCELX or not 0 <= y < MAXCELY:
        return False
    return decor[x * MAXCELY + y] in [0x11c, 0x12d, 0x151]


def adapt_mid_border(decor, x, y):
    num = 0b1111
    if not is_right_border(decor, x, y + 1, 0, -1):
        num -= 0b0001
    if not is_right_border(decor, x, y - 1, 0, 1):
        num -= 0b0010
    if not is_right_border(decor, x + 1, y, -1, 0):
        num -= 0b0100
    if not is_right_border(decor, x - 1, y, 1, 0):
        num -= 0b1000

    icon = decor[x * MAXCELY + y]
    if icon == 0x9c:
        icon = 0x23
    elif icon == 0xfc or icon == 0xfd:
        icon = 0xfb
    elif icon == 0xff:
        icon = 0xfe
    elif icon == 0x16a:
        icon = 0x15b
    elif icon == 0x16b:
        icon = 0x15c
    elif 0x154 < icon < 0x15b:
        icon = 0x155
    elif 0x182 <= icon <= 0x18d: # this and on are new
        icon = 0x18c
    elif 0xba <= icon <= 0xc5:
        icon = 0xba

    if icon in table_adapt_decor:
        icon = table_adapt_decor[table_adapt_decor.index(icon) // 16 * 16 + num]
        if icon == 0x23 and random.random() < 0.5:
            icon = 0x9c
        elif icon == 0xfb:
            icon = random.randrange(0xfb, 0xfd + 1)
        elif icon == 0xfe and random.random() < 0.5:
            icon = 0xff
        elif icon == 0x15b and random.random() < 0.5:
            icon = 0x16a
        elif icon == 0x15c and random.random() < 0.5:
            icon = 0x16b
        elif icon == 0x155:
            icon = random.randrange(0x155, 0x15a + 1)
        elif icon == 0x18c and random.random() < 0.1: # this and onward are new
            icon = random.randrange(0x184, 0x187 + 1)
        elif icon == 0xc1 and random.random() < 0.5:
            icon = 0xc3
        elif icon == 0xba:
            icon = random.randrange(0xba, 0xc3 + 1)

    if icon == -1 or 0x107 < icon < 0x11b:
        num = 0b1111
        if not is_fromage(decor, x, y + 1):
            num -= 0b0001
        if not is_fromage(decor, x, y - 1):
            num -= 0b0010
        if not is_fromage(decor, x + 1, y):
            num -= 0b0100
        if not is_fromage(decor, x - 1, y):
            num -= 0b1000

        icon = table_adapt_fromage[num]
        if icon == 0x10c and random.random() < 0.5:
            icon = 0x117
        elif icon == 0x10d and random.random() < 0.5:
            icon = 0x118
        elif icon == 0x108 and random.random() < 0.5:
            icon = 0x119
        elif icon == 0x109 and random.random() < 0.5:
            icon = 0x11a

    if icon == -1 or (0x11c < icon < 0x130 and icon != 0x12d):
        num = 0b1111
        if not is_grotte(decor, x, y + 1):
            num -= 0b0001
        if not is_grotte(decor, x, y - 1):
            num -= 0b0010
        if not is_grotte(decor, x + 1, y):
            num -= 0b0100
        if not is_grotte(decor, x - 1, y):
            num -= 0b1000

        icon = table_adapt_grotte[num]
        if icon == 0x121 and random.random() < 0.5:
            icon = 0x12c
        elif icon == 0x11d and random.random() < 0.5:
            icon = 0x12e
        elif icon == 0x11e and random.random() < 0.5:
            icon = 0x12f

    decor[x * MAXCELY + y] = icon