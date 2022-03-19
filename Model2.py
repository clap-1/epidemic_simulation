import random
import csv
import numpy as np
from people_2 import Person
from Region import Region_info
from enum import Enum
import squarify
import matplotlib.pyplot as plt

#人口密度大的地方，越容易得病
Population_Density = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]
#商业化程度越高的地方，活动性越强，越容易感染
Commercial_Degree = [5, 4, 6, 4, 7, 2, 3, 6, 9]
#卫生水平高的区域不容易得病
Health_Level = [2, 3, 4, 2, 3, 2, 3, 2, 5]


# parameters
travel_update = 14
simulation_time = 30*24
region_num = 11
Persons_num = 15000
region_width = 10
region_length = 10

infect_radius = 0.05

# 检查是否与患者接触
def check_if_contact(id, Persons, t, region):
    x = Persons[id].x
    y = Persons[id].y
    reg = Persons[id].region
    # 检查传播半径
    for k in region[reg].ret_id():
        if (k == id):
            continue
        cur_x = Persons[k].x
        cur_y = Persons[k].y
        dis = ((cur_x - x) ** 2 + (cur_y - y) ** 2) ** 0.5
        # 小于此半径才会有记录被感染，且码无论感染与否都会变红
        if (dis <= infect_radius):
            if (Persons[k].ret_state() == 'susceptible' and Persons[id].ret_state() == 'infected'):
                Persons[k].Sus_to_Exposed(t, id, Persons, Persons[k].age, region)

def trans_risk(repro_num):
    if (repro_num <= 2):
        return 1
    elif (repro_num >= 5):
        return 3
    else:
        return 2


def Find_list(a, list):
    if (a in list):
        return 1
    else:
        return 0


# 查找一个人处于sus, expo, infc, reco的状态
def Find_state(id, Persons):
    return Persons[id].ret_state()


def create_csv(path):
    with open(path, 'w', newline='') as f:
        csv_write = csv.writer(f)
        csv_head = ['id', 'sex', 'age', 'trace', 'Infected_Num', '0', '1', '2', '3'
            , '4', '5', '6', '7', '8', '9', 'place_been_to', 'trans_risk']
        csv_write.writerow(csv_head)


def write_csv(path, data_row):
    with open(path, 'a', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)


if __name__ == "__main__":
    # 初始化
    region = {}
    k = 1
    # 初始化四个区域，参数为100,100的长和宽，第9和第10区域分别为医院和隔离点
    for k in range(0, region_num):
        if (k <= 8):
            region[k] = Region_info(region_width, region_length, Population_Density[k],
                                Commercial_Degree[k], Health_Level[k])
        else:
            region[k] = Region_info(region_width, region_length)
    print(region)
    # 初始化人的信息
    Persons = {}
    p = Persons_num / region_num
    Pr = Population_Density
    region_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for k in range(0, Persons_num):
        np.random.seed(1)
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        # 不同区域根据人口密度不同，分配不同数量的人
        r = np.random.choice(region_list, p = Pr)
        sex_c = random.random()
        sex = 'male' if sex_c <= 0.5 else 'female'
        age_c = random.random()
        if (age_c <= 0.16):
            age = random.randint(1, 20)
        elif (age_c >= 0.82):
            age = random.randint(61, 80)
        else:
            age = random.randint(21, 60)
        Persons[k] = Person(k, r, x, y, 'green', 'susceptible', sex, age)
        region[Persons[k].region].add_per(k)
    # 初始化一个感染者,第一个感染者在五天后才就送入医院
    Persons[0].Init_One_Infected()
    Infected_Count = [0 for _ in range(9)]
    for t in range(0, simulation_time):
        print(t, '--------')
        for i in range(0, Persons_num):
            Persons[i].Person_Info_Update(t, region)
        for k in range(0, Persons_num):
            if (Persons[k].ret_state() == 'infected'):
                check_if_contact(k, Persons, t, region)
            #加一个判断目前是否能移动的函数
            Persons[k].change_pos(Persons[k].ret_region(), Persons[k].age, region)
        i = 0
        for i in range(9):
            for j in region[i].ret_id():
                if (Persons[j].state == 'infected'):
                    Infected_Count[i] += 1
                if (Persons[j].state == 'exposed'):
                    Infected_Count[i] += 0.2
        print(Infected_Count)
        plt.ion()
        labels = ['1' + '\n Transmission_Risk: \n' + str(Infected_Count[0]),
                  '2' + '\n Transmission_Risk: \n' + str(Infected_Count[1]),
                  '3' + '\n Transmission_Risk: \n' + str(Infected_Count[2]),
                  '4' + '\n Transmission_Risk: \n' + str(Infected_Count[3]),
                  '5' + '\n Transmission_Risk: \n' + str(Infected_Count[4]),
                  '6' + '\n Transmission_Risk: \n' + str(Infected_Count[5]),
                  '7' + '\n Transmission_Risk: \n' + str(Infected_Count[6]),
                  '8' + '\n Transmission_Risk: \n' + str(Infected_Count[7]),
                  '9' + '\n Transmission_Risk: \n' + str(Infected_Count[8])]
        #color = plt.cm.Spectral([1 for _ in range(9)])
        colors = [plt.cm.Spectral(i / float(len(labels))) for i in range(len(labels))]
        color = ['blue' for _ in range(9)]
        # for i in range(9):
        #     color.append(1)
        squarify.plot(sizes=(8, 8, 8, 8, 8, 8, 8, 8, 8), label=labels, color=color, alpha=.8)
        plt.title('Treemap of Vechile Class')
        plt.axis('off')
        plt.pause(0.1)  # 暂停0.1秒
        # 清空画布
        plt.cla()
        Infected_Count = [0 for _ in range(9)]
    plt.ioff()
    plt.show()
    #Plot
    
