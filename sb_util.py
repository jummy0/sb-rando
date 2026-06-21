import struct, random, sb_gamecode
from collections import Counter

from PIL import Image, ImageDraw
from sb_types import *

DRAW_EMPTY_MOBS = False
FIX_EMPTY_MOB_GRAPHICS = True

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
					elif sem == BlockSem.FULL_LIFT:
						sem = BlockSem.FULL_BLOCK
					attempts = 0
					while attempts < len_themes_src:
						if len(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem]) > 0:
							decor[i] = random.choice(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem])
							break
						elif sem in (BlockSem.SPECIAL_FULL, BlockSem.TRIANGLE_LEFT, BlockSem.TRIANGLE_RIGHT, BlockSem.FULL_LIFT):
							sem = BlockSem.FULL_BLOCK
						else:
							attempts += 1
							theme_idx = (theme_idx + 1) % len_themes_src

	for mob in mobs:
		if mob.type in [MobType.ASCENSEUR, MobType.CAISSE] and mob.channel == Channel.OBJECT and 0 <= mob.icon <= 0x1b8:
			theme = block_themes[mob.icon]
			if theme in themes_src:
				theme_idx = themes_src.index(theme)
				sem = block_semantics[mob.icon]
				if sem == BlockSem.FULL_BLOCK:
					sem = BlockSem.FULL_LIFT
				attempts = 0
				while attempts < len_themes_src:
					if len(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem]) > 0:
						mob.icon = random.choice(blocks_per_sem_per_theme[themes_dst[theme_idx]][sem])
						break
					elif sem in (BlockSem.SPECIAL_FULL, BlockSem.TRIANGLE_LEFT, BlockSem.TRIANGLE_RIGHT, BlockSem.FULL_LIFT):
						sem = BlockSem.FULL_BLOCK
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
		print(f'{i:03x}  {block_themes[i].name:10} {block_semantics[i].name:15} {blocks_solid[i]}')

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

	if desc_file.dimDecorX > 0:
		desc_file.posDecorX = max(0, min(blupi_x, 64 * MAXCELX - 640))

	desc_file.blupiDir[0] = BlupiDir.LEFT if desc_file.blupiDir[0] == BlupiDir.RIGHT else BlupiDir.RIGHT

def render_preview(decor, big_decor, mobs, desc_file):
	mob_icons = [
		-1,	-1, 0x0c, 0x30, 0x3a, 0x02, 0x15, 0x21,
		-1, -1, -1, -1, -1, 0x44, -1, -1,
		0x46, 0x54, -1, 0x59, 0x5a, 0x7c, -1, 0xb0,
		0x82, 0x90, -1, -1, 0xa7, 0xb1, 0xb2, -1,
		0x110, 0xee, 0xa8, -1, -1, 0x28, -1, -1,
		0xbb, -1, -1, -1, 0xc3, -1, 0xd0, -1,
		-1, 0xd4, 0xdb, 0xe2, -1, -1, 0xf4, 0xfc,
		0xfd, -1, -1,
		*[-1] * 31,
		-1, -1, -1, -1, -1,
		0x100, 0x100, -1, -1, -1,
		*[-1] * 100,
		0x101, 0x101, 0x101, 0x101
	]
	empty_mob_icon_pairs = {
		0x2e: 0x02, # treasure
		0x2f: 0x02,
		0x30: 0x02,
		0x31: 0x02,
		0x32: 0x02,
		0x33: 0x02,
		0x34: 0x02,
		0x35: 0x02,
		0x36: 0x02,
		0x37: 0x02,
		0x38: 0x02,
		0x39: 0x02,

		0x3b: 0x0c, # bomb
		0x3c: 0x0c,
		0x3d: 0x0c,
		0x3e: 0x0c,
		0x3f: 0x0c,
		0x40: 0x0c,
		0x41: 0x0c,
		0x42: 0x0c,

		0x44: 0x15, # egg
		0x45: 0x15,
		0x46: 0x15,
		0x47: 0x15,
		0x48: 0x15,
		0x49: 0x15,
		0x4a: 0x15,

		0x4b: 0x21,  # goal
		0x4c: 0x21,
		0x4d: 0x21,
		0x4e: 0x21,
		0x4f: 0x21,
		0x50: 0x21,
		0x51: 0x21,
		0x52: 0x21,

		0x61: 0x30, # hanging bomb
		0x62: 0x30,
		0x63: 0x30,
		0x64: 0x30,
		0x65: 0x30,
		0x66: 0x30,
		0x67: 0x30,
		0x68: 0x30,

		0x90: 0x44, # helicopter

		0xb3: 0x45, # moving bomb

		0xb6: 0x54, # somewhere in this range moving bomb transitions to fish
		0xb7: 0x54,
		0xb8: 0x54,
		0xb9: 0x54,
		0xba: 0x54,
		0xbb: 0x54,
		0xbc: 0x54,
		0xbd: 0x54,
		0xbe: 0x54,
		0xbf: 0x54,
		0xc0: 0x54,
		0xc1: 0x54,
		0xc2: 0x54,
		0xc3: 0x54,

		0xd2: 0x59, # jeep

		0x151: 0x82, # skateboard

	}
	image = Image.new('RGBA', (64 * MAXCELX, 64 * MAXCELY), (0, 0, 255, 255))
	boxes = Image.new('RGBA', (64 * MAXCELX, 64 * MAXCELY))
	lines = Image.new('RGBA', (64 * MAXCELX, 64 * MAXCELY))
	box_draw = ImageDraw.Draw(boxes)
	line_draw = ImageDraw.Draw(lines)
	obj = Image.open('assets/object.png').convert('RGBA')
	blupi = Image.open('assets/blupi000.png').convert('RGBA')
	blupi1 = Image.open('assets/blupi001.png').convert('RGBA')
	blupi2 = Image.open('assets/blupi002.png').convert('RGBA')
	blupi3 = Image.open('assets/blupi003.png').convert('RGBA')
	element = Image.open('assets/element.png').convert('RGBA')
	explo = Image.open('assets/explo.png').convert('RGBA')
	for i in (obj, blupi, blupi1, blupi2, blupi3, element, explo):
		i_px = i.load()
		mask = Image.new('1', i.size, 1)
		mask_px = mask.load()
		for x in range(i.size[0]):
			for y in range(i.size[1]):
				if i_px[x, y] == (0, 0, 255, 255):
					mask_px[x, y] = 0
		i.putalpha(mask)
	start_blupi = []
	for i in (blupi, blupi1, blupi2, blupi3):
		start_blupi.append(i.crop((120, 0, 180, 60)))
	secret = obj.crop((384, 832, 448, 896))

	for x in range(MAXCELX):
		for y in range(MAXCELY):
			i = x * MAXCELY + y
			tile = big_decor[i]
			if 0 <= tile <= 0x62:
				tile_image = explo.crop((144 * (tile % 16), 144 * (tile // 16), 144 * (tile % 16) + 144, 144 * (tile // 16) + 144))
				image.alpha_composite(tile_image, (x * 64, y * 64))

	for x in range(MAXCELX):
		for y in range(MAXCELY):
			i = x * MAXCELY + y
			tile = decor[i]
			if 0 <= tile <= 0x3ff:
				tile_image = obj.crop((64 * (tile % 16), 64 * (tile // 16), 64 * (tile % 16) + 64, 64 * (tile // 16) + 64))
				image.alpha_composite(tile_image, (x * 64, y * 64))

	for mob in mobs:
		if mob.type != MobType.NONE or DRAW_EMPTY_MOBS:
			fixed_blupi_channel_empty_mob = False
			mob_image = None
			x_index = mob.icon % 16
			y_index = mob.icon // 16
			if mob.type <= MobType.BOMBEPERSO4:
				if mob_icons[mob.type] != -1:
					x_index = mob_icons[mob.type] % 16
					y_index = mob_icons[mob.type] // 16
			else:
				print(f'wtf mob type {mob.type}')
			if mob.channel == Channel.ELEMENT:
				mob_image = element.crop((60 * x_index, 60 * y_index, 60 * x_index + 60, 60 * y_index + 60))
			elif mob.channel == Channel.BLUPI:
				if FIX_EMPTY_MOB_GRAPHICS and mob.type == MobType.NONE:
					if mob.icon in empty_mob_icon_pairs:
						icon = empty_mob_icon_pairs[mob.icon]
						x_index = icon % 16
						y_index = icon // 16
						mob_image = element.crop((60 * x_index, 60 * y_index, 60 * x_index + 60, 60 * y_index + 60))
						fixed_blupi_channel_empty_mob = True
					else:
						mob_image = blupi.crop((60 * x_index, 60 * y_index, 60 * x_index + 60, 60 * y_index + 60))
				else:
					mob_image = blupi.crop((60 * x_index, 60 * y_index, 60 * x_index + 60, 60 * y_index + 60))
			elif mob.channel == Channel.OBJECT:
				mob_image = obj.crop((64 * x_index, 64 * y_index, 64 * x_index + 64, 64 * y_index + 64))
			elif mob.channel == Channel.BLUPI1:
				mob_image = blupi1.crop((60 * x_index, 60 * y_index, 60 * x_index + 60, 60 * y_index + 60))
			elif mob.channel == Channel.BLUPI2:
				mob_image = blupi2.crop((60 * x_index, 60 * y_index, 60 * x_index + 60, 60 * y_index + 60))
			elif mob.channel == Channel.BLUPI3:
				mob_image = blupi3.crop((60 * x_index, 60 * y_index, 60 * x_index + 60, 60 * y_index + 60))
			else:
				if mob.type != MobType.NONE:
					print(f'mob {mob.type} used weird channel {mob.channel}')
				mob_image = secret #obj.crop((0, 0, 64, 64))
			image.alpha_composite(mob_image, (mob.posStartX, mob.posStartY))
			if mob.type == MobType.CAISSE and not mob.icon in (0x20, 0x21, 0x22):
				image.alpha_composite(secret, (mob.posStartX, mob.posStartY))
			if mob.posStartX != mob.posEndX or mob.posStartY != mob.posEndY:
				start_box = (
					mob.posStartX, mob.posStartY,
					mob.posStartX + mob_image.size[0], mob.posStartY + mob_image.size[1]
				)
				end_box = (
					mob.posEndX, mob.posEndY,
					mob.posEndX + mob_image.size[0], mob.posEndY + mob_image.size[1]
				)
				line = (
					mob.posStartX + mob_image.size[0] / 2, mob.posStartY + mob_image.size[1] / 2,
					mob.posEndX + mob_image.size[0] / 2, mob.posEndY + mob_image.size[1] / 2
				)
				box_color = (255, 0, 0) if mob.type == MobType.NONE else (255, 255, 0)
				line_color = (255, 0, 0) if mob.type == MobType.NONE else (255, 255, 255)
				box_draw.rectangle(start_box, None, box_color, 3)
				#box_draw.rectangle(end_box, None, (255, 255, 0), 3)
				line_draw.line(line, (0, 0, 0), 8)
				line_draw.line(line, line_color, 4)
				line_draw.circle((line[2], line[3]), 10, line_color, (0, 0, 0), 2)
			if mob.type == MobType.NONE:
				circle_color = (0, 128, 0)
				if mob.channel == Channel.BLUPI:
					if fixed_blupi_channel_empty_mob:
						print(f'empty mob at ({mob.posStartX},{mob.posStartY}) uses CHBLUPI icon {mob.icon:03x}')
						circle_color = (0, 255, 255)
					else:
						print(f'UNFIXED empty mob at ({mob.posStartX},{mob.posStartY}) uses CHBLUPI icon {mob.icon:03x}')
						circle_color = (255, 0, 0)
				elif mob.icon != 0 and mob.channel != -12851:
					print(f'empty mob at ({mob.posStartX},{mob.posStartY}) uses CH{mob.channel.name if hasattr(mob.channel, 'name') else mob.channel} icon {mob.icon:03x}')
				line_draw.circle((mob.posStartX + mob_image.size[0] / 2, mob.posStartY + mob_image.size[1] / 2), 30, None, circle_color, 5)
	image.alpha_composite(boxes)
	image.alpha_composite(lines)

	for i in range(4):
		pos = desc_file.blupiPos[3 - i]
		image.alpha_composite(start_blupi[3 - i], (pos[0], pos[1]))

	for i in (obj, blupi, blupi1, blupi2, blupi3, element, explo):
		i.close()
	return image