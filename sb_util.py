import struct, random, sb_gamecode
from collections import Counter
from PIL import Image
from sb_types import *

def get_decor_as_2d_list(data):
	decor = []
	for i in range(MAXCELX):
		decor.append(list(struct.unpack_from(f'<{MAXCELY}h', data, 0x364 + i * 200)))
	return decor

def get_decor_as_1d_list(data):
	return list(struct.unpack_from(f'<{MAXCELX * MAXCELY}h', data, 0x364))

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
	return list(struct.unpack_from(f'<{MAXCELX * MAXCELY}h', data, 0x5184))

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

def resolve_block_connectivity(data):
	decor = get_decor_as_2d_list(data)
	for x in range(MAXCELX):
		for y in range(MAXCELY):
			sb_gamecode.adapt_mid_border(decor, x, y)
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
	decor = get_decor_as_1d_list(data)
	mobs = get_mobs(data)
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
	
	set_mobs(data, mobs)
	return set_decor_as_1d_list(data, decor)

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