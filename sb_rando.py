MOB_SPEED_FACTOR_MAX = 2.25
MOB_SPEED_FACTOR_MIN = 0.2
RANDOM_MOB_SPEED_CHANCE = 1.0
RANDOM_LIFT_TYPE_CHANCE = 0.1
REPLACE_EGG_WITH_CHEST_CHANCE = 0.2
MIRROR_MISSION_CHANCE = 0.5
REMOVE_EGG_CHANCE = 0.0
GIVE_EGGS_IN_HUB = True
RANDOMIZE_SOUNDS = False
PROCESS_BACKGROUNDS = True
PROCESS_MUSICS = True
PROCESS_MISSIONS = True
SEED = 1

import random, sb_util, shutil
from pathlib import Path
from PIL import Image
from enum import *


# sb_util.audit_block_data()
# exit()

class MissionType(Enum):
    NORMAL = 0
    START = 1
    TRAINING = 2
    WORLD = 3
    FINAL = 4


# noinspection PyTypeChecker
def randomize_blupi_color():
    masked = Image.open('assets/blupi-masked.png').convert('RGBA')
    sheet = Image.open('assets/blupi000.png').convert('RGBA')
    overlay = Image.open('assets/blupi-overlay.png').convert('RGBA')

    bands = list(masked.split())
    colors = []
    for i in range(4):
        bands_i = bands.copy()
        colors.append((random.random(), random.random(), random.random()))
        for j in range(3):
            bands_i[j] = bands_i[j].point(lambda x: x * colors[i][j])

        masked_new = Image.merge('RGBA', bands_i)
        sheet_new = Image.alpha_composite(sheet, masked_new)
        sheet_new.alpha_composite(overlay)
        sheet_new.save(f'game/image/blupi{i:03d}.bmp')
    overlay.close()
    sheet.close()
    masked.close()

    for i in ['init', 'win', 'lost']:
        bg = Image.open(f'assets/{i}.png').convert('RGBA')
        bg_masked = Image.open(f'assets/{i}-masked.png').convert('RGBA')
        bg_overlay = Image.open(f'assets/{i}-overlay.png').convert('RGBA')
        bg_masked_bands = list(bg_masked.split())
        for j in range(3):
            bg_masked_bands[j] = bg_masked_bands[j].point(lambda x: x * colors[0][j])
        bg_masked_new = Image.merge('RGBA', bg_masked_bands)
        bg_new = Image.alpha_composite(bg, bg_masked_new)
        bg_new.alpha_composite(bg_overlay)
        bg_new.save(f'game/image/{i}.bmp')
        bg.close()
        bg_masked.close()

def apply_mission_modifiers(data, mission_type, needs_key_goal, num_musics, num_backgrounds):
    if mission_type == MissionType.FINAL:
        mission_type = MissionType.NORMAL

    sb_util.randomize_background(data, num_backgrounds)

    if mission_type == MissionType.NORMAL or (
            mission_type == MissionType.TRAINING and sb_util.count_missions(data) == 0):
        sb_util.randomize_music(data, num_musics)

    sb_util.shuffle_block_themes(data)

    if mission_type != MissionType.TRAINING and random.random() < MIRROR_MISSION_CHANCE:  # hardcoded positions in training would break a mirrored level
        sb_util.mirror(data)

    sb_util.resolve_block_connectivity(data)

    if mission_type == MissionType.NORMAL:
        sb_util.randomly_replace_eggs_with_chests(data, REPLACE_EGG_WITH_CHEST_CHANCE)

    sb_util.randomize_mob_speed(data, RANDOM_MOB_SPEED_CHANCE, MOB_SPEED_FACTOR_MIN, MOB_SPEED_FACTOR_MAX)
    sb_util.randomize_lift_types(data, RANDOM_LIFT_TYPE_CHANCE)
    sb_util.randomly_remove_eggs(data, REMOVE_EGG_CHANCE)

    if mission_type in [MissionType.START, MissionType.WORLD] and GIVE_EGGS_IN_HUB:
        sb_util.give_free_eggs(data)

    if needs_key_goal:
        sb_util.replace_arrow_with_key(data)
    else:
        sb_util.replace_key_with_arrow(data)

    # sb_util.preview(data)

def main():
    if SEED != 0:
        random.seed(SEED)

    mission_pool = []
    training_pool = []
    world_pool = []
    start_pool = []

    mission_source_dir = Path('./missions')
    game_dir = Path('./game')
    background_source_dir = Path('./backgrounds')
    music_source_dir = Path('./musics')
    sound_source_dir = Path('./sounds')
    data_dir = None
    image_dir = None
    sound_dir = None

    for path in [x for x in game_dir.iterdir() if x.is_dir()]:
        name = path.name.lower()
        if name == 'data':
            data_dir = path
        elif name == 'image':
            image_dir = path
        elif name == 'sound':
            sound_dir = path

    assert data_dir is not None, "game data directory not found"
    assert image_dir is not None, "game image directory not found"
    assert sound_dir is not None, "game sound directory not found"

    randomize_blupi_color()

    for i in ['button00', 'bye', 'clear', 'create', 'element', 'explo', 'gamer', 'gread', 'gwrite', 'help', 'info',
              'insert', 'jauge', 'little', 'map', 'movie', 'multi', 'music', 'name', 'object', 'read', 'region',
              'service', 'session', 'setup', 'stop', 'temp', 'text', 'write']:
        path = (image_dir / f'{i}.bmp')
        if not path.is_file():
            with Image.open(f'assets/{i}.png') as image:
                image.save(path)

    num_backgrounds = 0
    num_musics = 0

    if RANDOMIZE_SOUNDS:
        print('\nprocessing sounds...')
        source_sounds = []

        for subdir in [x for x in sound_source_dir.iterdir() if x.is_dir()]:
            for path in [x for x in subdir.iterdir() if x.is_file()]:
                if path.suffix.lower() == '.wav':
                    source_sounds.append(path)

        random.shuffle(source_sounds)

        for i in range(93):
            shutil.copy(source_sounds.pop(0), sound_dir / f'sound{i:03d}.wav')
    else:
        do_we_need_to_do_this = False

        for i in range(93):
            path = sound_dir / f'sound{i}.wav'
            if not path.is_file() or path.stat().st_size != (
                    sound_source_dir / 'speedy-blupi' / path.name).stat().st_size:
                do_we_need_to_do_this = True
                break

        if do_we_need_to_do_this:
            for i in range(93):
                shutil.copy(sound_source_dir / 'speedy-blupi' / f'sound{i:03d}.wav', sound_dir / f'sound{i:03d}.wav')

    if PROCESS_BACKGROUNDS:
        print('processing backgrounds...')
        for background in [x for x in image_dir.iterdir() if
                           x.name.lower().startswith('decor') and x.suffix.lower() == '.bmp' and x.is_file()]:
            background.unlink()

        for subdir in [x for x in background_source_dir.iterdir() if x.is_dir()]:
            if num_backgrounds >= 65536:
                break
            for path in [x for x in subdir.iterdir() if x.is_file()]:
                if path.suffix.lower() in ['.bmp', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.tif']:
                    num = ((num_backgrounds + 32768) % 65536) - 32768  # cast to s16
                    num_str = f'{'-' if num < 0 else ''}{abs(num):03d}'  # printf format %.3d
                    with Image.open(path) as image:
                        if image.size[0] == image.size[1]:  # square images will be tiled
                            out_image = Image.new('RGB', (640, 480))
                            tile = image.resize((160, 160))
                            for x in range(0, 640, 160):
                                for y in range(0, 480, 160):
                                    out_image.paste(tile, (x, y))
                        else:  # non-square images get squished
                            out_image = image.resize((640, 480))
                        out_image.save(image_dir / f'decor{num_str}.bmp')
                    num_backgrounds += 1
                    if num_backgrounds >= 65536:
                        break
        print(f'{num_backgrounds} backgrounds')
        if num_backgrounds >= 65536:
            print('Warning: Max backgrounds reached. Any further are ignored.')
    else:
        num_backgrounds = len([x for x in image_dir.iterdir() if x.name.lower().startswith('decor') and x.suffix.lower() == '.bmp' and x.is_file()])
        print(f'{num_backgrounds} backgrounds found')

    if PROCESS_MUSICS:
        print('\nprocessing musics...')
        for music in [x for x in sound_dir.iterdir() if
                      x.name.lower().startswith('music') and x.suffix.lower() == '.mid' and x.is_file()]:
            music.unlink()

        for subdir in [x for x in music_source_dir.iterdir() if x.is_dir()]:
            if num_musics >= 65535:
                break
            for path in [x for x in subdir.iterdir() if x.is_file()]:
                if path.suffix.lower() == '.mid':
                    num = ((
                                       num_musics + 32769) % 65536) - 32769  # cast to s16, further offset by 1 to match game's behavior
                    num_str = f'{'-' if num < 0 else ''}{abs(num):03d}'  # printf format %.3d
                    shutil.copy(path, sound_dir / f'music{num_str}.mid')
                    num_musics += 1
                    if num_musics >= 65535:
                        break
        print(f'{num_musics} musics')
        if num_musics >= 65535:
            print('Warning: Max musics reached (65535). Any further are ignored.')
    else:
        num_musics = len([x for x in sound_dir.iterdir() if x.name.lower().startswith('music') and x.suffix.lower() == '.mid' and x.is_file()])
        print(f'{num_musics} musics found')

    if PROCESS_MISSIONS:
        for mission in [x for x in data_dir.iterdir() if
                        x.name.lower().startswith('world') and x.suffix.lower() == '.xch' and x.is_file()]:
            mission.unlink()

        print('\nprocessing missions...')
        for subdir in [x for x in mission_source_dir.iterdir() if x.is_dir()]:
            for path in [x for x in subdir.iterdir() if x.is_file()]:
                if path.suffix.lower() == '.xch':
                    with open(path, 'rb') as file:
                        data = bytearray(file.read())
                        if sb_util.count_goals(data) > 0:  # try to exclude multiplayer levels
                            mission_pool.append(path)
                elif path.suffix.lower() == '.blp' and path.name.lower().startswith('world'):
                    mission_num = int(path.name[5:-4])
                    if mission_num == 10:
                        training_pool.append(path)
                    elif mission_num == 1:
                        start_pool.append(path)
                    elif mission_num % 10 == 0:
                        with open(path, 'rb') as file:
                            data = bytearray(file.read())
                            num_missions = sb_util.count_missions(data)
                        if num_missions > 0:
                            world_pool.append(path)
                    else:
                        with open(path, 'rb') as file:
                            data = bytearray(file.read())
                            if sb_util.count_goals(data) > 0:
                                mission_pool.append(path)

        print(f'MISSION POOL {len(mission_pool)}')
        print(f'TRAINING POOL {len(training_pool)}')
        print(f'WORLD POOL {len(world_pool)}')
        print(f'START POOL {len(start_pool)}')

        random.shuffle(world_pool)
        random.shuffle(mission_pool)

        start_path = random.choice(start_pool)
        print(f'world001.xch <-- {start_path.relative_to(mission_source_dir)}')
        shutil.copy(start_path, data_dir / 'world001.xch')
        with open(data_dir / 'world001.xch', 'rb+') as start:
            data = bytearray(start.read())
            start.seek(0)
            apply_mission_modifiers(data, MissionType.START, False, num_musics, num_backgrounds)
            start.write(data)

        training_path = random.choice(training_pool)
        print(f'world010.xch <-- {training_path.relative_to(mission_source_dir)}')
        shutil.copy(training_path, data_dir / 'world010.xch')
        with open(data_dir / 'world010.xch', 'rb+') as training:
            data = bytearray(training.read())
            training.seek(0)
            apply_mission_modifiers(data, MissionType.TRAINING, True, num_musics, num_backgrounds)
            training.write(data)

        total_missions = 0
        with open(data_dir / 'world001.xch', 'rb') as start:
            data = bytearray(start.read())
            num_worlds = sb_util.count_worlds(data)
            print(f'{num_worlds} worlds to populate')

        for i in range(num_worlds):
            dest_world_name = f'world{i + 1:02d}0.xch'
            if i > 0:  # already copied training
                world_path = world_pool.pop(0)
                print(f'{dest_world_name} <-- {world_path.relative_to(mission_source_dir)}')
                shutil.copy(world_path, data_dir / dest_world_name)

            num_missions = 0
            with open(data_dir / dest_world_name, 'rb+') as world:
                data = bytearray(world.read())
                world.seek(0)
                if i > 0:
                    apply_mission_modifiers(data, MissionType.WORLD, False, num_musics, num_backgrounds)
                num_missions = sb_util.count_missions(data)
                total_missions += num_missions
                print(f'\t{num_missions} missions to populate')
                world.write(data)

            for j in range(num_missions):
                dest_mission_name = f'world{(i + 1) * 10 + j + 1:03d}.xch'
                mission_path = mission_pool.pop(0)
                print(f'\t{dest_mission_name} <-- {mission_path.relative_to(mission_source_dir)}')
                shutil.copy(mission_path, data_dir / dest_mission_name)

                with open(data_dir / dest_mission_name, 'rb+') as mission:
                    data = bytearray(mission.read())
                    mission.seek(0)
                    apply_mission_modifiers(data, MissionType.NORMAL, j == num_missions - 1, num_musics, num_backgrounds)
                    mission.write(data)

        final_path = mission_pool.pop(0)
        print(f'world199.xch <-- {final_path.relative_to(mission_source_dir)}')
        shutil.copy(final_path, data_dir / 'world199.xch')
        with open(data_dir / 'world199.xch', 'rb+') as final:
            data = bytearray(final.read())
            final.seek(0)
            apply_mission_modifiers(data, MissionType.FINAL, False, num_musics, num_backgrounds)
            final.write(data)
        print(f'\ndone with {total_missions} missions in {num_worlds} worlds')
    else:
        print(f'\ndone')


if __name__ == '__main__':
    main()
