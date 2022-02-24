
#每个区域里的信息
class Region_info(object):
    #width,length分别为区域宽和长，per_num为该区域人数
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.pers_num = 0
        self.pers_id = []
    
    #返回该区域人的id
    def ret_id(self):
        return self.pers_id
    
    #向该区域加一个人
    def add_per(self, id):
        self.pers_id.append(id)
        self.pers_num = self.pers_num + 1
    
    #删除一个人
    def delete_per(self, id):
        self.pers_id.remove(id)
        self.pers_num = self.pers_num - 1
        
    #返回区域人数
    def ret_per_num(self):
        return self.pers_id