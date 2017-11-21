import joblib
import os
import pandas as pd

def load_vars(*args,**kwargs):
    """
    加载制定文件名的缓存文件为对象

    :param args:
    :param kwargs:
        dir:缓存文件的目录
        names:缓存文件名
    :return:一定要注意返回的是对象元组
    """
    dir_path=kwargs['dir']
    names=kwargs['names']
    ret_vars=[]
    for name in names:
        ret_vars.append(joblib.load(os.path.join(dir_path,name)))
    return ret_vars

def to_csv(*args,**kwargs):
    """
    将指定名字的缓存文件转化为csv文件

    :param args:
    :param kwargs:
        load_dir:函数load_vars加载缓存文件的目录
        dump_dir:最终转化的csv文件存储目录
        names:要加载的缓存文件名（也是存储的csv文件名）
        if_df:要转存的缓存文件load后的对象是否是DataFrame格式，默认为Series格式
    :return:
    """
    results= load_vars(dir=kwargs['load_dir'],names=kwargs['names'])
    if 'if_df' in kwargs and kwargs['if_df']==1:
        for i in range(len(kwargs['names'])):
            pd.DataFrame(results[i]).to_csv(os.path.join(kwargs['dump_dir'],kwargs['names'][i]+'.csv'))
    else:
        for i in range(len(kwargs['names'])):
            pd.Series(results[i]).to_csv(os.path.join(kwargs['dump_dir'],kwargs['names'][i]+'.csv'))
    print(','.join(kwargs['names'])+'已经全部另存为csv文件')
