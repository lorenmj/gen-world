# gen-world

Generate a grid pattern world with terrain options using perlin noise generation written in Python.

Uses and depends on https://github.com/caseman/noise

Typical output using seed 0, no command line parameters, all defaults:

Generating world of size 1000 by 1000...
Seed 0 Water Percentage 15.0 Land Feature Variant 24.0.
Make water level 45 or below..
Rivers to make: 10.
River start:0 from [844x758] length of 842.
Eroding..river. Length: 842.
Eroding..Done
River start:1 from [239x968] length of 57.
Eroding..river. Length: 899.
Eroding..Done
River start:2 from [879x900] length of 648.
Eroding..river. Length: 1547.
Eroding..Done
River start:3 from [105x422] length of 1579.
Eroding..river. Length: 3126.
Eroding..Done
River start:4 from [998x153] length of 812.
Eroding..river. Length: 3938.
Eroding..Done
River start:5 from [560x817] length of 753.
Eroding..river. Length: 4691.
Eroding..Done
River start:6 from [546x161] length of 1759.
Eroding..river. Length: 6450.
Eroding..Done
River start:7 from [487x107] length of 1323.
Eroding..river. Length: 7773.
Eroding..Done
River start:8 from [780x604] length of 1033.
Eroding..river. Length: 8806.
Eroding..Done
River start:9 from [758x616] length of 1396.
Eroding..river. Length: 10202.
Eroding..Done
Generated. Normalizing...
Normalize results: MAX 240 MIN 11 CNT 1000000 AVG 123
Area around 84 x 73
145 [016] | 144 [012] | 142 [016]
----------+-----------+----------
152 [010] | 150 [000] | 148 [012]
----------+-----------+----------
158 [014] | 156 [010] | 154 [014]
] Row 71 *****
] Row 72 *****
] Row 73 %%***
] Row 74 %%%%%
] Row 75 %%%%%
Creating map representations:
PGM world.pgm [DONE]
PPM world.ppm [DONE]
TEXT world.txt [DONE]
Saving generated world to files.


