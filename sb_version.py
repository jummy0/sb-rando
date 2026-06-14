# unimplemented

class GameVersion(Enum):
	SB_DEMO_08 = 1
	SB_DE_10 = 2
	SB_EN_10 = 3
	SB_FR_10 = 4
	SE_DEMO_10 = 5
	SE_VALUE_10 = 6
	SE_DE_10 = 7
	SE_EN_10 = 8
	SE_ES_10 = 9
	SE_FR_10 = 10
	SE_IT_10 = 11
	SE_PT_10 = 12
	SE_DE_11 = 13
	SE_EN_11 = 14
	SE_FR_11 = 15
	SE_ES_11 = 16
	SE_IT_11 = 17
	SE_PT_11 = 18
	SE_RU_11 = 19
	SB2_DE_22 = 20
	SB2_EN_22 = 21
	SB2_FR_22 = 22
	SE2_EN_10 = 23
	SE2_PT_10 = 24
	SB_JESSE_240110 = 25
	SB2_JESSE_240110 = 26

game_versions = {
	GameVersion.SB_DEMO_08:  {'crc': 0x995050cf, 'name': u'Speedy Blupi DEMO (English 0.8)'},
	GameVersion.SB_DE_10:    {'crc': 0x92687daa, 'name': u'Speedy Blupi (Deutsch 1.0)'},
	GameVersion.SB_EN_10:    {'crc': 0x5e9f7778, 'name': u'Speedy Blupi (English 1.0)'},
	GameVersion.SB_FR_10:    {'crc': 0xc04660ad, 'name': u'Speedy Blupi (Français 1.0)'},
	GameVersion.SE_DEMO_10:  {'crc': 0xbfb48e29, 'name': u'Speedy Eggbert DEMO (English 1.0)'},
	GameVersion.SE_VALUE_10: {'crc': 0x671fda8e, 'name': u'Speedy Eggbert VALUEWARE (English 1.0)'},
	GameVersion.SE_DE_10:    {'crc': 0x03dd9c3b, 'name': u'Speedy Eggbert (Deutsch 1.0)'},
	GameVersion.SE_EN_10:    {'crc': 0xc4aee5df, 'name': u'Speedy Eggbert (English 1.0)'},
	GameVersion.SE_ES_10:    {'crc': 0xf7ef2a09, 'name': u'Speedy Eggbert (Español 1.0)'},
	GameVersion.SE_FR_10:    {'crc': 0x3149b9be, 'name': u'Speedy Eggbert (Français 1.0)'},
	GameVersion.SE_IT_10:    {'crc': 0xadb2af64, 'name': u'Speedy Eggbert (Italiano 1.0)'},
	GameVersion.SE_PT_10:    {'crc': 0xba0b3cd6, 'name': u'Speedy Eggbert (Português 1.0)'},
	GameVersion.SE_DE_11:    {'crc': 0xcd6c404e, 'name': u'Speedy Eggbert (Deutsch 1.1)'},
	GameVersion.SE_EN_11:    {'crc': 0x313fd005, 'name': u'Speedy Eggbert (English 1.1)'},
	GameVersion.SE_ES_11:    {'crc': 0x397cf67c, 'name': u'Speedy Eggbert (Español 1.1)'},
	GameVersion.SE_FR_11:    {'crc': 0xffda65cb, 'name': u'Speedy Eggbert (Français 1.1)'},
	GameVersion.SE_IT_11:    {'crc': 0xd8a439c9, 'name': u'Speedy Eggbert (Italiano 1.1)'},
	GameVersion.SE_PT_11:    {'crc': 0xcf1daa7c, 'name': u'Speedy Eggbert (Português 1.1)'},
	GameVersion.SE_RU_11:    {'crc': 0x12f78c30, 'name': u'Реактивный Эгберт (Русский 1.1)'},
	GameVersion.SB2_DE_22:   {'crc': 0x15eeddf8, 'name': u'Speedy Blupi 2 (Deutsch 2.2)'},
	GameVersion.SB2_EN_22:   {'crc': 0x329402b9, 'name': u'Speedy Blupi 2 (English 2.2)'},
	GameVersion.SB2_FR_22:   {'crc': 0x52d9cdb9, 'name': u'Speedy Blupi 2 (Français 2.2)'},
	GameVersion.SE2_EN_10:   {'crc': 0x7b7238bd, 'name': u'Speedy Eggbert 2 (English 1.0)'},
	GameVersion.SE2_PT_10:   {'crc': 0xcdca3cb6, 'name': u'Speedy Eggbert 2 (Português 1.0)'},
	GameVersion.SB2_JESSE_240110: {'crc': 0x3f7794f3, 'name': u'Speedy Blupi 2 Remastered by Jesse Savoie (English 2024-01-10)'},
	GameVersion.SB_JESSE_240110: {'crc': 0xc0af89e2, 'name': u'Speedy Blupi Remastered by Jesse Savoie (English 2024-01-10)'},
}

crcs = [game_versions[i]['crc'] for i in game_versions]

detected_version = None