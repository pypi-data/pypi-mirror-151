#分层抽样 抽样最优分配
import math
import numpy as np
class fenceng:                    #定义类
    def __init__(self,name):
        self.name=name
def hanshu(n1,n2,n3,var1,var2,var3,exp1,exp2,exp3,r):     #定义函数
#求出总的计划样本容量 三个加一起乘上0.1
        n=(n1+n2+n3)*r
        Nh=[n1,n2,n3]
        Sh=[math.sqrt(var1),math.sqrt(var2),math.sqrt(var3)]   #标准差
        NhSh=np.multiply(Nh,Sh)     #列表之间对应位置相乘 求出NhSh
        a=NhSh[0]/math.sqrt(exp1)   #求每一层的分子
        b=NhSh[1]/math.sqrt(exp2)
        c=NhSh[2]/math.sqrt(exp3)
        u=a+b+c          #算每一层的时候分母是相同的 是一个求和
        x1=round(n*a/u)   #第一层最优数
        x2=round(n*b/u)
        x3=round(n*c/u)
        print(x1,x2,x3)
fenceng.hanshu(299,303,306,92,103,81,76,88,82,0.1)   #调用函数 返回结果