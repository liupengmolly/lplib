import pandas as pd
import numpy as np
from scipy.spatial.distance import *

class Wifi:
    """
    对单个wifi的描述
    """
    def __init__(self,id,strength,if_connect):
        """
        初始化函数，初始化wifi的属性

        :param id:
        :param strength: 信号强度，为负值，值越大表示信号越强
        :param if_connect: 该wifi是否被连接，通常有一个场景
        """
        self.id=id
        self.strength=strength
        self.if_connect=if_connect



class Wifi_Vector:
    """
    若干个wifi组成的向量,初始化元素是字典，但所有所有的计算都是
    转化为ndarrays,利用scripy计算
    """
    def __init__(self,wifis):
        """
        初始化，其中wifis是经过预处理的：
            去除该商场从未出现过的wifi,这里从未出现过指的是在mall记录的字典中，
            可能该wifi出现过1次，但如果记录只取大于一次的，也视为没出现
        :param wifis: 允许是嵌套列表（[[wifi_id,signal_strength],...])
                        或字典形式（{wifi_id:signal_strength,...})
        """
        self.wifis=wifis if type(wifis)==list else list(wifis.items())
        self.wifi_ids=[w[0] for w in self.wifis] #先用列表固定好key的顺序，从而保证wifi向量的匹配
        self.vector=np.array([w[1] for w in self.wifis]).astype('float64')
        self.length=len(self.wifis)


    def dis_euc(self,wifis_dict):
        """
        计算与wifis_dict的欧氏距离
        :param wifis_dict:
        :return:
        """
        if self.length==0:
            return 999999
        wifis_vector=self.valid_wifis(wifis_dict)
        return euclidean(self.vector,wifis_vector)

    def dis_mah(self,wifis_dict):
        """
        计算与wifis_dict的曼哈顿距离
        :param wifis_dict:
        :return:
        """
        if self.length==0:
            return 999999
        wifis_vector=self.valid_wifis(wifis_dict)
        return cityblock(self.vector, wifis_vector)

    def dis_cos(self,wifis_dict):
        """
        计算与wifis_dict的欧氏距离
        :param wifis_dict:
        :return:
        """
        if self.length==0:
            return 999999
        wifis_vector=self.valid_wifis(wifis_dict)
        return cosine(self.vector,wifis_vector)

    def dis_cheb(self,wifis_dict):
        """
        计算与wifis_dict的契比雪夫距离
        :param wifis_dict:
        :return:
        """
        if self.length==0:
            return 999999
        wifis_vector=self.valid_wifis(wifis_dict)
        return chebyshev(self.vector,wifis_vector)

    def valid_wifis(self,wifis_dict):
        """
        返回wifis_dict对应与对象wifi的有效向量，缺失值默认-128

        :param wifis_dict:
        :return:
        """
        wifis_list=[wifis_dict[k] if k in wifis_dict else -128 for k in self.wifi_ids]
        return np.array(wifis_list).astype('float64')

    def dis_weight_euc(self,wifis_dict,wifis_rate):
        """
        计算加权欧氏距离

        :param wifis:
        :param rate_detects_wifi_shop: 每个wifi下能被检测到的shop的权重
        :param shop:
        :return:
        """
        if self.length==0:
            return 999999
        wifis_vector=self.valid_wifis(wifis_dict)

        max_rate=(max(wifis_rate.values()) if len(wifis_rate)>0 else 1)
        wifis_rate_list=[wifis_rate[k] if k in wifis_rate else max_rate for k in self.wifi_ids]
        sum_rate=sum(wifis_rate_list)
        wifis_rate_norm=np.array([v/sum_rate for v in wifis_rate_list]).astype('float64')

        # wifis_vector=wifis_vector*wifis_rate_norm
        return euclidean(self.vector,wifis_vector)