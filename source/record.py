#运行路径设置
import sys
import time, keyboard
sys.path.insert(0,r'D:\Pyproject\dogfight-sandbox-hg2-main\dogfight-sandbox-hg2-main\network_client_example')
#库引用
import dogfight_client as df
import network_server as ns
import re
import argparse


def change_missile_name(missiles):
    missiles_changed=[]
    for missile_name in missiles:
        if missile_name=='':
            continue
        else:
            missile_name_split=re.split('([0-9]+)', missile_name)
            missiles_changed.append(missile_name_split[0]+missile_name_split[1]+'-'+missile_name_split[2]+'-'+missile_name_split[3])
    return missiles_changed

#连接测试平台
address=ns.get_network()
df.connect(address[0],address[1])
#获得参数
f = open('first_record/record_0mix_09.txt', "w")

while True:
    planes = df.get_planes_list()
    for i, plane in enumerate(planes):
        states = df.get_plane_state(plane)
        for j, state in enumerate(states):
            state['id'] = planes[j]
            f.write(str(state) + "\n")

