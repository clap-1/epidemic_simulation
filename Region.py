
#每个区域里的信息
class Region_info(object):
    #width,length分别为区域宽和长，per_num为该区域人数
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.pers_num = 0
        self.pers_id = []
        self.pers_pos = []
    
    #返回该区域人的id
    def ret_id(self):
        return self.pers_id
    
    #向该区域加一个人
    def add_per(self, id, x = 0, y = 0):
        self.pers_id.append(id)
        self.pers_num = self.pers_num + 1
        self.pers_pos.append([x, y])
    
    #删除一个人
    def delete_per(self, id):
        #print(self.pers_id)
        index_a = self.pers_id.index(id)
        self.pers_id.remove(id)
        self.pers_num = self.pers_num - 1
        self.pers_pos.pop(index_a)
        
    #返回区域人数
    def ret_per_num(self):
        return self.pers_id
    
    def ret_pers_id(self):
        return self.pers_id
    
    def ret_pers_pos(self):
        return self.pers_pos
    
    def update_pos(self, id, x, y):
        index = self.pers_id.index(id)
        self.pers_pos[index] = [x, y]