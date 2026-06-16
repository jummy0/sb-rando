import json, shutil
from PIL import Image
from pathlib import Path

def apply(exe_bytes, patch_name):
    with open(f'patches/{patch_name}.json', 'r') as patch_file:
        patch = json.load(patch_file)
        if 'byte_sequences' in patch:
            for seq in patch['byte_sequences']:
                old = bytes.fromhex(seq['old'].replace(' ', ''))
                new = bytes.fromhex(seq['new'].replace(' ', ''))
                found = exe_bytes.find(old)
                if found == -1:
                    print(f'failed to apply patch "{patch['name'] or patch_name}". byte sequence not found: {seq['old']}')
                    exit()
                else:
                    exe_bytes[found:found+len(new)] = new
        if 'sounds' in patch:
            for sound_patch in patch['sounds']:
                shutil.copy(Path('patches') / sound_patch['new'], f'game/sound/sound{sound_patch['id']:03d}.wav')
        if 'images' in patch:
            for image_patch in patch['images']:
                base = Image.open(Path('game/image') / image_patch['base']).convert('RGBA')
                overlay = Image.open(Path('patches') / image_patch['overlay']).convert('RGBA')
                base.alpha_composite(overlay)
                base.save(Path('game/image') / image_patch['base'])
                base.close()
                overlay.close()

        print(f'applied patch "{patch['name'] or patch_name}"')