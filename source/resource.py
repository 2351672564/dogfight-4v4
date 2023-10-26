import os
import json
import random


# for start in range(9):
#     gap = 10
#     f1 = open('first_record/record_0mix_0' + str(start) + '.txt', 'r')
#     lines = f1.readlines()
#     for t in range(62):
#         print(start+gap)
#         f2 = open('first_record/record_0mix_' + str(start+gap) +'.txt', 'w')
#         gap += 10
#
#         for line in lines:
#
#             _dict = eval(line)
#             pretime = _dict['timestamp']
#             _dict['timestamp'] += random.randint(0, 30)
#             if _dict['timestamp'] < pretime:
#                 _dict['timestamp'] = pretime + random.randint(5,30)
#
#             #position
#             pos = _dict['position']
#             if pos[0] == 10.0:
#                 pos[1] += 0.130999755859375
#             else:
#                 for i in range(3):
#                     pos[i] += 0.130999755859375
#
#             # Euglar
#             euglar = _dict['Euler_angles']
#             for i in range(3):
#                 if euglar[i] != 0:
#                     euglar[i] += 0.0003598405746743083
#             # thrust_level
#             ps = random.random()
#             if ps > 0.5 and _dict['thrust_level'] != 0:
#                 _dict['thrust_level'] += 0.18815920036286116
#
#             # brake_level
#             if ps > 0.5 and _dict['brake_level'] != 0:
#                 _dict['brake_level'] += 0.18815920036286116
#
#             # flaps_level
#             if ps > 0.5 and _dict['flaps_level'] != 0:
#                 _dict['flaps_level'] += 0.18815920036286116
#
#             # horizontal_speed
#             if _dict['horizontal_speed'] != 0:
#                 _dict['horizontal_speed'] += 3.89878463745117
#
#             # vertical_speed
#             if _dict['vertical_speed'] != 0:
#                 _dict['vertical_speed'] -= 0.01878463745117
#
#             # linear_speed
#             if _dict['linear_speed'] != 0:
#                 _dict['linear_speed'] += 3.89878463745117
#
#             # move_vector
#             move_vector = _dict['move_vector']
#             for i in range(3):
#                 if move_vector[i] != 0:
#                     move_vector[i] += 0.0003598405746743083
#
#             # linear_acceleration
#             _dict['linear_acceleration'] += 0.09878463745117
#
#             # altitude
#             _dict['altitude'] += 3.02878463745117
#
#             # heading
#             if _dict['heading'] != 0:
#                 _dict['heading'] += 3
#
#             f2.write(str(_dict) + "\n")
#         f2.close()
# gap = 10
gap = 10
f1 = open('first_record/record_0mix_09.txt', 'r')
lines = f1.readlines()
for t in range(62):

    f2 = open('first_record/record_0mix_' + str(9+gap) +'.txt', 'w')
    gap += 10

    for line in lines:

        _dict = eval(line)
        pretime = _dict['timestamp']
        _dict['timestamp'] += random.randint(0, 30)
        if _dict['timestamp'] < pretime:
            _dict['timestamp'] = pretime + random.randint(5,30)

        #position
        pos = _dict['position']
        if pos[0] == 10.0:
            pos[1] += 0.130999755859375
        else:
            for i in range(3):
                pos[i] += 0.130999755859375

        # Euglar
        euglar = _dict['Euler_angles']
        for i in range(3):
            if euglar[i] != 0:
                euglar[i] += 0.0003598405746743083
        # thrust_level
        ps = random.random()
        if ps > 0.5 and _dict['thrust_level'] != 0:
            _dict['thrust_level'] += 0.18815920036286116

        # brake_level
        if ps > 0.5 and _dict['brake_level'] != 0:
            _dict['brake_level'] += 0.18815920036286116

        # flaps_level
        if ps > 0.5 and _dict['flaps_level'] != 0:
            _dict['flaps_level'] += 0.18815920036286116

        # horizontal_speed
        if _dict['horizontal_speed'] != 0:
            _dict['horizontal_speed'] += 3.89878463745117

        # vertical_speed
        if _dict['vertical_speed'] != 0:
            _dict['vertical_speed'] -= 0.01878463745117

        # linear_speed
        if _dict['linear_speed'] != 0:
            _dict['linear_speed'] += 3.89878463745117

        # move_vector
        move_vector = _dict['move_vector']
        for i in range(3):
            if move_vector[i] != 0:
                move_vector[i] += 0.0003598405746743083

        # linear_acceleration
        _dict['linear_acceleration'] += 0.09878463745117

        # altitude
        _dict['altitude'] += 3.02878463745117

        # heading
        if _dict['heading'] != 0:
            _dict['heading'] += 3

        f2.write(str(_dict) + "\n")
    f2.close()