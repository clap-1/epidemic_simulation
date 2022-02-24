import random

import numpy as np
from people import Person
from Region import Region_info

#parameters
travel_update = 14
simulation_time = 30
Persons_num = 15000
region_num = 2
region_width = 10
region_length = 10
infect_radius = 0.05
#暴露者的传染性（密接）
expo_c = 0.2
#次密接的传染性
ci_expo_c = 0.01
#感染者的传染性
infc_c = 0.9
#若此person患病，则检查其圆域范围内的其他人，将其他人标记为
def check_if_contact(id, Persons, t):
    x = Persons[id].x
    y = Persons[id].y
    reg = Persons[id].region
    for k in region[reg].ret_id():
        if(k == id):
            continue
        cur_x = Persons[k].x
        cur_y = Persons[k].y
        dis = ((cur_x - x)**2 + (cur_y - y)**2)**0.5
        #小于此半径才会有记录被感染，且码无论感染与否都会变红
        if(dis <= infect_radius):
            if(Persons[k].ret_state() == 'susceptible' and Persons[id].ret_state() == 'infected'):
                Persons[k].Sus_to_Exposed(t, id, Persons)
            elif(Persons[k].ret_state() == 'susceptible' and Persons[id].ret_state() == 'exposed'):
                Persons[k].Sus_to_ci_Exposed(t, id, Persons)

#查找一个人处于sus, expo, infc, reco的状态
def Find_state(id, Persons):
    return Persons[id].ret_state()
   
    
    
if __name__ == "__main__":
    # 初始化
    region = {}
    k = 1
    # 初始化四个区域，参数为100,100的长和宽，初始人数均相同
    for k in range(0, region_num):
        region[k] = Region_info(region_width, region_length)
    print(region)
    # 初始化人的信息
    Persons = {}
    for k in range(0, Persons_num):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        #前100个在区域0，后100个在区域1
        Persons[k] = Person(k, 0  if k < Persons_num/region_num else 1, x, y, 'green', 'susceptible')
        region[Persons[k].region].add_per(k)
    #初始化一个感染者,第一个感染者在五天后才就送入医院
    Persons[0].Init_One_Infected()
    for t in range(0, simulation_time):
        for i in range(0, Persons_num):
            Persons[i].Person_Info_Update(t)
            Persons[i].Expo_ci_Expo_to_Sus(t)
        for k in range(0, Persons_num):
            if(Persons[k].ret_state() == 'exposed' and Persons[k].ret_trans() == 'yes'):
                    check_if_contact(k, Persons, t)
            elif (Persons[k].ret_state() == 'ci-exposed' and Persons[k].ret_trans() == 'yes'):
                    check_if_contact(k, Persons, t)
            elif(Persons[k].ret_state() == 'infected'):
                r3 = random.random()
                if (r3 <= infc_c):
                    check_if_contact(k, Persons, t)
            Persons[k].change_pos(Persons[k].ret_region())
        print('Time:', t ,'-----------------------------',)
        for j in range(0, Persons_num):
            if (Persons[j].ret_if_ever_infected() == 'yes'):
                print(Persons[j].incubation_time, Persons[j].recover_time, Persons[j].ret_state(),
                      Persons[j].ret_health_code())
                print(Persons[j].ret_went_reg())
                print(Persons[j].ret_travel_rec())
    