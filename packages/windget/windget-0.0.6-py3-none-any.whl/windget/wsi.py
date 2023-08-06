#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from WindPy import w
def convertInputSecurityTypeForWsi(func):
    def convertedFunc(*args):
        args = tuple((i.strftime("%Y-%m-%d %H:%M:%S") if hasattr(i,"strftime") else i for i in args))
        if type(args[0])==type(''):
            return func(*args)[1].fillna(np.nan)
        else:
            security = args[0]
            args = args[1:]
            return func(",".join(security),*args)[1].fillna(np.nan)
    return convertedFunc
@convertInputSecurityTypeForWsi
def getOpenWsi(security:list,*args,**kwargs):
    # 获取开盘价分钟序列
    return w.wsi(security,"open",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getHighWsi(security:list,*args,**kwargs):
    # 获取最高价分钟序列
    return w.wsi(security,"high",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getLowWsi(security:list,*args,**kwargs):
    # 获取最低价分钟序列
    return w.wsi(security,"low",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getCloseWsi(security:list,*args,**kwargs):
    # 获取收盘价分钟序列
    return w.wsi(security,"close",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getVolumeWsi(security:list,*args,**kwargs):
    # 获取成交量分钟序列
    return w.wsi(security,"volume",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getAmtWsi(security:list,*args,**kwargs):
    # 获取成交额分钟序列
    return w.wsi(security,"amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getChgWsi(security:list,*args,**kwargs):
    # 获取涨跌分钟序列
    return w.wsi(security,"chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getPctChgWsi(security:list,*args,**kwargs):
    # 获取涨跌幅分钟序列
    return w.wsi(security,"pct_chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getOiWsi(security:list,*args,**kwargs):
    # 获取持仓量分钟序列
    return w.wsi(security,"oi",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getBeginTimeWsi(security:list,*args,**kwargs):
    # 获取开始时间分钟序列
    return w.wsi(security,"begin_time",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getEndTimeWsi(security:list,*args,**kwargs):
    # 获取结束时间分钟序列
    return w.wsi(security,"end_time",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getBiasWsi(security:list,*args,**kwargs):
    # 获取BIAS乖离率分钟序列
    return w.wsi(security,"BIAS",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getBollWsi(security:list,*args,**kwargs):
    # 获取BOLL布林带分钟序列
    return w.wsi(security,"BOLL",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getDMiWsi(security:list,*args,**kwargs):
    # 获取DMI趋向标准分钟序列
    return w.wsi(security,"DMI",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getExpMaWsi(security:list,*args,**kwargs):
    # 获取EXPMA指数平滑移动平均分钟序列
    return w.wsi(security,"EXPMA",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getHvWsi(security:list,*args,**kwargs):
    # 获取HV历史波动率分钟序列
    return w.wsi(security,"HV",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getKDjWsi(security:list,*args,**kwargs):
    # 获取KDJ随机指标分钟序列
    return w.wsi(security,"KDJ",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getMaWsi(security:list,*args,**kwargs):
    # 获取MA简单移动平均分钟序列
    return w.wsi(security,"MA",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getMacDWsi(security:list,*args,**kwargs):
    # 获取MACD指数平滑异同平均分钟序列
    return w.wsi(security,"MACD",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsi
def getRsiWsi(security:list,*args,**kwargs):
    # 获取RSI相对强弱指标分钟序列
    return w.wsi(security,"RSI",*args,**kwargs,usedf=True)