tile_size = 32

tiles_x = 16
tiles_y = 15

screen_width = tile_size * tiles_x
screen_height = tile_size * tiles_y

map_layout = (
	'                                                                                                             ',
	'                        p                                                     p                              ',
	'                   XXXXXXXXXXXXX                                            XXXXXX                 q         ',
	'                                                                                             XXXXXXXXXXXX    ',
	'                                       q                                                                     ',
	'                                  XXXXXXXXXXXX               q                    q                          ',
	'                    p                                      XXXXX             XXXXXXXXXXXX                    ',
	'               XXXXXXXXXXXX                                                                                  ',
	'                                                                                                         q   ',
	'                                          XXXXXXXXXXXXXXXXXXXXXX                                  XXXXXXXXXXX',
	'    O                   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                     XXXXXXXXXXXXXXXXX',
	'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
	'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
	'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
	'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
)

scroll = len(map_layout[0]) > tiles_x
print(scroll)
