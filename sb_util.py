import struct, random
from collections import Counter
from enum import *
from PIL import Image

MAXMOVEOBJECT = 200
MAXCELX = 100
MAXCELY = 100

class MobType(IntEnum):
	NONE = 0
	ASCENSEUR = 1
	BOMBEDOWN = 2
	BOMBEUP = 3
	BULLDOZER = 4
	TRESOR = 5
	EGG = 6
	GOAL = 7
	EXPLO1 = 8
	EXPLO2 = 9
	EXPLO3 = 10
	EXPLO4 = 11
	CAISSE = 12
	HELICO = 13
	PLOUF = 14
	BLUP = 15
	BOMBEMOVE = 16
	POISSON = 17
	TOMATES = 18
	JEEP = 19
	OISEAU = 20
	CLE = 21
	DOOR = 22
	BALLE = 23
	SKATE = 24
	SHIELD = 25
	POWER = 26
	MAGICTRACK = 27
	TANK = 28
	BULLET = 29
	DRINK = 30
	CHARGE = 31
	BLUPIHELICO = 32
	BLUPITANK = 33
	GLU = 34
	TIPLOUF = 35
	POLLUTION = 36
	CLEAR = 37
	ELECTRO = 38
	TRESORTRACK = 39
	INVERT = 40
	INVERTSTART = 41
	INVERTSTOP = 42
	INVERTSPIN = 43
	GUEPE = 44
	OVER = 46
	ASCENSEURs = 47
	ASCENSEURsi = 48
	CLE1 = 49
	CLE2 = 50
	CLE3 = 51
	BRIDGE = 52
	TENTACULE = 53
	CREATURE = 54
	DYNAMITE = 55
	DYNAMITEf = 56
	SHIELDTRACK = 57
	HIDETRACK = 58
	EXPLO5 = 90
	EXPLO6 = 91
	EXPLO7 = 92
	EXPLO8 = 93
	EXPLO9 = 94
	EXPLO10 = 95
	BOMBEFOLLOW1 = 96
	BOMBEFOLLOW2 = 97
	SPLOUTCH1 = 98
	SPLOUTCH2 = 99
	SPLOUTCH3 = 100
	BOMBEPERSO1 = 200
	BOMBEPERSO2 = 201
	BOMBEPERSO3 = 202
	BOMBEPERSO4 = 203
	DUMMY = 999

class BlockSem(IntEnum):
	UNIQUE = 0
	FULL_BLOCK = 1
	TRIANGLE_RIGHT = 2
	TRIANGLE_LEFT = 3
	FG_SECRET = 4
	FG_ARCH = 5
	FG_FRINGE = 6
	FG_PILLAR = 7
	FG_STAND = 8
	UPPER_HALF = 9
	UPPER_QUARTER = 10
	FULL_BLOCK_TOPPER = 11
	SPECIAL_FULL = 12

# noinspection DuplicatedCode
class Theme(IntEnum):
	NONE = 0
	ROCK = 1
	TECH = 2
	MECH = 3
	BRICK = 4
	PALACE = 5
	HOUSE = 6
	SLIME = 7
	CAVE = 8
	CHEESE = 9
	TOY = 10
	DREAM = 11
	FURNITURE = 12
	WOOD = 13
	PIPE = 14

class Connex(IntEnum):
	NONE = 0
	L = 1
	U = 2
	UL = 3
	R = 4
	LR = 5
	UR = 6
	ULR = 7
	D = 8
	DL = 9
	UD = 10
	UDL = 11
	DR = 12
	DLR = 13
	UDR = 14
	UDLR = 15

class Step(IntEnum):
	NONE = 0
	STOPSTART = 1
	ADVANCE = 2
	STOPEND = 3
	RECEDE = 4

# noinspection DuplicatedCode
class Channel(IntEnum):
	BACK = 0
	OBJECT = 1
	BLUPI = 2
	DECOR = 3
	BUTTON = 4
	JAUGE = 5
	TEXT = 6
	LITTLE = 7
	MAP = 8
	EXPLO = 9
	ELEMENT = 10
	BLUPI1 = 11
	BLUPI2 = 12
	BLUPI3 = 13
	TEMP = 14

block_themes = [
	Theme.NONE,
	*[Theme.TECH] * 29,
	*[Theme.NONE] * 5,
	*[Theme.ROCK] * 6,
	*[Theme.WOOD] * 7,
	*[Theme.DREAM] * 20,
	*[Theme.NONE] * 5,
	Theme.TECH,
	*[Theme.ROCK] * 2,
	*[Theme.NONE] * 2,
	*[Theme.MECH] * 13,
	*[Theme.NONE] * 48,
	*[Theme.FURNITURE] * 5,
	*[Theme.ROCK] * 13,
	*[Theme.NONE] * 28,
	Theme.ROCK,
	*[Theme.HOUSE] * 13,
	Theme.NONE,
	*[Theme.MECH] * 2,
	*[Theme.NONE] * 13,
	*[Theme.TOY] * 22,
	*[Theme.NONE] * 9,
	*[Theme.CHEESE] * 4,
	*[Theme.PIPE] * 11,
	*[Theme.BRICK] * 3,
	*[Theme.CHEESE] * 19,
	Theme.BRICK,
	*[Theme.CAVE] * 20,
	*[Theme.NONE] * 33,
	*[Theme.CAVE] * 2,
	*[Theme.CHEESE] * 2,
	*[Theme.SLIME] * 23,
	*[Theme.NONE] * 22,
	*[Theme.PALACE] * 15,
	*[Theme.NONE] * 40
]

block_semantics = [
	*[BlockSem.FULL_BLOCK] * 15,
	*[BlockSem.TRIANGLE_RIGHT] * 2,
	*[BlockSem.TRIANGLE_LEFT] * 2,
	BlockSem.TRIANGLE_RIGHT,
	*[BlockSem.TRIANGLE_LEFT] * 2,
	BlockSem.FG_ARCH,
	*[BlockSem.SPECIAL_FULL] * 2,
	BlockSem.UPPER_HALF,
	*[BlockSem.SPECIAL_FULL] * 2,
	BlockSem.UPPER_HALF,
	BlockSem.UPPER_QUARTER,
	*[BlockSem.UNIQUE] * 5,
	*[BlockSem.FULL_BLOCK] * 6,
	*[BlockSem.FULL_BLOCK] * 4,
	*[BlockSem.UPPER_HALF] * 2,
	BlockSem.UPPER_QUARTER,
	*[BlockSem.FULL_BLOCK] * 20,
	*[BlockSem.UNIQUE] * 5,
	BlockSem.FG_SECRET,
	BlockSem.TRIANGLE_LEFT,
	BlockSem.TRIANGLE_RIGHT,
	BlockSem.FG_PILLAR,
	BlockSem.FG_ARCH,
	*[BlockSem.FULL_BLOCK] * 7,
	*[BlockSem.FG_SECRET] * 2,
	*[BlockSem.TRIANGLE_LEFT] * 2,
	*[BlockSem.TRIANGLE_RIGHT] * 2,
	*[BlockSem.UNIQUE] * 16,
	*[BlockSem.FULL_BLOCK] * 3,
	*[BlockSem.UNIQUE] * 29,
	*[BlockSem.FULL_BLOCK] * 15,
	BlockSem.TRIANGLE_LEFT,
	BlockSem.TRIANGLE_RIGHT,
	*[BlockSem.FULL_BLOCK] * 2,
	*[BlockSem.UNIQUE] * 27,
	BlockSem.FG_SECRET,
	*[BlockSem.FULL_BLOCK] * 12,
	BlockSem.FG_SECRET,
	*[BlockSem.FG_ARCH] * 3,
	*[BlockSem.UNIQUE] * 13,
	*[BlockSem.FULL_BLOCK] * 8,
	*[BlockSem.SPECIAL_FULL] * 7,
	*[BlockSem.FULL_BLOCK] * 2,
	BlockSem.SPECIAL_FULL,
	*[BlockSem.FULL_BLOCK] * 2,
	*[BlockSem.FG_ARCH] * 2,
	*[BlockSem.UNIQUE] * 9,
	*[BlockSem.FULL_BLOCK] * 18,
	*[BlockSem.FG_FRINGE] * 19,
	*[BlockSem.FULL_BLOCK] * 2,
	*[BlockSem.FG_FRINGE] * 16,
	BlockSem.FULL_BLOCK,
	*[BlockSem.FG_FRINGE] * 2,
	*[BlockSem.UNIQUE] * 33,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	*[BlockSem.FULL_BLOCK] * 23,
	*[BlockSem.UNIQUE] * 11,
	*[BlockSem.FG_ARCH] * 3,
	*[BlockSem.UNIQUE] * 8,
	*[BlockSem.FULL_BLOCK] * 12,
	BlockSem.FG_STAND,
	BlockSem.FG_PILLAR,
	*[BlockSem.FG_ARCH] * 4,
	*[BlockSem.UNIQUE] * 37,
]

block_mirrors = {
	0x0f: 0x11,
	0x10: 0x12,
	0x4a: 0x4b,
	0x57: 0x59,
	0x58: 0x5a,
	0x6e: 0x72,
	0x7e: 0x81,
	0x9a: 0x9b
}

for k in list(block_mirrors):
	block_mirrors[block_mirrors[k]] = k

class Mob:
	def __init__(self, type_, step_advance, step_recede, time_stop_start, time_stop_end, pos_start_x, pos_start_y, pos_end_x, pos_end_y, pos_current_x, pos_current_y, step, time, phase, channel, icon):
		self.type = type_
		self.stepAdvance = step_advance
		self.stepRecede = step_recede
		self.timeStopStart = time_stop_start
		self.timeStopEnd = time_stop_end
		self.posStartX = pos_start_x
		self.posStartY = pos_start_y
		self.posEndX = pos_end_x
		self.posEndY = pos_end_y
		self.posCurrentX = pos_current_x
		self.posCurrentY = pos_current_y
		self.step = step
		self.time = time
		self.phase = phase
		self.channel = channel
		self.icon = icon

def get_decor_as_2d_list(data):
	decor = []
	for i in range(MAXCELX):
		decor.append(list(struct.unpack_from(f'<{MAXCELY}h', data, 0x364 + i * 200)))
	return decor

def get_decor_as_1d_list(data):
	return struct.unpack_from(f'<{MAXCELX * MAXCELY}h', data, 0x364)

def set_decor_as_2d_list(data, decor):
	for i in range(MAXCELX):
		struct.pack_into(f'<{MAXCELY}h', data, 0x364 + i * 200, *decor[i])
	return data

def set_decor_as_1d_list(data, decor):
	struct.pack_into(f'<{MAXCELX * MAXCELY}h', data, 0x364, *decor)
	return data

def get_big_decor_as_2d_list(data):
	big_decor = []
	for i in range(MAXCELX):
		big_decor.append(list(struct.unpack_from(f'<{MAXCELY}h', data, 0x5184 + i * 200)))
	return big_decor

def get_big_decor_as_1d_list(data):
	return struct.unpack_from(f'<{MAXCELX * MAXCELY}h', data, 0x5184)

def set_big_decor_as_2d_list(data, big_decor):
	for i in range(MAXCELX):
		struct.pack_into(f'<{MAXCELY}h', data, 0x5184 + i * 200, *big_decor[i])
	return data

def set_big_decor_as_1d_list(data, big_decor):
	struct.pack_into(f'<{MAXCELX * MAXCELY}h', data, 0x5184, *big_decor)
	return data

def get_mobs(data):
	mobs = []
	for i in range(MAXMOVEOBJECT):
		mob_data = struct.unpack_from('<6h6i5h', data, 0x9FA4 + i * 48)
		mobs.append(Mob(*mob_data[:5], *mob_data[6:])) #skip alignment padding
	return mobs

def set_mobs(data, mobs):
	for i in range(MAXMOVEOBJECT):
		mob = mobs[i]
		mob_data = [
			mob.type,
			mob.stepAdvance,
			mob.stepRecede,
			mob.timeStopStart,
			mob.timeStopEnd,
			0,
			mob.posStartX,
			mob.posStartY,
			mob.posEndX,
			mob.posEndY,
			mob.posCurrentX,
			mob.posCurrentY,
			mob.step,
			mob.time,
			mob.phase,
			mob.channel,
			mob.icon,
			0
		]
		struct.pack_into('<6h6i6h', data, 0x9FA4 + i * 48, *mob_data)
	return data


def count_worlds(data):
	world_portal_ids = [
		0x09E, 0x09F, 0x0A0, 0x0A1, 0x0A2,
		0x0A3, 0x0A4, 0x0A5, 0x0A6, 0x0A7,
		0x0A8, 0x0A9, 0x0AA, 0x0AB, 0x0AC,
		0x0AD, 0x135, 0x136, 0x19B, 0x19C,
		0x19D, 0x19E, 0x19F, 0x1A0, 0x1A1,
		0x1A2, 0x1A3, 0x1A4
	]
	counter = Counter(get_decor_as_1d_list(data))
	return sum([counter[x] for x in world_portal_ids])

def count_missions(data):
	mission_portal_ids = [
		0x0AE, 0x0AF, 0x0B0, 0x0B1, 0x0B2,
		0x0B3, 0x0B4, 0x0B5
	]
	counter = Counter(get_decor_as_1d_list(data))
	return sum([counter[x] for x in mission_portal_ids])

def replace_key_with_arrow(data):
	mobs = get_mobs(data)
	for mob in mobs:
		if mob.type == MobType.CLE:
			mob.type = MobType.GOAL
	return set_mobs(data, mobs)

def replace_arrow_with_key(data):
	mobs = get_mobs(data)
	for mob in mobs:
		if mob.type == MobType.GOAL:
			mob.type = MobType.CLE
	return set_mobs(data, mobs)

def count_goals(data):
	goal_types = [
		MobType.GOAL,
		MobType.CLE
	]
	counter = Counter([x.type for x in get_mobs(data)])
	return sum([counter[x] for x in goal_types])

def randomize_background(data, num_backgrounds):
	struct.pack_into('<H', data, 0xE0, random.randrange(num_backgrounds))

def randomize_music(data, num_musics):
	struct.pack_into('<H', data, 0xDE, random.randrange(num_musics) + 1)

def randomly_remove_eggs(data, chance):
	if chance == 0.0:
		return data
	mobs = get_mobs(data)
	for mob in mobs:
		if mob.type == MobType.EGG and random.random() < chance:
			mob.type = MobType.NONE
	return set_mobs(data, mobs)

#def randomly_remove_chests(data, chance):
#	mobs = get_mobs(data)
#	for mob in mobs:
#		if mob.type == MobType.TRESOR and random.random() < chance:
#			mob.type = MobType.NONE
#	return set_mobs(data, mobs)

def randomly_replace_eggs_with_chests(data, chance):
	if chance == 0.0:
		return data
	mobs = get_mobs(data)
	decor = get_decor_as_2d_list(data)
	for mob in mobs:
		if mob.type == MobType.EGG and random.random() < chance:
			block = decor[mob.posCurrentX // 64][mob.posCurrentY // 64]
			if block == -1 or not block_semantics[block] in [BlockSem.FULL_BLOCK, BlockSem.SPECIAL_FULL]:
				mob.type = MobType.TRESOR
				mob.posCurrentY -= 3
				mob.posStartY -= 3
				mob.posEndY -= 3
	return set_mobs(data, mobs)

def randomize_mob_speed(data, chance, speed_min, speed_max):
	if chance == 0.0 or (speed_min == 1.0 and speed_max == 1.0):
		return data
	mobs = get_mobs(data)
	for mob in mobs:
		if random.random() < chance and (mob.stepAdvance > 1 or mob.stepRecede > 1 or mob.timeStopStart > 0 or mob.timeStopEnd > 0):
			mob.stepAdvance = int(mob.stepAdvance / (random.random() * (speed_max - speed_min) + speed_min))
			mob.stepRecede = int(mob.stepRecede / (random.random() * (speed_max - speed_min) + speed_min))
			mob.timeStopStart = max(0, int(mob.timeStopStart / (random.random() * (speed_max - speed_min) + speed_min)) + random.randrange(-10, 10))
			mob.timeStopEnd = max(0, int(mob.timeStopEnd / (random.random() * (speed_max - speed_min) + speed_min)) + random.randrange(-10, 10))
			if mob.type == MobType.BLUPIHELICO or mob.type == MobType.BLUPITANK:
				# ensure ranged attacking mobs have time to fire
				mob.timeStopStart = max(mob.timeStopStart, 21)
				mob.timeStopEnd = max(mob.timeStopEnd, 21)
	return set_mobs(data, mobs)

def randomize_lift_types(data, chance):
	if chance == 0.0:
		return data
	lift_types = [
		MobType.ASCENSEUR,
		MobType.ASCENSEURs,
		MobType.ASCENSEURsi
	]
	mobs = get_mobs(data)
	for mob in mobs:
		if mob.type in lift_types and random.random() < chance:
			mob.type = random.choice(lift_types)
	return set_mobs(data, mobs)

def give_free_eggs(data):
	mobs = get_mobs(data)
	eggs_added = 0
	blupi_pos_x, blupi_pos_y = struct.unpack_from('<2i', data, 0x148)
	for mob in mobs:
		if mob.type == MobType.NONE:
			mob.type = MobType.EGG
			mob.stepAdvance = 1
			mob.stepRecede = 1
			mob.timeStopStart = 0
			mob.timeStopEnd = 0
			mob.posStartX = blupi_pos_x
			mob.posStartY = blupi_pos_y
			mob.posEndX = blupi_pos_x
			mob.posEndY = blupi_pos_y
			mob.posCurrentX = blupi_pos_x
			mob.posCurrentY = blupi_pos_y
			mob.step = Step.STOPSTART
			mob.time = 0
			mob.phase = 0
			mob.channel = Channel.ELEMENT
			mob.icon = 21
			eggs_added += 1
			if eggs_added >= 11:
				break
	set_mobs(data, mobs)

table_adapt_decor = [
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
	0x18d, 0x18d, 0x18c, 0x18d,

	0xfb, 0xfe, 0xfe, 0xfe,
	0xfb, 0x102, 0x104, 0x102,
	0xfb, 0x101, 0x103, 0x101,
	0xfb, 0xfa, 0x100, 0xfa
]

table_adapt_fromage = [
	-1, 0x109, 0x108, 0x10c,
	0x10b, 0x111, 0x10f, 0x113,
	0x10a, 0x110, 0x10e, 0x112,
	0x10d, 0x115, 0x114, 0x116
]

table_adapt_grotte = [
	-1, 0x11e, 0x11d, 0x121,
	0x120, 0x126, 0x124, 0x128,
	0x11f, 0x125, 0x123, 0x127,
	0x122, 0x12a, 0x129, 0x12b
]

def _is_right_border(decor, x, y, dx, dy):
	if not 0 <= x < MAXCELX or not 0 <= y < MAXCELY:
		return True
	icon = decor[x + dx][y + dy]
	if (icon < 0x182 or icon > 0x104) and icon != 400:
		if icon < 250 or icon > 260:
			icon = decor[x][y]
			if icon == -1:
				return False
			if not icon in [32, 33, 34]:
				if icon == 92 or icon == 68:
					return dy != -1
				if icon == 317:
					return dy != 1
				if icon in [19, 21, 25, 26, 28]:
					return dy != 1
				if icon == 27:
					return dx == 0
				if 0x2c < icon < 0x30:
					return dy != 1
				if icon in [0xf, 0x10, 0x4b, 0x59, 0x5a, 0x9b]:
					b_var = dx == -1
				else:
					if not icon in [17, 18, 74, 87, 88, 154]:
						if icon in [76, 77, 199, 200]:
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
						if icon in [107, 108, 109, 157]:
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
			icon = decor[x][y]
			if 0xf9 < icon < 0x105:
				return True
		return False
	icon = decor[x][y]
	if (icon < 0x182 or icon > 0x18d) and icon != 400:
		return False
	return True

def _is_fromage(decor, x, y):
	if not 0 <= x < MAXCELX or not 0 <= y < MAXCELY:
		return False
	return 0xf5 < decor[x][y] < 0xfa or decor[x][y] == 0x153

def _is_grotte(decor, x, y):
	if not 0 <= x < MAXCELX or not 0 <= y < MAXCELY:
		return False
	return decor[x][y] in [0x11c, 0x12d, 0x151]

def _adapt_mid_border(decor, x, y):
	num = 0b1111
	if not _is_right_border(decor, x, y + 1, 0, -1):
		num -= 0b0001
	if not _is_right_border(decor, x, y - 1, 0, 1):
		num -= 0b0010
	if not _is_right_border(decor, x + 1, y, -1, 0):
		num -= 0b0100
	if not _is_right_border(decor, x - 1, y, 1, 0):
		num -= 0b1000

	icon = decor[x][y]
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
	
	for i in range(len(table_adapt_decor)):
		if icon == table_adapt_decor[i]:
			icon = table_adapt_decor[i // 16 * 16 + num]
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
	
	if icon == -1 or 0x107 < icon < 0x11b:
		num = 0b1111
		if not _is_fromage(decor, x, y + 1):
			num -= 0b0001
		if not _is_fromage(decor, x, y - 1):
			num -= 0b0010
		if not _is_fromage(decor, x + 1, y):
			num -= 0b0100
		if not _is_fromage(decor, x - 1, y):
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
		if not _is_grotte(decor, x, y + 1):
			num -= 0b0001
		if not _is_grotte(decor, x, y - 1):
			num -= 0b0010
		if not _is_grotte(decor, x + 1, y):
			num -= 0b0100
		if not _is_grotte(decor, x - 1, y):
			num -= 0b1000
		
		icon = table_adapt_grotte[num]
		if icon == 0x121 and random.random() < 0.5:
			icon = 0x12c
		elif icon == 0x11d and random.random() < 0.5:
			icon = 0x12e
		elif icon == 0x11e and random.random() < 0.5:
			icon = 0x12f
	
	decor[x][y] = icon

def resolve_block_connectivity(data):
	decor = get_decor_as_2d_list(data)
	for x in range(MAXCELX):
		for y in range(MAXCELY):
			_adapt_mid_border(decor, x, y)
	return set_decor_as_2d_list(data, decor)
	
def shuffle_block_themes(data):
	decor = get_decor_as_2d_list(data)
	mobs = get_mobs(data)
	themes_src = [
		Theme.ROCK, Theme.TECH, Theme.MECH, Theme.PIPE,
		Theme.CHEESE, Theme.CAVE, Theme.SLIME, Theme.DREAM,
		Theme.TOY, Theme.BRICK, Theme.HOUSE, Theme.FURNITURE,
		Theme.PALACE
	]
	len_themes_src = len(themes_src)
	themes_dst = themes_src.copy()
	random.shuffle(themes_dst)

	blocks_per_sem_per_theme = {}
	for theme in Theme:
		blocks_per_sem_per_theme[theme] = {}
		for sem in BlockSem:
			blocks_per_sem_per_theme[theme][sem] = [i for i, x in enumerate(block_semantics) if x == sem and block_themes[i] == theme]
	
	for x in range(MAXCELX):
		for y in range(MAXCELY):
			if 0 <= decor[x][y] <= 0x1b8:
				theme = block_themes[decor[x][y]]
				if theme in themes_src:
					theme_idx = themes_src.index(theme)
					sem = block_semantics[decor[x][y]]
					if sem == BlockSem.FG_FRINGE:
						decor[x][y] = -1
						continue
					for attempts in range(len_themes_src):
						if len(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem]) > 0:
							decor[x][y] = random.choice(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem])
							break
						else:
							attempts += 1
							theme_idx = (theme_idx + 1) % len_themes_src

	for mob in mobs:
		if mob.type in [MobType.ASCENSEUR, MobType.CAISSE] and mob.channel == Channel.OBJECT and 0 <= mob.icon <= 0x1b8:
			theme = block_themes[mob.icon]
			if theme in themes_src:
				theme_idx = themes_src.index(theme)
				sem = block_semantics[mob.icon]
				for attempts in range(len_themes_src):
					if len(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem]) > 0:
						mob.icon = random.choice(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem])
						break
					else:
						attempts += 1
						theme_idx = (theme_idx + 1) % len_themes_src
	set_mobs(data, mobs)
	return set_decor_as_2d_list(data, decor)

def scramble_block_themes(data):
	decor = get_decor_as_2d_list(data)
	mobs = get_mobs(data)
	blocks_per_sem = {}
	for sem in BlockSem:
		blocks_per_sem[sem] = [i for i, x in enumerate(block_semantics) if x == sem]
	for x in range(MAXCELX):
		for y in range(MAXCELY):
			if 0 <= decor[x][y] <= 0x1b8 and block_semantics[decor[x][y]] != BlockSem.UNIQUE:
				decor[x][y] = random.choice(blocks_per_sem[block_semantics[decor[x][y]]])
	for mob in mobs:
		if not mob.type in [MobType.ASCENSEUR, MobType.CAISSE]: continue
		if mob.channel != Channel.OBJECT: continue
		if not 0 <= mob.icon <= 0x1b8: continue
		if block_semantics[mob.icon] == BlockSem.UNIQUE: continue
		mob.icon = random.choice(blocks_per_sem[block_semantics[mob.icon]])
	
	set_mobs(data, mobs)
	return set_decor_as_2d_list(data, decor)

def audit_block_data():
	for i in range(len(block_themes)):
		print(f'{i:03x}  {block_themes[i].name:10} {block_semantics[i].name:20}')

def mirror(data):
	width = 10 if struct.unpack_from('<i', data, 0xd4)[0] == 0 else MAXCELX

	decor = get_decor_as_2d_list(data)
	decor = list(reversed(decor[:width])) + decor[width:]
	for i in range(MAXCELX * MAXCELY):
		cx = i // MAXCELY
		cy = i % MAXCELY
		if decor[cx][cy] in block_mirrors:
			decor[cx][cy] = block_mirrors[decor[cx][cy]]
	
	big_decor = get_big_decor_as_2d_list(data)
	big_decor = list(reversed(big_decor[:width])) + decor[width:]

	mobs = get_mobs(data)
	for mob in mobs:
		mob.posCurrentX = (width - (mob.posCurrentX // 64) - 1) * 64 + mob.posCurrentX - (mob.posCurrentX // 64) * 64
		mob.posStartX = (width - (mob.posStartX // 64) - 1) * 64 + mob.posStartX - (mob.posStartX // 64) * 64
		mob.posEndX = (width - (mob.posEndX // 64) - 1) * 64 + mob.posEndX - (mob.posEndX // 64) * 64
	
	blupi_pos_x = struct.unpack_from('<i', data, 0x148)[0]
	blupi_pos_x = (width - (blupi_pos_x // 64) - 1) * 64 + blupi_pos_x - (blupi_pos_x // 64) * 64
	struct.pack_into('<i', data, 0x148, blupi_pos_x)

	blupi_dir = struct.unpack_from('<i', data, 0x168)[0]
	blupi_dir = 3 - blupi_dir
	struct.pack_into('<i', data, 0x168, blupi_dir)

	set_mobs(data, mobs)
	set_big_decor_as_2d_list(data, big_decor)
	return set_decor_as_2d_list(data, decor)

def preview(data):
	image = Image.new('RGB', (64 * MAXCELX, 64 * MAXCELY), (0, 0, 255))
	sheet = Image.open('game/image16/object.bmp')
	blupi = Image.open('assets/blupi000.png').crop((120, 0, 180, 60))
	decor = get_decor_as_2d_list(data)
	for x in range(MAXCELX):
		for y in range(MAXCELY):
			tile = decor[x][y]
			if 0 <= tile <= 0x1b8:
				tile_image = sheet.crop((64 * (tile % 16), 64 * (tile // 16), 64 * (tile % 16) + 64, 64 * (tile // 16) + 64))
				image.paste(tile_image, (x * 64, y * 64))
	blupi_pos = struct.unpack_from('<2i', data, 0x148)
	image.paste(blupi, blupi_pos)
	blupi.close()
	sheet.close()
	image.show()
	input('Press enter to continue...')