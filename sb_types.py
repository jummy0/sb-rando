from enum import *

MAXMOVEOBJECT = 200
MAXCELX = 100
MAXCELY = 100
MAXBLUPI = 4

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

class BlupiDir(IntEnum):
	LEFT = 1
	RIGHT = 2

class Mob:
	def __init__(self,
				 type_,
				 step_advance,
				 step_recede,
				 time_stop_start,
				 time_stop_end,
				 pos_start_x,
				 pos_start_y,
				 pos_end_x,
				 pos_end_y,
				 pos_current_x,
				 pos_current_y,
				 step,
				 time,
				 phase,
				 channel,
				 icon):
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

class DescFile:
	def __init__(self,
				 maj_rev,
				 min_rev,
				 pos_decor_x,
				 pos_decor_y,
				 dim_decor_x,
				 dim_decor_y,
				 world,
				 music,
				 region,
				 blupi_pos,
				 blupi_dir,
				 name):
		self.majRev = maj_rev
		self.minRev = min_rev
		self.posDecorX = pos_decor_x
		self.posDecorY = pos_decor_y
		self.dimDecorX = dim_decor_x
		self.dimDecorY = dim_decor_y
		self.world = world
		self.music = music
		self.region = region
		self.blupiPos = blupi_pos
		self.blupiDir = blupi_dir
		self.name = name

block_themes = (
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
	*[Theme.NONE] * 40,

	# custom
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.DREAM,
	Theme.NONE,
	Theme.TOY,
	Theme.NONE,
	Theme.TOY,
	Theme.NONE,
	Theme.TOY,
	Theme.NONE,
	Theme.TOY,
	Theme.NONE,
	Theme.TOY,
	Theme.NONE,
	Theme.TOY,
	Theme.NONE,
	Theme.CHEESE,
	Theme.NONE,
	Theme.CHEESE,
	Theme.NONE,
	Theme.CHEESE,
	Theme.NONE,
	Theme.FURNITURE,
	Theme.NONE,
	Theme.FURNITURE,
	Theme.NONE,
	Theme.PALACE,
	Theme.NONE,
	Theme.PALACE,
	Theme.NONE,
	Theme.PALACE,
	Theme.NONE,
	Theme.PALACE,
	Theme.NONE,
	Theme.FURNITURE,
	Theme.NONE,
	Theme.FURNITURE,
	Theme.NONE,
	Theme.HOUSE,
	Theme.NONE,
	Theme.HOUSE,
	Theme.NONE,
	Theme.HOUSE,
	Theme.NONE,
)

block_semantics = (
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
	*[BlockSem.FG_ARCH] * 4,
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

	# custom
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
	BlockSem.FG_SECRET,
	BlockSem.UNIQUE,
)