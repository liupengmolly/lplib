from sklearn.externals import joblib
import os
import pickle
"""
Attention:
    尽量用函数的参数取代装饰器本身的参数，这样能方便的根据不同的情况在调用函数时更改参数
    假如使用装饰器自带的参数，则是固定的，需要调整时只能去修改函数本身程序
"""

def cache_dump(func):
    """
    对函数返回值进行缓存的装饰器，装饰器功能依耐于函数的kwargs参数
    kwargs['names']:函数返回值缓存文件的名字
    kwargs['dir']:缓存文件的目录路径

    Attention:
        被装饰函数不能返回单个元组

    :param func:
    :return:
    """
    def wrapper(*args,**kwargs):
        if 'names' in kwargs:
            vars_to_cache=func(*args,**kwargs)
            #如果只是返回一个变量，既不是元组，则下面第四行遍历时会把对象拆开,所以需在外面加一层列表，此外，为防止混淆，被装饰函数尽量不要返回单个的元组
            vars_to_cache_list=[vars_to_cache] if type(vars_to_cache)!=tuple else vars_to_cache
            names=kwargs['names']
            for var,name in zip(vars_to_cache_list,names):
                joblib.dump(var,os.path.join(kwargs['dir'],name))
                # file=open(os.path.join(kwargs['dir'],name),'wb')
                # pickle.dump(var,file,1)
            return vars_to_cache
        else:
            return func(*args,**kwargs)
    return wrapper





