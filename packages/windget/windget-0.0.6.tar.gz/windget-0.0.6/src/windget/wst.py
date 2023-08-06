#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from WindPy import w
def convertInputSecurityTypeForWst(func):
    def convertedFunc(*args):
        args = tuple((i.strftime("%Y-%m-%d %H:%M:%S") if hasattr(i,"strftime") else i for i in args))
        if type(args[0])==type(''):
            return func(*args)[1].fillna(np.nan)
        else:
            security = args[0]
            args = args[1:]
            return func(",".join(security),*args)[1].fillna(np.nan)
    return convertedFunc
@convertInputSecurityTypeForWst
def getPreCloseWst(security:list,*args,**kwargs):
    # 获取前收盘价日内跳价
    return w.wst(security,"pre_close",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getOpenWst(security:list,*args,**kwargs):
    # 获取开盘价日内跳价
    return w.wst(security,"open",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getHighWst(security:list,*args,**kwargs):
    # 获取最高价日内跳价
    return w.wst(security,"high",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getLowWst(security:list,*args,**kwargs):
    # 获取最低价日内跳价
    return w.wst(security,"low",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getLastWst(security:list,*args,**kwargs):
    # 获取最新价日内跳价
    return w.wst(security,"last",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAskWst(security:list,*args,**kwargs):
    # 获取卖价日内跳价
    return w.wst(security,"ask",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBidWst(security:list,*args,**kwargs):
    # 获取买价日内跳价
    return w.wst(security,"bid",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getVolumeWst(security:list,*args,**kwargs):
    # 获取成交量日内跳价
    return w.wst(security,"volume",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAmtWst(security:list,*args,**kwargs):
    # 获取成交额日内跳价
    return w.wst(security,"amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getPreSettleWst(security:list,*args,**kwargs):
    # 获取前结算价日内跳价
    return w.wst(security,"pre_settle",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getSettleWst(security:list,*args,**kwargs):
    # 获取结算价日内跳价
    return w.wst(security,"settle",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getPreOiWst(security:list,*args,**kwargs):
    # 获取前持仓量日内跳价
    return w.wst(security,"pre_oi",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getOiWst(security:list,*args,**kwargs):
    # 获取持仓量日内跳价
    return w.wst(security,"oi",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getVolRatioWst(security:list,*args,**kwargs):
    # 获取量比日内跳价
    return w.wst(security,"vol_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAfterPriceWst(security:list,*args,**kwargs):
    # 获取盘后最新成交价日内跳价
    return w.wst(security,"afterprice",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAfterVolumeWst(security:list,*args,**kwargs):
    # 获取盘后成交量日内跳价
    return w.wst(security,"aftervolume",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAfterTurnoverWst(security:list,*args,**kwargs):
    # 获取盘后成交额日内跳价
    return w.wst(security,"afterturnover",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk10Wst(security:list,*args,**kwargs):
    # 获取卖10价日内跳价
    return w.wst(security,"ask10",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk9Wst(security:list,*args,**kwargs):
    # 获取卖9价日内跳价
    return w.wst(security,"ask9",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk8Wst(security:list,*args,**kwargs):
    # 获取卖8价日内跳价
    return w.wst(security,"ask8",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk7Wst(security:list,*args,**kwargs):
    # 获取卖7价日内跳价
    return w.wst(security,"ask7",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk6Wst(security:list,*args,**kwargs):
    # 获取卖6价日内跳价
    return w.wst(security,"ask6",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk5Wst(security:list,*args,**kwargs):
    # 获取卖5价日内跳价
    return w.wst(security,"ask5",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk4Wst(security:list,*args,**kwargs):
    # 获取卖4价日内跳价
    return w.wst(security,"ask4",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk3Wst(security:list,*args,**kwargs):
    # 获取卖3价日内跳价
    return w.wst(security,"ask3",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk2Wst(security:list,*args,**kwargs):
    # 获取卖2价日内跳价
    return w.wst(security,"ask2",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getAsk1Wst(security:list,*args,**kwargs):
    # 获取卖1价日内跳价
    return w.wst(security,"ask1",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid1Wst(security:list,*args,**kwargs):
    # 获取买1价日内跳价
    return w.wst(security,"bid1",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid2Wst(security:list,*args,**kwargs):
    # 获取买2价日内跳价
    return w.wst(security,"bid2",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid3Wst(security:list,*args,**kwargs):
    # 获取买3价日内跳价
    return w.wst(security,"bid3",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid4Wst(security:list,*args,**kwargs):
    # 获取买4价日内跳价
    return w.wst(security,"bid4",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid8Wst(security:list,*args,**kwargs):
    # 获取买8价日内跳价
    return w.wst(security,"bid8",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid9Wst(security:list,*args,**kwargs):
    # 获取买9价日内跳价
    return w.wst(security,"bid9",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid10Wst(security:list,*args,**kwargs):
    # 获取买10价日内跳价
    return w.wst(security,"bid10",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize10Wst(security:list,*args,**kwargs):
    # 获取卖10量日内跳价
    return w.wst(security,"asize10",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize9Wst(security:list,*args,**kwargs):
    # 获取卖9量日内跳价
    return w.wst(security,"asize9",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize8Wst(security:list,*args,**kwargs):
    # 获取卖8量日内跳价
    return w.wst(security,"asize8",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize7Wst(security:list,*args,**kwargs):
    # 获取卖7量日内跳价
    return w.wst(security,"asize7",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize6Wst(security:list,*args,**kwargs):
    # 获取卖6量日内跳价
    return w.wst(security,"asize6",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize5Wst(security:list,*args,**kwargs):
    # 获取卖5量日内跳价
    return w.wst(security,"asize5",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize4Wst(security:list,*args,**kwargs):
    # 获取卖4量日内跳价
    return w.wst(security,"asize4",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize3Wst(security:list,*args,**kwargs):
    # 获取卖3量日内跳价
    return w.wst(security,"asize3",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize2Wst(security:list,*args,**kwargs):
    # 获取卖2量日内跳价
    return w.wst(security,"asize2",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getASize1Wst(security:list,*args,**kwargs):
    # 获取卖1量日内跳价
    return w.wst(security,"asize1",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize1Wst(security:list,*args,**kwargs):
    # 获取买1量日内跳价
    return w.wst(security,"bsize1",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize2Wst(security:list,*args,**kwargs):
    # 获取买2量日内跳价
    return w.wst(security,"bsize2",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize3Wst(security:list,*args,**kwargs):
    # 获取买3量日内跳价
    return w.wst(security,"bsize3",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize4Wst(security:list,*args,**kwargs):
    # 获取买4量日内跳价
    return w.wst(security,"bsize4",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize5Wst(security:list,*args,**kwargs):
    # 获取买5量日内跳价
    return w.wst(security,"bsize5",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize6Wst(security:list,*args,**kwargs):
    # 获取买6量日内跳价
    return w.wst(security,"bsize6",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize7Wst(security:list,*args,**kwargs):
    # 获取买7量日内跳价
    return w.wst(security,"bsize7",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize8Wst(security:list,*args,**kwargs):
    # 获取买8量日内跳价
    return w.wst(security,"bsize8",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize9Wst(security:list,*args,**kwargs):
    # 获取买9量日内跳价
    return w.wst(security,"bsize9",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBSize10Wst(security:list,*args,**kwargs):
    # 获取买10量日内跳价
    return w.wst(security,"bsize10",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getIoPvWst(security:list,*args,**kwargs):
    # 获取IOPV日内跳价
    return w.wst(security,"iopv",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getLimitUpWst(security:list,*args,**kwargs):
    # 获取涨停价日内跳价
    return w.wst(security,"limit_up",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getLimitDownWst(security:list,*args,**kwargs):
    # 获取跌停价日内跳价
    return w.wst(security,"limit_down",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid5Wst(security:list,*args,**kwargs):
    # 获取买5价日内跳价
    return w.wst(security,"bid5",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid6Wst(security:list,*args,**kwargs):
    # 获取买6价日内跳价
    return w.wst(security,"bid6",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWst
def getBid7Wst(security:list,*args,**kwargs):
    # 获取买7价日内跳价
    return w.wst(security,"bid7",*args,**kwargs,usedf=True)