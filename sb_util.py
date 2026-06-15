import struct, random, sb_gamecode
from collections import Counter

from PIL import Image
from sb_types import *

def get_decor_as_2d_list(data):
	decor = []
	for i in range(MAXCELX):
		decor.append(list(struct.unpack_from(f'<{MAXCELY}h', data, 0x364 + i * 200)))
	return decor

def get_decor(data):
	return list(struct.unpack_from(f'<{MAXCELX * MAXCELY}h', data, 0x364))

def set_decor_as_2d_list(data, decor):
	for i in range(MAXCELX):
		struct.pack_into(f'<{MAXCELY}h', data, 0x364 + i * 200, *decor[i])

def set_decor(data, decor):
	struct.pack_into(f'<{MAXCELX * MAXCELY}h', data, 0x364, *decor)

def get_big_decor_as_2d_list(data):
	big_decor = []
	for i in range(MAXCELX):
		big_decor.append(list(struct.unpack_from(f'<{MAXCELY}h', data, 0x5184 + i * 200)))
	return big_decor

def get_big_decor(data):
	return list(struct.unpack_from(f'<{MAXCELX * MAXCELY}h', data, 0x5184))

def set_big_decor_as_2d_list(data, big_decor):
	for i in range(MAXCELX):
		struct.pack_into(f'<{MAXCELY}h', data, 0x5184 + i * 200, *big_decor[i])

def set_big_decor(data, big_decor):
	struct.pack_into(f'<{MAXCELX * MAXCELY}h', data, 0x5184, *big_decor)

def get_mobs(data):
	mobs = []
	for i in range(MAXMOVEOBJECT):
		mob_data = struct.unpack_from('<5h2x6i5h2x', data, 0x9FA4 + i * 48)
		mobs.append(Mob(*mob_data))
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
		]
		struct.pack_into('<5h2x6i5h2x', data, 0x9FA4 + i * 48, *mob_data)

def get_desc_file(data):
	st = struct.unpack_from(f'<2h200x4i3h102x{MAXBLUPI * 3}i100s', data, 0x0)
	desc_file = DescFile(
		*st[:9],
		[list(st[9 + i * 2:11 + i * 2]) for i in range(MAXBLUPI)],
		list(st[9 + 2 * MAXBLUPI:9 + 3 * MAXBLUPI]),
		st[9 + 3 * MAXBLUPI].rstrip(b'\x00')
	)
	return desc_file

def set_desc_file(data, desc_file):
	desc_data = [
		desc_file.majRev,
		desc_file.minRev,
		desc_file.posDecorX,
		desc_file.posDecorY,
		desc_file.dimDecorX,
		desc_file.dimDecorY,
		desc_file.world,
		desc_file.music,
		desc_file.region,
		*[a for b in desc_file.blupiPos for a in b],
		*desc_file.blupiDir,
		desc_file.name
	]
	struct.pack_into(f'<2h200x4i3h102x{MAXBLUPI * 3}i100s', data, 0x0, *desc_data)

def unpack(data):
	decor = get_decor(data)
	big_decor = get_big_decor(data)
	mobs = get_mobs(data)
	desc_file = get_desc_file(data)
	return decor, big_decor, mobs, desc_file

def pack(data, decor, big_decor, mobs, desc_file):
	set_decor(data, decor)
	set_big_decor(data, big_decor)
	set_mobs(data, mobs)
	set_desc_file(data, desc_file)
	return data

def count_worlds(decor):
	world_portal_ids = (
		0x09E, 0x09F, 0x0A0, 0x0A1, 0x0A2,
		0x0A3, 0x0A4, 0x0A5, 0x0A6, 0x0A7,
		0x0A8, 0x0A9, 0x0AA, 0x0AB, 0x0AC,
		0x0AD, 0x135, 0x136, 0x19B, 0x19C,
		0x19D, 0x19E, 0x19F, 0x1A0, 0x1A1,
		0x1A2, 0x1A3, 0x1A4
	)
	counter = Counter(decor)
	return sum([counter[x] for x in world_portal_ids])

def count_missions(decor):
	mission_portal_ids = (
		0x0AE, 0x0AF, 0x0B0, 0x0B1, 0x0B2,
		0x0B3, 0x0B4, 0x0B5
	)
	counter = Counter(decor)
	return sum([counter[x] for x in mission_portal_ids])

def replace_key_with_arrow(mobs):
	for mob in mobs:
		if mob.type == MobType.CLE:
			mob.type = MobType.GOAL

def replace_arrow_with_key(mobs):
	for mob in mobs:
		if mob.type == MobType.GOAL:
			mob.type = MobType.CLE

def count_goals(mobs):
	goal_types = (
		MobType.GOAL,
		MobType.CLE
	)
	counter = Counter([x.type for x in mobs])
	return sum([counter[x] for x in goal_types])

def randomize_background(desc_file, num_backgrounds):
	desc_file.region = random.randrange(num_backgrounds)

def randomize_music(desc_file, num_musics):
	desc_file.music = random.randrange(num_musics)

def randomly_remove_eggs(mobs, chance):
	if chance == 0.0: return
	for mob in mobs:
		if mob.type == MobType.EGG and random.random() < chance:
			mob.type = MobType.NONE

#def randomly_remove_chests(mobs, chance):
#	for mob in mobs:
#		if mob.type == MobType.TRESOR and random.random() < chance:
#			mob.type = MobType.NONE

def randomly_replace_eggs_with_chests(mobs, decor, chance):
	if chance == 0.0: return
	for mob in mobs:
		if mob.type == MobType.EGG and random.random() < chance:
			block = decor[mob.posCurrentX // 64 * 100 + mob.posCurrentY // 64]
			if block == -1 or not block_semantics[block] in [BlockSem.FULL_BLOCK, BlockSem.SPECIAL_FULL]:
				mob.type = MobType.TRESOR
				mob.posCurrentY -= 3
				mob.posStartY -= 3
				mob.posEndY -= 3

def randomize_mob_speed(mobs, chance, speed_min, speed_max):
	if chance == 0.0 or (speed_min == 1.0 and speed_max == 1.0): return
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

def randomize_lift_types(mobs, chance):
	if chance == 0.0: return
	lift_types = [
		MobType.ASCENSEUR,
		MobType.ASCENSEURs,
		MobType.ASCENSEURsi
	]
	for mob in mobs:
		if mob.type in lift_types and random.random() < chance:
			mob.type = random.choice(lift_types)

def give_free_eggs(mobs, desc_file):
	eggs_added = 0
	blupi_pos_x, blupi_pos_y = desc_file.blupiPos[0]
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

def resolve_block_connectivity(decor):
	for x in range(MAXCELX):
		for y in range(MAXCELY):
			sb_gamecode.adapt_mid_border(decor, x, y)
	
def shuffle_block_themes(decor, mobs):
	themes_src = (
		Theme.ROCK, Theme.TECH, Theme.MECH, Theme.PIPE,
		Theme.CHEESE, Theme.CAVE, Theme.SLIME, Theme.DREAM,
		Theme.TOY, Theme.BRICK, Theme.HOUSE, Theme.FURNITURE,
		Theme.PALACE
	)
	len_themes_src = len(themes_src)
	themes_dst = list(themes_src)
	random.shuffle(themes_dst)

	blocks_per_sem_per_theme = {}
	for theme in Theme:
		blocks_per_sem_per_theme[theme] = {}
		for sem in BlockSem:
			blocks_per_sem_per_theme[theme][sem] = [i for i, x in enumerate(block_semantics) if x == sem and block_themes[i] == theme]
	
	for x in range(MAXCELX):
		for y in range(MAXCELY):
			i = x * MAXCELY + y
			if 0 <= decor[i] <= 0x1b8:
				theme = block_themes[decor[i]]
				if theme in themes_src:
					theme_idx = themes_src.index(theme)
					sem = block_semantics[decor[i]]
					if sem == BlockSem.FG_FRINGE:
						decor[i] = -1
						continue
					for attempts in range(len_themes_src):
						if len(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem]) > 0:
							decor[i] = random.choice(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem])
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

def scramble_block_themes(decor, mobs):
	blocks_per_sem = {}
	for sem in BlockSem:
		blocks_per_sem[sem] = [i for i, x in enumerate(block_semantics) if x == sem]
	for i in range(MAXCELX * MAXCELY):
		if 0 <= decor[i] <= 0x1b8 and block_semantics[decor[i]] != BlockSem.UNIQUE:
			decor[i] = random.choice(blocks_per_sem[block_semantics[decor[i]]])
	for mob in mobs:
		if not mob.type in [MobType.ASCENSEUR, MobType.CAISSE]: continue
		if mob.channel != Channel.OBJECT: continue
		if not 0 <= mob.icon <= 0x1b8: continue
		if block_semantics[mob.icon] == BlockSem.UNIQUE: continue
		mob.icon = random.choice(blocks_per_sem[block_semantics[mob.icon]])

def audit_block_data():
	for i in range(len(block_themes)):
		print(f'{i:03x}  {block_themes[i].name:10} {block_semantics[i].name:20}')

def mirror(decor, big_decor, mobs, desc_file):
	width = 10 if desc_file.dimDecorX == 0 else MAXCELX

	for x in range(MAXCELX):
		for y in range(MAXCELY):
			i = x * MAXCELY + y
			if x < width / 2:
				decor[i], decor[(width - x - 1) * MAXCELY + y] = decor[(width - x - 1) * MAXCELY + y], decor[i]
				big_decor[i], big_decor[(width - x - 2) * MAXCELY + y] = big_decor[(width - x - 2) * MAXCELY + y], big_decor[i]
			if big_decor[i] == 0xcb and x < MAXCELX - 1: # marine plant
				big_decor[i] = -1
				big_decor[i + MAXCELY] = 0xcb
			if decor[i] in block_mirrors:
				decor[i] = block_mirrors[decor[i]]

	for mob in mobs:
		mob.posCurrentX = (width - (mob.posCurrentX // 64) - 1) * 64 + mob.posCurrentX - (mob.posCurrentX // 64) * 64
		mob.posStartX = (width - (mob.posStartX // 64) - 1) * 64 + mob.posStartX - (mob.posStartX // 64) * 64
		mob.posEndX = (width - (mob.posEndX // 64) - 1) * 64 + mob.posEndX - (mob.posEndX // 64) * 64

	blupi_x = desc_file.blupiPos[0][0]
	blupi_x = (width - (desc_file.blupiPos[0][0] // 64) - 1) * 64 + blupi_x - (blupi_x // 64) * 64
	desc_file.blupiPos[0][0] = blupi_x

	desc_file.blupiDir[0] = BlupiDir.LEFT if desc_file.blupiDir[0] == BlupiDir.RIGHT else BlupiDir.RIGHT

def preview(decor, desc_file):
	image = Image.new('RGB', (64 * MAXCELX, 64 * MAXCELY), (0, 0, 255))
	sheet = Image.open('game/image/object.bmp')
	blupi = Image.open('assets/blupi000.png').crop((120, 0, 180, 60))
	for x in range(MAXCELX):
		for y in range(MAXCELY):
			i = x * MAXCELY + y
			tile = decor[i]
			if 0 <= tile <= 0x1b8:
				tile_image = sheet.crop((64 * (tile % 16), 64 * (tile // 16), 64 * (tile % 16) + 64, 64 * (tile // 16) + 64))
				image.paste(tile_image, (x * 64, y * 64))
	blupi_pos = desc_file.blupiPos[0]
	image.paste(blupi, blupi_pos)
	blupi.close()
	sheet.close()
	image.show()
	input('Press enter to continue...')