import random
import csv
import numpy as np
from relationship import family
from relationship import class_a
from relationship import team
from people_new import Person
from Region import Region_info


# parameters
travel_update = 14
simulation_time = 30*14
region_num = 5
Persons_num = 1000*region_num
region_width = 10
region_length = 10
infect_radius = 0.05
# 暴露者的传染性（密接）
expo_c = 0.2
# 次密接的传染性
ci_expo_c = 0.01
# 感染者的传染性
infc_c = 0.9


# 若此person患病，则检查其圆域范围内的其他人，将其他人标记为
def check_if_contact(id, Persons, t):
    x = Persons[id].x
    y = Persons[id].y
    reg = Persons[id].region
    for k in region[reg].ret_id():
        if (k == id):
            continue
        cur_x = Persons[k].x
        cur_y = Persons[k].y
        dis = ((cur_x - x) ** 2 + (cur_y - y) ** 2) ** 0.5
        # 小于此半径才会有记录被感染，且码无论感染与否都会变红
        if (dis <= infect_radius):
            if (Persons[k].ret_state() == 'susceptible' and Persons[id].ret_state() == 'infected'):
                '''
                :为减小数据量，将追踪infected过去5天接触的人
                :其家人，同组同事或者同班同学都被列为一级密接
                :其在自由活动时间接触的人都被列为二级密接
                :病患共处一个区域的其他人为三级密接，包括在自由场所接触的其他人但是与其大于传播距离的其他人
                :此溯源机制在病患发病的一刻（即送往医院）触发，而不是在其得病的时间触发
                '''
                Persons[k].Sus_to_Exposed(t, id, Persons, Persons[k].age)
            elif (Persons[k].ret_state() == 'susceptible' and Persons[id].ret_state() == 'exposed'):
                Persons[k].Sus_to_ci_Exposed(t, id, Persons, Persons[k].age)

def trans_risk(repro_num):
    if(repro_num <= 2):
        return 1
    elif(repro_num >=5):
        return 3
    else:
        return 2
def Find_list(a, list):
    if(a in list):
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
                    , '4', '5', '6', '7', '8', '9','place_been_to', 'trans_risk']
        csv_write.writerow(csv_head)

def write_csv(path, data_row):
    with open(path, 'a', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)

def if_mobility(day, age, time):
    if(day != 6 and day != 7):
        if(time>=0 and time <= 9):
            if(age >= 61):
                return 'true'
            else:
                return 'false'
        else:
            return 'true'
    else:
        return 'true'
    
if __name__ == "__main__":
    '''
    1. 假设仿真时间定为白天的早上八点到晚上十点，其余时间人员不活动。
    2. 60岁以上老人的行动能力和20岁以下人群的mobility相同，20-60之间的人群行动能力稍强。
    3. 仿真时间以小时为单位，暂且定仿真时间为60天，即1440小时。
    4. 由于模拟小范围内的传播，仿真地点为学校，小区，公司，游乐场/公园等可以自由活动的地方。
    5. 仿真的人数要减少，可以减少到1000以下。
    6. 在工作日，每天早上8点到下午5点，只有60岁以上的老年人，20-60岁的无业人士可以自由移动
      （目前只考虑全部都有工作），其余人群只有在上学或者在工作两种状态，只能在学校或者公司活动。
       下午5点到晚上十点，所有人都可以自由移动，即可以进入公共场所。
    7. 在周末，所有人都可以自由移动。
    8. 仿真从0时刻开始，设定0时刻所有人都在家。
    9. 0为小区，1为公司，2为学校，3为公园
    10. 每个家庭都是4个人，每个公司的一个team都是50人，每个课堂都是50人
    '''
    # 初始化
    region = {}
    k = 1
    # 初始化四个区域，参数为100,100的长和宽，初始人数均相同
    for k in range(0, region_num):
        region[k] = Region_info(region_width, region_length)
    # 初始化人的信息
    Persons = {}
    Family = {}
    Class = {}
    Team = {}
    team_num = Persons_num*0.5//50
    #存储每刻各区域的人员信息
    Persons_region1 = []
    Persons_region2 = []
    Persons_region3 = []
    Persons_region4 = []
    #存储公园的人员位置
    Position_record = []
    p = Persons_num / region_num
    for k in range(0, int(team_num)):
        Team[k] = team(k)
    for k in range(0, Persons_num):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        # 前100个在区域0，后100个在区域1
        #r = random.randint(0, region_num - 1)
        '''
        假定每个家庭都是四口之家，一个60岁以上的老人，两个20-60岁的中年人，一个20以下的人群
        只考虑6-80岁的人群
        '''
        if(k < int(Persons_num*0.25)):
            sex_c = random.random()
            sex = 'male' if sex_c <= 0.5 else 'female'
            age = random.randint(6, 20)
            Persons[k] = Person(k, 0, x, y, 'green', 'susceptible', sex, age, k, k//50, None)
            #以6-20岁的儿童建立家庭类，再逐步添加成员
            Family[k] = family(k)
            Family[k].add_mem(k)
            if(k%50 == 0):
                Class[k//50] = class_a(k//50)
                Class[k//50].add_mem(k)
            else:
                Class[k//50].add_mem(k)
            #以6-20岁的儿童建立课堂类，再逐步添加成员
        elif(k < int(Persons_num*0.5)):
            sex = 'male'
            age = random.randint(21, 60)
            busi_id = (k - int(Persons_num*0.25))//25
            Persons[k] = Person(k, 0, x, y, 'green', 'susceptible', sex, age,
                                k - int(Persons_num * 0.25), None, busi_id)
            Team[busi_id].add_mem(k)
            Family[k - int(Persons_num * 0.25)].add_mem(k)
        elif(k < int(Persons_num * 0.75)):
            sex = 'female'
            age = random.randint(21, 60)
            busi_id = team_num - 1 - (k - int(Persons_num * 0.5)) // 25
            Persons[k] = Person(k, 0, x, y, 'green', 'susceptible', sex, age,
                                k - int(Persons_num * 0.5), None, busi_id)
            Family[k - int(Persons_num * 0.5)].add_mem(k)
            Team[busi_id].add_mem(k)
        else:
            sex_c = random.random()
            sex = 'male' if sex_c <= 0.5 else 'female'
            age = random.randint(61, 80)
            Persons[k] = Person(k, 0, x, y, 'green', 'susceptible', sex, age,
                                k - int(Persons_num * 0.75), None, None)
            Family[k - int(Persons_num * 0.75)].add_mem(k)
        region[Persons[k].region].add_per(k, 0, 0)
    # 初始化一个感染者,第一个感染者在五天后才就送入医院
    Persons[int(Persons_num*0.5)].Init_One_Infected()
    print(Family[1].ret_family_mem())
    print(Persons[int(Persons_num*0.5)].ret_if_ever_infected())
    # for k in range(0, 20):
    #     print(Class[k].ret_class_mem())
    # for k in range(0, 40):
    #     print(Team[k].ret_team_mem())
    for t in range(1, simulation_time+1):
        #目前所处仿真时间的第几周
        week = t//(14*7) + 1
        #目前属于星期几
        day = (t - (week - 1)*14*7)//14 + 1
        tim = t%14
        for i in range(0, Persons_num):
            Persons[i].Person_Info_Update(t, day, Persons[i].age, Family, Class, Team, Persons, region)
            Persons[i].Expo_ci_Expo_to_Sus(t)
        Persons_region3.append(region[3].ret_pers_id())
        Position_record.append(region[3].ret_pers_pos())
        for k in range(0, Persons_num):
            if (Persons[k].ret_state() == 'exposed' and Persons[k].ret_trans() == 'yes'):
                check_if_contact(k, Persons, t)
            # elif (Persons[k].ret_state() == 'ci-exposed' and Persons[k].ret_trans() == 'yes'):
            #     check_if_contact(k, Persons, t)
            elif (Persons[k].ret_state() == 'infected'):
                check_if_contact(k, Persons, t)
            mobility = if_mobility(day, Persons[k].age, tim)
            if(mobility == 'true'):
                Persons[k].change_pos(Persons[k].ret_region(), Persons[k].age, region)
        print('Time:', t, '-----------------------------', )
    for j in range(0, Persons_num):
        # if (Persons[j].ret_if_ever_infected() == 'yes'):
        #     print(Persons[j].incubation_time, Persons[j].recover_time, Persons[j].ret_state(),
        #           j, Persons[j].ret_health_code())
        #     print(Persons[j].ret_travel_rec())
        print(Persons[j].ret_state(), j, Persons[j].ret_health_code(), Persons[j].CC_level)
        print(Persons[j].ret_travel_rec())
        
    # print(Persons_region3)
    # print(Position_record)
    # path = 'Lay1Network_new_new.csv'
    # for j in range(0, Persons_num):
    #     if(Persons[j].ret_if_ever_infected() == 'yes'):
    #         list_rec = Persons[j].ret_travel_rec()
    #         list1 = [j, Persons[j].sex, Persons[j].age,list_rec, Persons[j].Repro_num, Find_list(0, list_rec),
    #                  Find_list(1, list_rec), Find_list(2, list_rec), Find_list(3, list_rec), Find_list(4, list_rec),
    #                  Find_list(5, list_rec), Find_list(6, list_rec), Find_list(7, list_rec), Find_list(8, list_rec),
    #                  Find_list(9, list_rec), len(list_rec), trans_risk(Persons[j].Repro_num)]
    #         write_csv(path, list1)
    #         print(j, Persons[j].sex, Persons[j].age, Persons[j].ret_travel_rec(), Persons[j].Repro_num)
