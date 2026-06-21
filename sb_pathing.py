from sb_types import *
import sb_util, random
from PIL import ImageDraw

WHITE = (255, 255, 255)
ORANGE = (255, 128, 64)
RED = (255, 64, 64)
BLUE = (0, 0, 128)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def decor_dot(draw, pos, fill):
	draw.circle((pos[0] * 64 + 32, pos[1] * 64 + 32), 15, fill, (0, 0, 0), 2)

def decor_line(draw, xy, fill):
	draw.line((xy[0] * 64 + 32, xy[1] * 64 + 32, xy[2] * 64 + 32, xy[3] * 64 + 32), fill, 10)

def is_solid(icon):
	return 0 <= icon < len_blocks_solid and blocks_solid[icon]

def flood_fill(src, dst, x, y):
	if src[x][y] != 1: return # cell is a wall
	if dst[x][y]: return # cell is already filled
	dst[x][y] = True
	if x - 1 >= 0: flood_fill(src, dst, x - 1, y)
	if y - 1 >= 0: flood_fill(src, dst, x, y - 1)
	if x + 1 < MAXCELX: flood_fill(src, dst, x + 1, y)
	if y + 1 < MAXCELY: flood_fill(src, dst, x, y + 1)

def add_chests(decor, big_decor, mobs, desc_file):
	#image = sb_util.render_preview(decor, big_decor, mobs, desc_file)
	#draw = ImageDraw.Draw(image)

	width = 10 if desc_file.dimDecorX == 0 else MAXCELX
	height = 8 if desc_file.dimDecorY == 0 else MAXCELY

	vertices = [ [0] * 100 for _ in range(100) ]
	ng_spots = [ [False] * 100 for _ in range(100) ]
	filled = [ [False] * 100 for _ in range(100) ]
	for i in range(MAXCELX * MAXCELY):
		x = i // MAXCELY
		y = i % MAXCELY
		if x < width and  y < height - 1 and (not is_solid(decor[i]) and not decor[i] == 0x44 and is_solid(decor[i + 1])) or decor[i] in (0x5b, 0x5c, 0x8a, 0xca):
			vertices[x][y] = 1
			#draw_dot(draw, (x, y), WHITE)
			if y - 1 >= 0 and not is_solid(decor[i - 1]):
				vertices[x][y - 1] = 1
				if decor[i] in (0x5b, 0x5c, 0x8a, 0xca):
					continue
				for dy in range(-2, -5, -1):
					if y + dy >= 0 and not is_solid(decor[i + dy]):
						vertices[x][y + dy] = 1
					else:
						break
				interrupted = False
				if x + 1 < width:
					for dy in range(-1, -5, -1):
						if y + dy >= 0 and not is_solid(decor[i + dy + MAXCELY]):
							vertices[x + 1][y + dy] = 1
						else:
							interrupted = False
							break
					if not interrupted and x + 2 < MAXCELX and not is_solid(decor[i - 4 + MAXCELY * 2]):
						if vertices[x + 2][y - 4] == 0:
							vertices[x + 2][y - 4] = 2
						else:
							vertices[x + 2][y - 4] = 1
				interrupted = False
				if x - 1 >= 0:
					for dy in range(-1, -5, -1):
						if y + dy >= 0 and not is_solid(decor[i + dy - MAXCELY]):
							vertices[x - 1][y + dy] = 1
						else:
							interrupted = False
							break
					if not interrupted and x - 2 >= 0 and not is_solid(decor[i - 4 - MAXCELY * 2]):
						if vertices[x - 2][y - 4] == 0:
							vertices[x - 2][y - 4] = 2
						else:
							vertices[x - 2][y - 4] = 1

	for mob in mobs: # deny treasures to be placed in positions already occupied by static mobs
		if mob.type != MobType.NONE and mob.posStartX == mob.posEndX and mob.posStartY == mob.posEndY:
			ng_spots[mob.posStartX // 64][mob.posStartY // 64] = True

	flood_fill(vertices, filled, desc_file.blupiPos[0][0] // 64, desc_file.blupiPos[0][1] // 64)
	for mob in [x for x in mobs if x.type in (MobType.TRESOR, MobType.GOAL, MobType.CLE, MobType.EGG)]:
		if mob.posStartX == mob.posEndX and mob.posStartY == mob.posEndY:
			#draw.circle((mob.posStartX // 64 * 64 + 32, mob.posStartY // 64 * 64 + 32), 10, ORANGE, BLACK, 3)
			flood_fill(vertices, filled, mob.posStartX // 64, mob.posStartY // 64)

	for i in range(MAXCELX * MAXCELX):
		x = i // MAXCELY
		y = i % MAXCELY
		if filled[x][y]:
			draw_x = x * 64 + 32
			draw_y = y * 64 + 32
			if decor[x * MAXCELY + y] != -1 and blocks_solid[decor[x * MAXCELY + y]]:
				print(f'solid block {decor[x * MAXCELY + y]:03x} at ({x},{y}) got marked ok somehow')
				#draw.line((draw_x - 20, draw_y - 20, draw_x + 20, draw_y + 20), RED, 15)
				#draw.line((draw_x - 20, draw_y + 20, draw_x + 20, draw_y - 20), RED, 15)
				continue
			if ng_spots[x][y]:
				pass
				#draw.circle((draw_x, draw_y), 24, BLACK)
				#draw.line((draw_x - 20, draw_y - 20, draw_x + 20, draw_y + 20), RED, 15)
				#draw.line((draw_x - 20, draw_y + 20, draw_x + 20, draw_y - 20), RED, 15)
			else:
				#draw.circle((draw_x, draw_y), 10, BLACK)
				num_neighbors = 0
				for neighbor in ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)):
					if 0 <= neighbor[0] < width and 0 <= neighbor[1] < width:
						if is_solid(decor[neighbor[0] * MAXCELY + neighbor[1]]):
							num_neighbors += 1
					else:
						num_neighbors += 1
				if num_neighbors < 4 and random.random() < (num_neighbors + 1) * 0.004: # this is probably temporary hopefully
					#draw.circle((draw_x, draw_y), 24, BLACK)
					#draw.line((draw_x - 20, draw_y, draw_x, draw_y + 20, draw_x + 20, draw_y - 20), GREEN, 15)
					for mob in mobs:
						if mob.type == MobType.NONE:
							mob.type = MobType.TRESOR
							mob.stepAdvance = 1
							mob.stepRecede = 1
							mob.timeStopStart = 0
							mob.timeStopEnd = 0
							mob.posStartX = x * 64 + 4
							mob.posStartY = y * 64 + 4
							mob.posEndX = x * 64 + 4
							mob.posEndY = y * 64 + 4
							mob.posCurrentX = x * 64 + 4
							mob.posCurrentY = y * 64 + 4
							mob.step = Step.STOPSTART
							mob.time = 0
							mob.phase = 0
							mob.channel = Channel.ELEMENT
							mob.icon = 0
							break
	#image.save(f'temp/{random.randrange(10000000000)}.png')
	#return image