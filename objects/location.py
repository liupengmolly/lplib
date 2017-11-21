from math import radians,cos,sin,asin,sqrt,atan,acos,tan,atan2,degrees

class Location:
    """
    对用户位置处理的工具类
    """

    def __init__(self,latitude,longitude):
        """
        初始化，赋值经度和纬度

        Args:
            longitude:经度
            latitude:纬度
        """
        self.longitude=longitude
        self.latitude=latitude


    def get_distance(self,loc):
        """
        haversine方法得到与loc之间的距离

        :param loc: 另一位置
        :return:
        """
        lon1, lat1, lon2, lat2 = map(radians, [self.longitude, self.latitude,
                                loc.longitude,loc.latitude])

        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a)) if a!=0.0 else 0.0
        r = 6371393
        return c * r

    def get_degree(self,loc):
        """
        得到loc相当于自身的角度

        :param loc:
        :return:
        """
        radLatA = radians(self.latitude)
        radLonA = radians(self.longitude)
        radLatB = radians(loc.latitude)
        radLonB = radians(loc.longitude)
        dLon = radLonB - radLonA
        y = sin(dLon) * cos(radLatB)
        x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
        brng = degrees(atan2(y, x))
        brng = (brng + 360) % 360
        return brng

    def get_nearest_shop_id(self,shops):
        """
        返回曼哈顿最近距离的商铺id

        :param shops:所有商店的信息的DataFrame
        :return:
        """
        shops['bias_lon']=abs(shops['longitude']-self.longitude)
        shops['bias_lat']=abs(shops['latitude']-self.latitude)
        shops['mah_dist']=shops['bias_lon']+shops['bias_lat']
        return shops.sort_values('mah_dist')[0:1]['shop_id'].values[0]

    def get_nearest_shops_id(self,num,shops):
        """
        返回曼哈顿最近距离的num个商铺的id
        Attention:
            默认shops已将shop_id设置为index

        :param shops:所有商店的信息的DataFrame
        :return:
        """
        shops['bias_lon']=abs(shops['longitude']-self.longitude)
        shops['bias_lat']=abs(shops['latitude']-self.latitude)
        shops['mah_dist']=shops['bias_lon']+shops['bias_lat']
        return shops.sort_values('mah_dist')[0:num].index.values
