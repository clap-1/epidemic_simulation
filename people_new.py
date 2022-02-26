import numpy as np
import csv
import random as rd

region_num = 4
# region_change_rate = 0.3
# coordinate_change = 0.5
region_width = 10
region_length = 10
# #暴露者的传染性（密接）
# expo_c = 0.2
# #次密接的传染性(本身次密接的传染性低，不再对各个年龄段划分)
ci_expo_c = 0.01
#

# #感染者的传染性
# infc_c = 0.9

# 暴露者的传染性（密接）
def exposed_c(age):
    if (0 <= age <= 12):
        expo_c = 0.25
        return expo_c
    elif (13 <= age <= 20):
        expo_c = 0.2
        return expo_c
    elif (21 <= age <= 40):
        expo_c = 0.15
        return expo_c
    elif (41 <= age <= 60):
        expo_c = 0.15
        return expo_c
    elif (61 <= age <= 80):
        expo_c = 0.25
        return expo_c


# 感染者的传染性
def infetcd_c(age):
    if (0 <= age <= 12):
        infc_c = 0.8
        return infc_c
    elif (13 <= age <= 20):
        infc_c = 0.75
        return infc_c
    elif (21 <= age <= 40):
        infc_c = 0.7
        return infc_c
    elif (41 <= age <= 60):
        infc_c = 0.7
        return infc_c
    elif (61 <= age <= 80):
        infc_c = 0.8
        return infc_c


# 不同年龄段人群的位置转移概率，在此模型假设下，假设每个人在自由转移状态下，只会转移到公共场所，在公共场所自由活动的能力都相同都为0.2
def pos_change_rate(age):
    if (6 <= age <= 20):
        region_change_pro = 0.1
        coordinate_change_pro = 0.5
        return [region_change_pro, coordinate_change_pro]
    elif (21 <= age <= 60):
        region_change_pro = 0.2
        coordinate_change_pro = 0.5
        return [region_change_pro, coordinate_change_pro]
    elif (61 <= age <= 80):
        region_change_pro = 0.1
        coordinate_change_pro = 0.5
        return [region_change_pro, coordinate_change_pro]


# class人，记录每个人的区域信息，在该区域的位置信息，健康状态等
class Person(object):
    def __init__(self, id, region, x, y, healthcode, state, sex, age,
                 family_id = None, class_id = None, business_id = None):
        self.id = id
        self.sex = sex
        self.age = age
        self.region = region
        self.family_id = family_id
        self.class_id = class_id
        self.business_id = business_id
        self.x = x
        self.y = y
        self.healthcode = healthcode
        self.if_ever_infected = 'no'
        # 感染人数
        self.Repro_num = 0
        # 是否具有病毒传播性
        self.trans = 'no'
        self.went_reg = [region]
        # 行程卡
        self.travel_rec = []
        # state为susceptible, exposed, infected, recovered四种
        self.state = state
        self.ci_expo_expo_to_sus_time = None
        # sus->expos后的潜伏时间
        self.incubation_time_inte = None
        # sus->expos的时间点
        self.incubation_time = None
        # 感染时间点
        self.infected_time = None
        # 感染后两天之内送入医院
        self.hosp_time = None
        # 感染后治疗恢复所用时间
        self.hosp_time_inte = None
        # 感染后恢复时间点
        self.recover_time = None
    
    # 返回id
    def ret_id(self):
        return id
    
    def ret_trans(self):
        return self.trans
    
    # 返回健康码
    def ret_health_code(self):
        return self.healthcode
    
    # 返回所处区域
    def ret_region(self):
        return self.region

    # 返回是否曾经患病
    def ret_if_ever_infected(self):
        return self.if_ever_infected
    
    # 返回位置坐标
    def ret_position(self):
        return self.x, self.y
    
    def ret_state(self):
        return self.state

    # 行程卡添加，添加前往过的地方
    def add_went_reg(self, iregion):
        self.went_reg.append(iregion)

    # 返回过去十四天的行程卡
    def ret_travel_rec(self):
        l1 = []
        if (len(self.went_reg) >= 14):
            l1 = self.went_reg[-14:-1]
            self.travel_rec = l1.copy()
            self.travel_rec = list(set(self.travel_rec))
        else:
            self.travel_rec = list(set(self.went_reg))
        return self.travel_rec
    
    # 返回行程卡
    def ret_went_reg(self):
        return self.went_reg
    
    # 下一刻的region及坐标,传入参数为当前region
    def change_pos(self, iregion, age):
        prob = pos_change_rate(age)
        region_change_rate = prob[0]
        coordinate_change_rate = prob[1]
        region_change = rd.random()
        if(region_change <= region_change_rate):
            reg_new = 3
            self.add_went_reg(reg_new)
            self.region = reg_new
            coordinate_change = rd.random()
            if(coordinate_change)
        if (place_change <= coordinate_change_rate):
            region_change = rd.random()
            if (region_change <= region_change_rate):
                reg_new = rd.randint(0, region_num - 1)
                while (reg_new == iregion):
                    reg_new = rd.randint(0, region_num - 1)
                self.add_went_reg(reg_new)
                # 下一刻的region
                self.region = reg_new
            else:
                self.add_went_reg(iregion)
            x = rd.uniform(0, region_width)
            y = rd.uniform(0, region_length)
            # 下一刻的坐标
            self.x = x
            self.y = y
        else:
            self.add_went_reg(iregion)

    # sus->exposed后,潜伏期为2-14天，传入参数为此转换的时间,与感染者接触后成为密接
    def Sus_to_Exposed(self, t, id, Persons, age):
        self.state = 'exposed'
        r1 = rd.random()
        if (r1 <= infetcd_c(age)):
            Persons[id].Repro_num = Persons[id].Repro_num + 1
            t1 = rd.randint(2, 14)
            self.incubation_time_inte = t1
            self.incubation_time = t
            self.infected_time = t + t1
            self.trans = 'yes'
            # 返回潜伏期结束的时间点，在此时间点之后此人出现症状或者自动康复，即不再具有传播性
            return self.trans
        else:
            self.trans = 'no'
            return self.trans

    # 与密接者接触后成为次密接
    def Sus_to_ci_Exposed(self, t, id, Persons, age):
        self.state = 'ci-exposed'
        r1 = rd.random()
        if (r1 <= exposed_c(age)):
            Persons[id].Repro_num = Persons[id].Repro_num + 1
            t1 = rd.randint(2, 14)
            self.incubation_time_inte = t1
            self.incubation_time = t
            self.infected_time = t + t1
            self.trans = 'yes'
            # 返回潜伏期结束的时间点，在此时间点之后此人出现症状或者自动康复，即不再具有传播性
            return self.trans
        else:
            self.trans = 'no'
            return self.trans
    
    ######################注：此处次密接的传播性和感染性都还未被刻画

    # exp且被感染的人->infec后，治疗期为10天到30天
    def Exposed_to_Infected(self, t):
        self.if_ever_infected = 'yes'
        self.trans = 'yes'
        r1 = rd.random()
        self.state = 'infected'
        self.healthcode = 'red'
        self.infected_time = t
        self.hosp_time = self.infected_time + 2
        t1 = rd.randint(10, 30)
        self.hosp_time_inte = t1
        self.recover_time = t1 + self.hosp_time
        # 返回恢复时间点，此点后该者不具备传播性
        return t1 + self.hosp_time
    
    def Infected_to_Recovered(self, t):
        self.trans = 'no'
        self.healthcode = 'green'
        self.state = 'recovered'

    # 在0时刻初始化一个感染者，其在五天后被送入医院
    def Init_One_Infected(self):
        self.state = 'infected'
        self.healthcode = 'red'
        self.infected_time = 0
        self.hosp_time_inte = rd.randint(10, 30)
        self.recover_time = 5 + self.hosp_time_inte
    
    def Person_Info_Update(self, t):
        if (t == self.infected_time):
            self.Exposed_to_Infected(t)
        if (t == self.recover_time):
            self.Infected_to_Recovered(t)

    # 虽然是密接或者次密接，但是其没感染病毒,在确定为次密接或者密接七天后恢复为susceptible
    def Expo_ci_Expo_to_Sus(self, t):
        if (t == self.ci_expo_expo_to_sus_time):
            self.healthcode = 'green'
            # state为susceptible, exposed, infected, recovered四种
            self.state = 'susceptible'
            # sus->expos后的潜伏时间
            self.incubation_time_inte = None
            # sus->expos的时间点
            self.incubation_time = None
            # 感染时间点
            self.infected_time = None
            # 感染后两天之内送入医院
            self.hosp_time = None
            # 感染后治疗恢复所用时间
            self.hosp_time_inte = None
            # 感染后恢复时间点
            self.recover_time = None
