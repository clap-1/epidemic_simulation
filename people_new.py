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
        #密接等级
        self.CC_level = None
        #成为exposed或者成为infected的源头，即感染此人的患者的id
        self.affected_by = None
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
        # 被隔离的时间
        self.quarantine_time = None
        # 出隔离的时间
        self.out_quarantine_time = None
        
    
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
        if (len(self.went_reg) >= 14*14):
            l1 = self.went_reg[-(14*14):-1]
            self.travel_rec = l1.copy()
            self.travel_rec = list(set(self.travel_rec))
        else:
            self.travel_rec = list(set(self.went_reg))
        return self.travel_rec
    
    # 返回行程卡
    def ret_went_reg(self):
        return self.went_reg
    
    # 下一刻的region及坐标,传入参数为当前region
    def change_pos(self, iregion, age, region):
        if(iregion == 4 or iregion == 5):
            self.add_went_reg(iregion)
            return
        prob = pos_change_rate(age)
        region_change_rate = prob[0]
        coordinate_change_rate = prob[1]
        region_change = rd.random()
        # 如果该person目前正在3区域，那么他如果区域改变的话，只能回家，只能变换到1
        if (region_change <= region_change_rate):
            if(iregion == 3):
                reg_new = 0
                self.add_went_reg(reg_new)
                self.region = reg_new
                region[reg_new].add_per(self.id)
                region[iregion].delete_per(self.id)
            elif(iregion == 0 or iregion == 1
                 or iregion == 2):
                reg_new = 3
                region[self.region].delete_per(self.id)
                self.add_went_reg(reg_new)
                self.region = reg_new
                x = rd.uniform(0, region_width)
                y = rd.uniform(0, region_length)
                # 下一刻的坐标
                self.x = x
                self.y = y
                region[reg_new].add_per(self.id, x, y)
        else:
            self.add_went_reg(iregion)
            if (iregion == 3):
                coordinate_change = rd.random()
                if (coordinate_change <= coordinate_change_rate):
                    x = rd.uniform(0, region_width)
                    y = rd.uniform(0, region_length)
                    # 下一刻的坐标
                    self.x = x
                    self.y = y
                    region[iregion].update_pos(self.id, x, y)
            

    # sus->exposed后,潜伏期为2-7天，传入参数为此转换的时间,与感染者接触后成为密接
    def Sus_to_Exposed(self, t, id, Persons, age):
        self.state = 'exposed'
        self.affected_by = id
        r1 = rd.random()
        if (r1 <= infetcd_c(age)):
            Persons[id].Repro_num = Persons[id].Repro_num + 1
            t1 = rd.randint(2*14, 7*14)
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
            t1 = rd.randint(2*14, 14*14)
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

    # exp且被感染的人->infec后，治疗期为5天到10天
    def Exposed_to_Infected(self, t):
        self.if_ever_infected = 'yes'
        self.trans = 'yes'
        r1 = rd.random()
        self.state = 'infected'
        self.healthcode = 'red'
        self.infected_time = t
        self.hosp_time = self.infected_time + 2*14
        t1 = rd.randint(5*14, 10*14)
        self.hosp_time_inte = t1
        n = (t1 + self.hosp_time)//14
        if ((t1 + self.hosp_time)%14 == 0):
            self.recover_time = n * 14
        else:
            self.recover_time = (n+1) * 14
        # 返回恢复时间点，此点后该者不具备传播性
        return self.recover_time
    
    def Infected_to_Recovered(self, t):
        self.trans = 'no'
        self.healthcode = 'green'
        self.state = 'recovered'

    # 在0时刻初始化一个感染者，其在五天后被送入医院
    def Init_One_Infected(self):
        self.state = 'infected'
        self.healthcode = 'red'
        self.if_ever_infected = 'yes'
        self.infected_time = 0
        self.hosp_time_inte = rd.randint(5*14, 10*14)
        self.hosp_time = 2*14
        n = (self.hosp_time + self.hosp_time_inte) // 14
        if ((self.hosp_time + self.hosp_time_inte) % 14 == 0):
            self.recover_time = n * 14
        else:
            self.recover_time = (n + 1) * 14
    
    #隔离
    def quarantine(self, region, t):
        #放入一个区域隔离，不再能自由活动
        region[self.region].delete_per(self.id)
        self.region = 4
        self.add_went_reg(self.region)
        region[self.region].add_per(self.id)
        self.state = 'close-contact'
        self.quarantine_time = t
        #隔离期为5天
        n = (t + 5*14)//14
        if ((t + 5*14)%14==0):
            self.out_quarantine_time = n*14
        else:
            self.out_quarantine_time = (n+1) * 14
        
    def out_quarantine(self, region):
        region[self.region].delete_per(self.id)
        self.region = 0
        self.add_went_reg(self.region)
        region[self.region].add_per(self.id)
        self.state = 'susceptible'
        
    #入院
    def hospital(self, region):
        region[self.region].delete_per(self.id)
        self.region = 5
        self.add_went_reg(self.region)
        region[self.region].add_per(self.id)
        self.out_quarantine_time = None
        self.state = 'hospital'
        
    #出院
    def out_hospital(self, region):
        region[5].delete_per(self.id)
        self.region = 0
        self.add_went_reg(self.region)
        region[self.region].add_per(self.id)
        self.state = 'recovered'
        
    #密接进入医院
    def CC_hospital(self, t, region):
        if(self.state == 'close-contact'):
            if (self.hosp_time == t):
                self.if_ever_infected = 'yes'
                self.trans = 'yes'
                self.state = 'hospital'
                self.healthcode = 'red'
                t1 = rd.randint(5 * 14, 10 * 14)
                self.hosp_time_inte = t1
                n = (t1 + self.hosp_time) // 14
                if ((t1 + self.hosp_time) % 14 == 0):
                    self.recover_time = n * 14
                else:
                    self.recover_time = (n + 1) * 14
                region[self.region].delete_per(self.id)
                self.region = 5
                self.add_went_reg(self.region)
                region[self.region].add_per(self.id)
                self.out_quarantine_time = None
                
        
    #每次时间更新，信息更新
    def Person_Info_Update(self, t, day, age, Family, Class, Team, Persons, region):
        # if(t >28 and t<50 and self.id == 3000):
        #     print(self.state)
        self.CC_hospital(t, region)
        if(self.state != 'close-contact' and self.state != 'hospital'):
            if (day != 6 and day != 7):
                if (t%14 >= 0 and t%14 <= 9):
                    if (age <= 20):
                        temp = self.region
                        self.region = 2
                        self.add_went_reg(self.region)
                        region[self.region].add_per(self.id)
                        region[temp].delete_per(self.id)
                    elif (age > 20 and age <=60):
                        temp = self.region
                        self.region = 1
                        self.add_went_reg(self.region)
                        region[self.region].add_per(self.id)
                        region[temp].delete_per(self.id)
            if (t%14 == 0):
                temp = self.region
                self.region = 0
                region[self.region].add_per(self.id)
                region[temp].delete_per(self.id)
                self.add_went_reg(self.region)
        if (t == self.infected_time):
            self.Exposed_to_Infected(t)
            #隔离，若其状态已经infected，则不被隔离
            family_id = self.family_id
            for k in Family[family_id].ret_family_mem():
                if(Persons[k].ret_state() != 'infected' and
                   Persons[k].ret_state() != 'hospital' and
                   Persons[k].ret_state() != 'close-contact' and
                   k != self.id):
                    Persons[k].quarantine(region, t)
                    Persons[k].CC_level_change(1)
            if (self.class_id != None):
                class_id = self.class_id
                for k in Class[class_id].ret_class_mem():
                    if (Persons[k].ret_state() != 'infected' and
                        Persons[k].ret_state() != 'hospital' and
                        Persons[k].ret_state() != 'close-contact' and
                        k != self.id):
                        Persons[k].quarantine(region, t)
                        Persons[k].CC_level_change(1)
            if (self.business_id != None):
                busi_id = self.business_id
                for k in Team[busi_id].ret_team_mem():
                    if (Persons[k].ret_state() != 'infected' and
                        Persons[k].ret_state() != 'hospital' and
                        Persons[k].ret_state() != 'close-contact' and
                        k != self.id):
                        Persons[k].quarantine(region, t)
                        Persons[k].CC_level_change(1)
        if (t == self.hosp_time):
            self.hospital(region)
        if (t == self.recover_time):
            self.out_hospital(region)
            self.Infected_to_Recovered(t)
        if (t == self.out_quarantine_time):
            #if (self.state == 'close-contact'):
            self.out_quarantine(region)

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
    
    def CC_level_change(self, level):
        if (self.CC_level == None):
            self.CC_level = level
        else:
            if (self.CC_level > level):
                self.CC_level = level
            