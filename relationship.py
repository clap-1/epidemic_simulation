'''
用于记录agent之间的家庭关系
'''
class family(object):
    #初始化
    def __init__(self, id):
        self.family_mem = []
        self.family_id = None
    
    def add_mem(self, person_id):
        '''
        :param relation_info: 只有两种relationship: family or colleague
        :return:
        '''
        self.family_mem.append(person_id)
    
    def ret_family_mem(self):
        return self.family_mem


'''
用于记录agent之间的校园关系
'''
class class_a(object):
    # 初始化
    def __init__(self, id):
        self.class_mem = []
        self.class_id = None
    
    def add_mem(self, person_id):
        self.class_mem.append(person_id)
    
    def ret_class_mem(self):
        return self.class_mem


'''
用于记录agent之间的同事关系
'''
class team(object):
    # 初始化
    def __init__(self, id):
        self.team_mem = []
        self.team_id = None
    
    def add_mem(self, person_id):
        self.team_mem.append(person_id)
    
    def ret_team_mem(self):
        return self.team_mem
        

            
    