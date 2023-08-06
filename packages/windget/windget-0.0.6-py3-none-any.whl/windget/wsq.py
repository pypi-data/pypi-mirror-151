#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from WindPy import w
def convertInputSecurityTypeForWsq(func):
    def convertedFunc(*args):
        args = tuple((i.strftime("%Y-%m-%d") if hasattr(i,"strftime") else i for i in args))
        if type(args[0])==type(''):
            return func(*args)[1].fillna(np.nan)
        else:
            security = args[0]
            args = args[1:]
            return func(",".join(security),*args)[1].fillna(np.nan)
    return convertedFunc
@convertInputSecurityTypeForWsq
def getRtDateWsq(security:list,*args,**kwargs):
    # 获取日期实时行情
    return w.wsq(security,"rt_date",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtTimeWsq(security:list,*args,**kwargs):
    # 获取时间实时行情
    return w.wsq(security,"rt_time",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPreCloseWsq(security:list,*args,**kwargs):
    # 获取前收实时行情
    return w.wsq(security,"rt_pre_close",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOpenWsq(security:list,*args,**kwargs):
    # 获取今开实时行情
    return w.wsq(security,"rt_open",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtHighWsq(security:list,*args,**kwargs):
    # 获取最高实时行情
    return w.wsq(security,"rt_high",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLowWsq(security:list,*args,**kwargs):
    # 获取最低实时行情
    return w.wsq(security,"rt_low",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLastWsq(security:list,*args,**kwargs):
    # 获取现价实时行情
    return w.wsq(security,"rt_last",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLastAmtWsq(security:list,*args,**kwargs):
    # 获取现额实时行情
    return w.wsq(security,"rt_last_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLastVolWsq(security:list,*args,**kwargs):
    # 获取现量实时行情
    return w.wsq(security,"rt_last_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLatestWsq(security:list,*args,**kwargs):
    # 获取最新成交价实时行情
    return w.wsq(security,"rt_latest",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVolWsq(security:list,*args,**kwargs):
    # 获取成交量实时行情
    return w.wsq(security,"rt_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAmtWsq(security:list,*args,**kwargs):
    # 获取成交额实时行情
    return w.wsq(security,"rt_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtChgWsq(security:list,*args,**kwargs):
    # 获取涨跌实时行情
    return w.wsq(security,"rt_chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChgWsq(security:list,*args,**kwargs):
    # 获取涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtHighLimitWsq(security:list,*args,**kwargs):
    # 获取涨停价实时行情
    return w.wsq(security,"rt_high_limit",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLowLimitWsq(security:list,*args,**kwargs):
    # 获取跌停价实时行情
    return w.wsq(security,"rt_low_limit",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPreLatestWsq(security:list,*args,**kwargs):
    # 获取盘前最新价实时行情
    return w.wsq(security,"rt_pre_latest",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtSwingWsq(security:list,*args,**kwargs):
    # 获取振幅实时行情
    return w.wsq(security,"rt_swing",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVWapWsq(security:list,*args,**kwargs):
    # 获取均价实时行情
    return w.wsq(security,"rt_vwap",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtUpwardVolWsq(security:list,*args,**kwargs):
    # 获取外盘实时行情
    return w.wsq(security,"rt_upward_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtDownwardVolWsq(security:list,*args,**kwargs):
    # 获取内盘实时行情
    return w.wsq(security,"rt_downward_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMinSpreadWsq(security:list,*args,**kwargs):
    # 获取最小价差实时行情
    return w.wsq(security,"rt_min_spread",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtTradeStatusWsq(security:list,*args,**kwargs):
    # 获取交易状态实时行情
    return w.wsq(security,"rt_trade_status",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtHigh52WKWsq(security:list,*args,**kwargs):
    # 获取52周最高实时行情
    return w.wsq(security,"rt_high_52wk",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLow52WKWsq(security:list,*args,**kwargs):
    # 获取52周最低实时行情
    return w.wsq(security,"rt_low_52wk",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg1MinWsq(security:list,*args,**kwargs):
    # 获取1分钟涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_1min",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg3MinWsq(security:list,*args,**kwargs):
    # 获取3分钟涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_3min",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg5MinWsq(security:list,*args,**kwargs):
    # 获取5分钟涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_5min",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg5DWsq(security:list,*args,**kwargs):
    # 获取5日涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_5d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg10DWsq(security:list,*args,**kwargs):
    # 获取10日涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_10d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg20DWsq(security:list,*args,**kwargs):
    # 获取20日涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_20d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg60DWsq(security:list,*args,**kwargs):
    # 获取60日涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_60d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg120DWsq(security:list,*args,**kwargs):
    # 获取120日涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_120d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChg250DWsq(security:list,*args,**kwargs):
    # 获取250日涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_250d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPctChgYTdWsq(security:list,*args,**kwargs):
    # 获取年初至今涨跌幅实时行情
    return w.wsq(security,"rt_pct_chg_ytd",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk1Wsq(security:list,*args,**kwargs):
    # 获取卖1价实时行情
    return w.wsq(security,"rt_ask1",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk2Wsq(security:list,*args,**kwargs):
    # 获取卖2价实时行情
    return w.wsq(security,"rt_ask2",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk3Wsq(security:list,*args,**kwargs):
    # 获取卖3价实时行情
    return w.wsq(security,"rt_ask3",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk4Wsq(security:list,*args,**kwargs):
    # 获取卖4价实时行情
    return w.wsq(security,"rt_ask4",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk5Wsq(security:list,*args,**kwargs):
    # 获取卖5价实时行情
    return w.wsq(security,"rt_ask5",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk6Wsq(security:list,*args,**kwargs):
    # 获取卖6价实时行情
    return w.wsq(security,"rt_ask6",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk7Wsq(security:list,*args,**kwargs):
    # 获取卖7价实时行情
    return w.wsq(security,"rt_ask7",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk8Wsq(security:list,*args,**kwargs):
    # 获取卖8价实时行情
    return w.wsq(security,"rt_ask8",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk9Wsq(security:list,*args,**kwargs):
    # 获取卖9价实时行情
    return w.wsq(security,"rt_ask9",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk10Wsq(security:list,*args,**kwargs):
    # 获取卖10价实时行情
    return w.wsq(security,"rt_ask10",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid1Wsq(security:list,*args,**kwargs):
    # 获取买1价实时行情
    return w.wsq(security,"rt_bid1",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid2Wsq(security:list,*args,**kwargs):
    # 获取买2价实时行情
    return w.wsq(security,"rt_bid2",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid3Wsq(security:list,*args,**kwargs):
    # 获取买3价实时行情
    return w.wsq(security,"rt_bid3",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid4Wsq(security:list,*args,**kwargs):
    # 获取买4价实时行情
    return w.wsq(security,"rt_bid4",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid5Wsq(security:list,*args,**kwargs):
    # 获取买5价实时行情
    return w.wsq(security,"rt_bid5",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid6Wsq(security:list,*args,**kwargs):
    # 获取买6价实时行情
    return w.wsq(security,"rt_bid6",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid7Wsq(security:list,*args,**kwargs):
    # 获取买7价实时行情
    return w.wsq(security,"rt_bid7",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid8Wsq(security:list,*args,**kwargs):
    # 获取买8价实时行情
    return w.wsq(security,"rt_bid8",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid9Wsq(security:list,*args,**kwargs):
    # 获取买9价实时行情
    return w.wsq(security,"rt_bid9",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid10Wsq(security:list,*args,**kwargs):
    # 获取买10价实时行情
    return w.wsq(security,"rt_bid10",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize1Wsq(security:list,*args,**kwargs):
    # 获取买1量实时行情
    return w.wsq(security,"rt_bsize1",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize2Wsq(security:list,*args,**kwargs):
    # 获取买2量实时行情
    return w.wsq(security,"rt_bsize2",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize3Wsq(security:list,*args,**kwargs):
    # 获取买3量实时行情
    return w.wsq(security,"rt_bsize3",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize4Wsq(security:list,*args,**kwargs):
    # 获取买4量实时行情
    return w.wsq(security,"rt_bsize4",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize5Wsq(security:list,*args,**kwargs):
    # 获取买5量实时行情
    return w.wsq(security,"rt_bsize5",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize6Wsq(security:list,*args,**kwargs):
    # 获取买6量实时行情
    return w.wsq(security,"rt_bsize6",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize7Wsq(security:list,*args,**kwargs):
    # 获取买7量实时行情
    return w.wsq(security,"rt_bsize7",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize8Wsq(security:list,*args,**kwargs):
    # 获取买8量实时行情
    return w.wsq(security,"rt_bsize8",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize9Wsq(security:list,*args,**kwargs):
    # 获取买9量实时行情
    return w.wsq(security,"rt_bsize9",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSize10Wsq(security:list,*args,**kwargs):
    # 获取买10量实时行情
    return w.wsq(security,"rt_bsize10",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize1Wsq(security:list,*args,**kwargs):
    # 获取卖1量实时行情
    return w.wsq(security,"rt_asize1",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize2Wsq(security:list,*args,**kwargs):
    # 获取卖2量实时行情
    return w.wsq(security,"rt_asize2",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize3Wsq(security:list,*args,**kwargs):
    # 获取卖3量实时行情
    return w.wsq(security,"rt_asize3",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize4Wsq(security:list,*args,**kwargs):
    # 获取卖4量实时行情
    return w.wsq(security,"rt_asize4",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize5Wsq(security:list,*args,**kwargs):
    # 获取卖5量实时行情
    return w.wsq(security,"rt_asize5",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize6Wsq(security:list,*args,**kwargs):
    # 获取卖6量实时行情
    return w.wsq(security,"rt_asize6",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize7Wsq(security:list,*args,**kwargs):
    # 获取卖7量实时行情
    return w.wsq(security,"rt_asize7",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize8Wsq(security:list,*args,**kwargs):
    # 获取卖8量实时行情
    return w.wsq(security,"rt_asize8",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize9Wsq(security:list,*args,**kwargs):
    # 获取卖9量实时行情
    return w.wsq(security,"rt_asize9",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASize10Wsq(security:list,*args,**kwargs):
    # 获取卖10量实时行情
    return w.wsq(security,"rt_asize10",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPostMktTimeWsq(security:list,*args,**kwargs):
    # 获取盘后时间实时行情
    return w.wsq(security,"rt_post_mkt_time",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPostMktLastVolWsq(security:list,*args,**kwargs):
    # 获取盘后现量实时行情
    return w.wsq(security,"rt_post_mkt_last_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPostMktLatestWsq(security:list,*args,**kwargs):
    # 获取盘后最新成交价实时行情
    return w.wsq(security,"rt_post_mkt_latest",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPostMktVolWsq(security:list,*args,**kwargs):
    # 获取盘后成交量实时行情
    return w.wsq(security,"rt_post_mkt_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPostMktAmtWsq(security:list,*args,**kwargs):
    # 获取盘后成交额实时行情
    return w.wsq(security,"rt_post_mkt_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPostMktChgWsq(security:list,*args,**kwargs):
    # 获取盘后涨跌实时行情
    return w.wsq(security,"rt_post_mkt_chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPostMktPctChgWsq(security:list,*args,**kwargs):
    # 获取盘后涨跌幅实时行情
    return w.wsq(security,"rt_post_mkt_pct_chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPostMktDealNumWsq(security:list,*args,**kwargs):
    # 获取盘后成交笔数实时行情
    return w.wsq(security,"rt_post_mkt_dealnum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfRatioWsq(security:list,*args,**kwargs):
    # 获取当日净流入率实时行情
    return w.wsq(security,"rt_mf_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfRatio5DWsq(security:list,*args,**kwargs):
    # 获取5日净流入率实时行情
    return w.wsq(security,"rt_mf_ratio_5d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfRatio10DWsq(security:list,*args,**kwargs):
    # 获取10日净流入率实时行情
    return w.wsq(security,"rt_mf_ratio_10d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfRatio20DWsq(security:list,*args,**kwargs):
    # 获取20日净流入率实时行情
    return w.wsq(security,"rt_mf_ratio_20d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfRatio60DWsq(security:list,*args,**kwargs):
    # 获取60日净流入率实时行情
    return w.wsq(security,"rt_mf_ratio_60d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfdays5DWsq(security:list,*args,**kwargs):
    # 获取5日净流入天数实时行情
    return w.wsq(security,"rt_mf_days_5d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfdays10DWsq(security:list,*args,**kwargs):
    # 获取10日净流入天数实时行情
    return w.wsq(security,"rt_mf_days_10d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfdays20DWsq(security:list,*args,**kwargs):
    # 获取20日净流入天数实时行情
    return w.wsq(security,"rt_mf_days_20d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfdays60DWsq(security:list,*args,**kwargs):
    # 获取60日净流入天数实时行情
    return w.wsq(security,"rt_mf_days_60d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfAmtWsq(security:list,*args,**kwargs):
    # 获取当日净流入额实时行情
    return w.wsq(security,"rt_mf_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfAmt5DWsq(security:list,*args,**kwargs):
    # 获取5日净流入额实时行情
    return w.wsq(security,"rt_mf_amt_5d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfAmt10DWsq(security:list,*args,**kwargs):
    # 获取10日净流入额实时行情
    return w.wsq(security,"rt_mf_amt_10d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfAmt20DWsq(security:list,*args,**kwargs):
    # 获取20日净流入额实时行情
    return w.wsq(security,"rt_mf_amt_20d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMfAmt60DWsq(security:list,*args,**kwargs):
    # 获取60日净流入额实时行情
    return w.wsq(security,"rt_mf_amt_60d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBidVolWsq(security:list,*args,**kwargs):
    # 获取委买总量实时行情
    return w.wsq(security,"rt_bidvol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAskVolWsq(security:list,*args,**kwargs):
    # 获取委卖总量实时行情
    return w.wsq(security,"rt_askvol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBSizeTotalWsq(security:list,*args,**kwargs):
    # 获取委买十档总量实时行情
    return w.wsq(security,"rt_bsize_total",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtASizeTotalWsq(security:list,*args,**kwargs):
    # 获取委卖十档总量实时行情
    return w.wsq(security,"rt_asize_total",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiVipBidWsq(security:list,*args,**kwargs):
    # 获取机构大户买入单总数实时行情
    return w.wsq(security,"rt_insti_vip_bid",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiVipAskWsq(security:list,*args,**kwargs):
    # 获取机构大户卖出单总数实时行情
    return w.wsq(security,"rt_insti_vip_ask",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiVipNetInFlowRatioWsq(security:list,*args,**kwargs):
    # 获取当日机构大户净流入占比实时行情
    return w.wsq(security,"rt_insti_vip_netinflow_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtTransSumVolWsq(security:list,*args,**kwargs):
    # 获取逐笔成交累计成交量实时行情
    return w.wsq(security,"rt_trans_sum_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiBuyVolWsq(security:list,*args,**kwargs):
    # 获取当日机构买入成交量实时行情
    return w.wsq(security,"rt_insti_buy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiSellVolWsq(security:list,*args,**kwargs):
    # 获取当日机构卖出成交量实时行情
    return w.wsq(security,"rt_insti_sell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipBuyVolWsq(security:list,*args,**kwargs):
    # 获取当日大户买入成交量实时行情
    return w.wsq(security,"rt_vip_buy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipSellVolWsq(security:list,*args,**kwargs):
    # 获取当日大户卖出成交量实时行情
    return w.wsq(security,"rt_vip_sell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidBuyVolWsq(security:list,*args,**kwargs):
    # 获取当日中户买入成交量实时行情
    return w.wsq(security,"rt_mid_buy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidSellVolWsq(security:list,*args,**kwargs):
    # 获取当日中户卖出成交量实时行情
    return w.wsq(security,"rt_mid_sell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiBuyVolWsq(security:list,*args,**kwargs):
    # 获取当日散户买入成交量实时行情
    return w.wsq(security,"rt_indi_buy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiSellVolWsq(security:list,*args,**kwargs):
    # 获取当日散户卖出成交量实时行情
    return w.wsq(security,"rt_indi_sell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiNetBuyVolWsq(security:list,*args,**kwargs):
    # 获取当日机构净买入成交量实时行情
    return w.wsq(security,"rt_insti_netbuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipNetBuyVolWsq(security:list,*args,**kwargs):
    # 获取当日大户净买入成交量实时行情
    return w.wsq(security,"rt_vip_netbuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidNetBuyVolWsq(security:list,*args,**kwargs):
    # 获取当日中户净买入成交量实时行情
    return w.wsq(security,"rt_mid_netbuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiNetBuyVolWsq(security:list,*args,**kwargs):
    # 获取当日散户净买入成交量实时行情
    return w.wsq(security,"rt_indi_netbuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiTotalBidWsq(security:list,*args,**kwargs):
    # 获取当日机构买单总数实时行情
    return w.wsq(security,"rt_insti_total_bid",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiTotalAskWsq(security:list,*args,**kwargs):
    # 获取当日机构卖单总数实时行情
    return w.wsq(security,"rt_insti_total_ask",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipTotalBidWsq(security:list,*args,**kwargs):
    # 获取当日大户买单总数实时行情
    return w.wsq(security,"rt_vip_total_bid",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipTotalAskWsq(security:list,*args,**kwargs):
    # 获取当日大户卖单总数实时行情
    return w.wsq(security,"rt_vip_total_ask",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidTotalBidWsq(security:list,*args,**kwargs):
    # 获取当日中户买单总数实时行情
    return w.wsq(security,"rt_mid_total_bid",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidTotalAskWsq(security:list,*args,**kwargs):
    # 获取当日中户卖单总数实时行情
    return w.wsq(security,"rt_mid_total_ask",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiTotalBidWsq(security:list,*args,**kwargs):
    # 获取当日散户买单总数实时行情
    return w.wsq(security,"rt_indi_total_bid",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiTotalAskWsq(security:list,*args,**kwargs):
    # 获取当日散户卖单总数实时行情
    return w.wsq(security,"rt_indi_total_ask",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiInFlowWsq(security:list,*args,**kwargs):
    # 获取机构资金净流入实时行情
    return w.wsq(security,"rt_insti_inflow",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipInFlowWsq(security:list,*args,**kwargs):
    # 获取大户资金净流入实时行情
    return w.wsq(security,"rt_vip_inflow",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidInFlowWsq(security:list,*args,**kwargs):
    # 获取中户资金净流入实时行情
    return w.wsq(security,"rt_mid_inflow",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiInFlowWsq(security:list,*args,**kwargs):
    # 获取散户资金净流入实时行情
    return w.wsq(security,"rt_indi_inflow",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiBuyAmtWsq(security:list,*args,**kwargs):
    # 获取当日机构买入成交额实时行情
    return w.wsq(security,"rt_insti_buy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiSellAmtWsq(security:list,*args,**kwargs):
    # 获取当日机构卖出成交额实时行情
    return w.wsq(security,"rt_insti_sell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipBuyAmtWsq(security:list,*args,**kwargs):
    # 获取当日大户买入成交额实时行情
    return w.wsq(security,"rt_vip_buy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipSellAmtWsq(security:list,*args,**kwargs):
    # 获取当日大户卖出成交额实时行情
    return w.wsq(security,"rt_vip_sell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidBuyAmtWsq(security:list,*args,**kwargs):
    # 获取当日中户买入成交额实时行情
    return w.wsq(security,"rt_mid_buy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidSellAmtWsq(security:list,*args,**kwargs):
    # 获取当日中户卖出成交额实时行情
    return w.wsq(security,"rt_mid_sell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiBuyAmtWsq(security:list,*args,**kwargs):
    # 获取当日散户买入成交额实时行情
    return w.wsq(security,"rt_indi_buy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiSellAmtWsq(security:list,*args,**kwargs):
    # 获取当日散户卖出成交额实时行情
    return w.wsq(security,"rt_indi_sell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiActiveBuyAmtWsq(security:list,*args,**kwargs):
    # 获取机构主买入金额实时行情
    return w.wsq(security,"rt_insti_activebuy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipActiveBuyAmtWsq(security:list,*args,**kwargs):
    # 获取大户主买入金额实时行情
    return w.wsq(security,"rt_vip_activebuy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidActiveBuyAmtWsq(security:list,*args,**kwargs):
    # 获取中户主买入金额实时行情
    return w.wsq(security,"rt_mid_activebuy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiActiveBuyAmtWsq(security:list,*args,**kwargs):
    # 获取散户主买入金额实时行情
    return w.wsq(security,"rt_indi_activebuy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiActiveBuyVolWsq(security:list,*args,**kwargs):
    # 获取机构主买入总量实时行情
    return w.wsq(security,"rt_insti_activebuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipActiveBuyVolWsq(security:list,*args,**kwargs):
    # 获取大户主买入总量实时行情
    return w.wsq(security,"rt_vip_activebuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidActiveBuyVolWsq(security:list,*args,**kwargs):
    # 获取中户主买入总量实时行情
    return w.wsq(security,"rt_mid_activebuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiActiveBuyVolWsq(security:list,*args,**kwargs):
    # 获取散户主买入总量实时行情
    return w.wsq(security,"rt_indi_activebuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiActiveSellAmtWsq(security:list,*args,**kwargs):
    # 获取机构主卖出金额实时行情
    return w.wsq(security,"rt_insti_activesell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipActiveSellAmtWsq(security:list,*args,**kwargs):
    # 获取大户主卖出金额实时行情
    return w.wsq(security,"rt_vip_activesell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidActiveSellAmtWsq(security:list,*args,**kwargs):
    # 获取中户主卖出金额实时行情
    return w.wsq(security,"rt_mid_activesell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiActiveSellAmtWsq(security:list,*args,**kwargs):
    # 获取散户主卖出金额实时行情
    return w.wsq(security,"rt_indi_activesell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInStiActiveSellVolWsq(security:list,*args,**kwargs):
    # 获取机构主卖出总量实时行情
    return w.wsq(security,"rt_insti_activesell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVipActiveSellVolWsq(security:list,*args,**kwargs):
    # 获取大户主卖出总量实时行情
    return w.wsq(security,"rt_vip_activesell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMidActiveSellVolWsq(security:list,*args,**kwargs):
    # 获取中户主卖出总量实时行情
    return w.wsq(security,"rt_mid_activesell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtInDiActiveSellVolWsq(security:list,*args,**kwargs):
    # 获取散户主卖出总量实时行情
    return w.wsq(security,"rt_indi_activesell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActiveBuyAmtWsq(security:list,*args,**kwargs):
    # 获取主买总额实时行情
    return w.wsq(security,"rt_activebuy_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActiveBuyVolWsq(security:list,*args,**kwargs):
    # 获取主买总量实时行情
    return w.wsq(security,"rt_activebuy_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActiveSellAmtWsq(security:list,*args,**kwargs):
    # 获取主卖总额实时行情
    return w.wsq(security,"rt_activesell_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActiveSellVolWsq(security:list,*args,**kwargs):
    # 获取主卖总量实时行情
    return w.wsq(security,"rt_activesell_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActiveNetInvolWsq(security:list,*args,**kwargs):
    # 获取资金主动净流入量实时行情
    return w.wsq(security,"rt_activenetin_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActiveNetInAmtWsq(security:list,*args,**kwargs):
    # 获取资金主动净流入金额实时行情
    return w.wsq(security,"rt_activenetin_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActiveInvolPropWsq(security:list,*args,**kwargs):
    # 获取资金主动流向占比(量)实时行情
    return w.wsq(security,"rt_activeinvol_prop",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActiveInFlowPropWsq(security:list,*args,**kwargs):
    # 获取资金主动流向占比(金额)实时行情
    return w.wsq(security,"rt_activeinflow_prop",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtHkConnectTotalAmountWsq(security:list,*args,**kwargs):
    # 获取港股通当日可用总额实时行情
    return w.wsq(security,"rt_hkconnect_totalamount",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtHkConnectAmountUsedWsq(security:list,*args,**kwargs):
    # 获取港股通当日已用额实时行情
    return w.wsq(security,"rt_hkconnect_amountused",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtHkConnectAmountRemainWsq(security:list,*args,**kwargs):
    # 获取港股通当日剩余可用额实时行情
    return w.wsq(security,"rt_hkconnect_amountremain",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtNetBuyAmountWsq(security:list,*args,**kwargs):
    # 获取当日净买入实时行情
    return w.wsq(security,"rt_net_buy_amount",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBuyOrderWsq(security:list,*args,**kwargs):
    # 获取港股通当日买入实时行情
    return w.wsq(security,"rt_buy_order",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtSellOrderWsq(security:list,*args,**kwargs):
    # 获取港股通当日卖出实时行情
    return w.wsq(security,"rt_sell_order",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtTotalVolWsq(security:list,*args,**kwargs):
    # 获取港股通当日总成交实时行情
    return w.wsq(security,"rt_total_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAdjFactorWsq(security:list,*args,**kwargs):
    # 获取最新复权因子实时行情
    return w.wsq(security,"rt_adj_factor",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtDirectionWsq(security:list,*args,**kwargs):
    # 获取当笔成交方向实时行情
    return w.wsq(security,"rt_direction",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVolRatioWsq(security:list,*args,**kwargs):
    # 获取量比实时行情
    return w.wsq(security,"rt_vol_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtCommitteeWsq(security:list,*args,**kwargs):
    # 获取委比实时行情
    return w.wsq(security,"rt_committee",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtCommissionWsq(security:list,*args,**kwargs):
    # 获取委差实时行情
    return w.wsq(security,"rt_commission",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtTurnWsq(security:list,*args,**kwargs):
    # 获取换手率实时行情
    return w.wsq(security,"rt_turn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMktCapWsq(security:list,*args,**kwargs):
    # 获取总市值实时行情
    return w.wsq(security,"rt_mkt_cap",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtFloatMktCapWsq(security:list,*args,**kwargs):
    # 获取流通市值实时行情
    return w.wsq(security,"rt_float_mkt_cap",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtRiseDaysWsq(security:list,*args,**kwargs):
    # 获取连涨天数实时行情
    return w.wsq(security,"rt_rise_days",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtSUspFlagWsq(security:list,*args,**kwargs):
    # 获取停牌标志实时行情
    return w.wsq(security,"rt_susp_flag",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMa5DWsq(security:list,*args,**kwargs):
    # 获取5日MA实时行情
    return w.wsq(security,"rt_ma_5d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMa10DWsq(security:list,*args,**kwargs):
    # 获取10日MA实时行情
    return w.wsq(security,"rt_ma_10d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMa20DWsq(security:list,*args,**kwargs):
    # 获取20日MA实时行情
    return w.wsq(security,"rt_ma_20d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMa60DWsq(security:list,*args,**kwargs):
    # 获取60日MA实时行情
    return w.wsq(security,"rt_ma_60d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMa120DWsq(security:list,*args,**kwargs):
    # 获取120日MA实时行情
    return w.wsq(security,"rt_ma_120d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMa250DWsq(security:list,*args,**kwargs):
    # 获取250日MA实时行情
    return w.wsq(security,"rt_ma_250d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPeTtMWsq(security:list,*args,**kwargs):
    # 获取市盈率TTM实时行情
    return w.wsq(security,"rt_pe_ttm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPbLfWsq(security:list,*args,**kwargs):
    # 获取市净率LF实时行情
    return w.wsq(security,"rt_pb_lf",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMacDWsq(security:list,*args,**kwargs):
    # 获取MACD实时行情
    return w.wsq(security,"rt_macd",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMacDDiffWsq(security:list,*args,**kwargs):
    # 获取MACD_DIFF实时行情
    return w.wsq(security,"rt_macd_diff",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtKDjKWsq(security:list,*args,**kwargs):
    # 获取KDJ_K实时行情
    return w.wsq(security,"rt_kdj_k",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtKDjDWsq(security:list,*args,**kwargs):
    # 获取KDJ_D实时行情
    return w.wsq(security,"rt_kdj_d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtKDjJWsq(security:list,*args,**kwargs):
    # 获取KDJ_J实时行情
    return w.wsq(security,"rt_kdj_j",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtCci14Wsq(security:list,*args,**kwargs):
    # 获取CCI指标实时行情
    return w.wsq(security,"rt_cci_14",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVirtualVolumeWsq(security:list,*args,**kwargs):
    # 获取虚拟成交量实时行情
    return w.wsq(security,"rt_virtual_volume",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVirtualAmountWsq(security:list,*args,**kwargs):
    # 获取虚拟成交额实时行情
    return w.wsq(security,"rt_virtual_amount",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLastDpWsq(security:list,*args,**kwargs):
    # 获取全价最新价实时行情
    return w.wsq(security,"rt_last_dp",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLastCpWsq(security:list,*args,**kwargs):
    # 获取净价最新价实时行情
    return w.wsq(security,"rt_last_cp",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLastYTMWsq(security:list,*args,**kwargs):
    # 获取收益率最新价实时行情
    return w.wsq(security,"rt_last_ytm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPreCloseDpWsq(security:list,*args,**kwargs):
    # 获取全价前收价实时行情
    return w.wsq(security,"rt_pre_close_dp",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtDeliverySpdWsq(security:list,*args,**kwargs):
    # 获取期现价差实时行情
    return w.wsq(security,"rt_delivery_spd",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtIRrWsq(security:list,*args,**kwargs):
    # 获取IRR实时行情
    return w.wsq(security,"rt_irr",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtSpreadWsq(security:list,*args,**kwargs):
    # 获取基差实时行情
    return w.wsq(security,"rt_spread",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBidPrice1YTMWsq(security:list,*args,**kwargs):
    # 获取买1价到期收益率实时行情
    return w.wsq(security,"rt_bid_price1ytm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAskPrice1YTMWsq(security:list,*args,**kwargs):
    # 获取卖1价到期收益率实时行情
    return w.wsq(security,"rt_ask_price1ytm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBidPrice1YTeWsq(security:list,*args,**kwargs):
    # 获取买1价行权收益率实时行情
    return w.wsq(security,"rt_bid_price1yte",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAskPrice1YTeWsq(security:list,*args,**kwargs):
    # 获取卖1价行权收益率实时行情
    return w.wsq(security,"rt_ask_price1yte",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAvgYTMWsq(security:list,*args,**kwargs):
    # 获取均价收益率实时行情
    return w.wsq(security,"rt_avg_ytm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtYTMBpWsq(security:list,*args,**kwargs):
    # 获取最新收益率BP实时行情
    return w.wsq(security,"rt_ytm_bp",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMacDurationWsq(security:list,*args,**kwargs):
    # 获取麦氏久期实时行情
    return w.wsq(security,"rt_mac_duration",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBestBaWsq(security:list,*args,**kwargs):
    # 获取债券最优报价组合实时行情
    return w.wsq(security,"rt_best_ba",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBestBidYTMWsq(security:list,*args,**kwargs):
    # 获取债券最优买报价收益率实时行情
    return w.wsq(security,"rt_best_bid_ytm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBestBidAmtWsq(security:list,*args,**kwargs):
    # 获取债券最优买券面总额实时行情
    return w.wsq(security,"rt_best_bid_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBestAskYTMWsq(security:list,*args,**kwargs):
    # 获取债券最优卖报价收益率实时行情
    return w.wsq(security,"rt_best_ask_ytm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBestAskAmtWsq(security:list,*args,**kwargs):
    # 获取债券最优卖券面总额实时行情
    return w.wsq(security,"rt_best_ask_amt",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getOverflowRatioWsq(security:list,*args,**kwargs):
    # 获取转股溢价率实时行情
    return w.wsq(security,"OverflowRatio",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtUStockTurnoverWsq(security:list,*args,**kwargs):
    # 获取正股换手率实时行情
    return w.wsq(security,"rt_ustock_turnover",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtConVPriceWsq(security:list,*args,**kwargs):
    # 获取转股价格实时行情
    return w.wsq(security,"rt_conv_price",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtConVRatioWsq(security:list,*args,**kwargs):
    # 获取转股比例实时行情
    return w.wsq(security,"rt_conv_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtConVValueWsq(security:list,*args,**kwargs):
    # 获取转股价值实时行情
    return w.wsq(security,"rt_conv_value",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtArbSpaceWsq(security:list,*args,**kwargs):
    # 获取套利空间实时行情
    return w.wsq(security,"rt_arb_space",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtNBondPriceWsq(security:list,*args,**kwargs):
    # 获取纯债价值实时行情
    return w.wsq(security,"rt_nbond_price",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtNBondPremWsq(security:list,*args,**kwargs):
    # 获取纯债溢价率实时行情
    return w.wsq(security,"rt_nbond_prem",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtWarrantPriceWsq(security:list,*args,**kwargs):
    # 获取权证价格实时行情
    return w.wsq(security,"rt_warrant_price",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtYTMWsq(security:list,*args,**kwargs):
    # 获取到期收益率实时行情
    return w.wsq(security,"rt_ytm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPjDjWsq(security:list,*args,**kwargs):
    # 获取平价底价溢价率实时行情
    return w.wsq(security,"rt_pjdj",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtConVTypeWsq(security:list,*args,**kwargs):
    # 获取可转债类型实时行情
    return w.wsq(security,"rt_conv_type",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtCurrentCouponWsq(security:list,*args,**kwargs):
    # 获取当期票息实时行情
    return w.wsq(security,"rt_current_coupon",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAmtOutstandingWsq(security:list,*args,**kwargs):
    # 获取债券余额实时行情
    return w.wsq(security,"rt_amt_outstanding",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtRemainMaturityWsq(security:list,*args,**kwargs):
    # 获取剩余期限实时行情
    return w.wsq(security,"rt_remain_maturity",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBiHarmonicStrategyWsq(security:list,*args,**kwargs):
    # 获取双低实时行情
    return w.wsq(security,"rt_biharmonic_strategy",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPreIoPvWsq(security:list,*args,**kwargs):
    # 获取昨IOPV实时行情
    return w.wsq(security,"rt_pre_iopv",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtIoPvWsq(security:list,*args,**kwargs):
    # 获取IOPV实时行情
    return w.wsq(security,"rt_iopv",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtDiscountWsq(security:list,*args,**kwargs):
    # 获取折价实时行情
    return w.wsq(security,"rt_discount",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtDiscountRatioWsq(security:list,*args,**kwargs):
    # 获取折价率实时行情
    return w.wsq(security,"rt_discount_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtConTangoRatioWsq(security:list,*args,**kwargs):
    # 获取贴水率实时行情
    return w.wsq(security,"rt_contango_ratio",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtEstimatedChgWsq(security:list,*args,**kwargs):
    # 获取估算涨跌幅实时行情
    return w.wsq(security,"rt_estimated_chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPreOiWsq(security:list,*args,**kwargs):
    # 获取前持仓量实时行情
    return w.wsq(security,"rt_pre_oi",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOiWsq(security:list,*args,**kwargs):
    # 获取持仓量实时行情
    return w.wsq(security,"rt_oi",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOiChgWsq(security:list,*args,**kwargs):
    # 获取日增仓实时行情
    return w.wsq(security,"rt_oi_chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOiChangeWsq(security:list,*args,**kwargs):
    # 获取增仓实时行情
    return w.wsq(security,"rt_oi_change",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtNatureWsq(security:list,*args,**kwargs):
    # 获取性质实时行情
    return w.wsq(security,"rt_nature",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPreSettleWsq(security:list,*args,**kwargs):
    # 获取前结算价实时行情
    return w.wsq(security,"rt_pre_settle",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtSettleWsq(security:list,*args,**kwargs):
    # 获取结算价实时行情
    return w.wsq(security,"rt_settle",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtEstSettleWsq(security:list,*args,**kwargs):
    # 获取预估结算价实时行情
    return w.wsq(security,"rt_est_settle",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtDeltaWsq(security:list,*args,**kwargs):
    # 获取Delta实时行情
    return w.wsq(security,"rt_delta",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtGammaWsq(security:list,*args,**kwargs):
    # 获取Gamma实时行情
    return w.wsq(security,"rt_gamma",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVegaWsq(security:list,*args,**kwargs):
    # 获取Vega实时行情
    return w.wsq(security,"rt_vega",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtThetaWsq(security:list,*args,**kwargs):
    # 获取Theta实时行情
    return w.wsq(security,"rt_theta",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtRhoWsq(security:list,*args,**kwargs):
    # 获取Rho实时行情
    return w.wsq(security,"rt_rho",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtImpVolatilityWsq(security:list,*args,**kwargs):
    # 获取隐含波动率实时行情
    return w.wsq(security,"rt_imp_volatility",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtMIvWsq(security:list,*args,**kwargs):
    # 获取中价隐含波动率实时行情
    return w.wsq(security,"rt_miv",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid1IvLWsq(security:list,*args,**kwargs):
    # 获取买一隐含波动率实时行情
    return w.wsq(security,"rt_bid1_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid2IvLWsq(security:list,*args,**kwargs):
    # 获取买二隐含波动率实时行情
    return w.wsq(security,"rt_bid2_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid3IvLWsq(security:list,*args,**kwargs):
    # 获取买三隐含波动率实时行情
    return w.wsq(security,"rt_bid3_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid4IvLWsq(security:list,*args,**kwargs):
    # 获取买四隐含波动率实时行情
    return w.wsq(security,"rt_bid4_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid5IvLWsq(security:list,*args,**kwargs):
    # 获取买五隐含波动率实时行情
    return w.wsq(security,"rt_bid5_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid6IvLWsq(security:list,*args,**kwargs):
    # 获取买六隐含波动率实时行情
    return w.wsq(security,"rt_bid6_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid7IvLWsq(security:list,*args,**kwargs):
    # 获取买七隐含波动率实时行情
    return w.wsq(security,"rt_bid7_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid8IvLWsq(security:list,*args,**kwargs):
    # 获取买八隐含波动率实时行情
    return w.wsq(security,"rt_bid8_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid9IvLWsq(security:list,*args,**kwargs):
    # 获取买九隐含波动率实时行情
    return w.wsq(security,"rt_bid9_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBid10IvLWsq(security:list,*args,**kwargs):
    # 获取买十隐含波动率实时行情
    return w.wsq(security,"rt_bid10_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk1IvLWsq(security:list,*args,**kwargs):
    # 获取卖一隐含波动率实时行情
    return w.wsq(security,"rt_ask1_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk2IvLWsq(security:list,*args,**kwargs):
    # 获取卖二隐含波动率实时行情
    return w.wsq(security,"rt_ask2_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk3IvLWsq(security:list,*args,**kwargs):
    # 获取卖三隐含波动率实时行情
    return w.wsq(security,"rt_ask3_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk4IvLWsq(security:list,*args,**kwargs):
    # 获取卖四隐含波动率实时行情
    return w.wsq(security,"rt_ask4_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk5IvLWsq(security:list,*args,**kwargs):
    # 获取卖五隐含波动率实时行情
    return w.wsq(security,"rt_ask5_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk6IvLWsq(security:list,*args,**kwargs):
    # 获取卖六隐含波动率实时行情
    return w.wsq(security,"rt_ask6_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk7IvLWsq(security:list,*args,**kwargs):
    # 获取卖七隐含波动率实时行情
    return w.wsq(security,"rt_ask7_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk8IvLWsq(security:list,*args,**kwargs):
    # 获取卖八隐含波动率实时行情
    return w.wsq(security,"rt_ask8_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk9IvLWsq(security:list,*args,**kwargs):
    # 获取卖九隐含波动率实时行情
    return w.wsq(security,"rt_ask9_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtAsk10IvLWsq(security:list,*args,**kwargs):
    # 获取卖十隐含波动率实时行情
    return w.wsq(security,"rt_ask10_ivl",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtUStockPriceWsq(security:list,*args,**kwargs):
    # 获取正股价格实时行情
    return w.wsq(security,"rt_ustock_price",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtUStockChgWsq(security:list,*args,**kwargs):
    # 获取正股涨跌幅实时行情
    return w.wsq(security,"rt_ustock_chg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtIntValueWsq(security:list,*args,**kwargs):
    # 获取内在价值实时行情
    return w.wsq(security,"rt_int_value",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtTimeValueWsq(security:list,*args,**kwargs):
    # 获取时间价值实时行情
    return w.wsq(security,"rt_time_value",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtTvAssetWsq(security:list,*args,**kwargs):
    # 获取时间价值（标的）实时行情
    return w.wsq(security,"rt_tv_asset",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtActLmWsq(security:list,*args,**kwargs):
    # 获取实际杠杆倍数实时行情
    return w.wsq(security,"rt_act_lm",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOptMarginWsq(security:list,*args,**kwargs):
    # 获取保证金实时行情
    return w.wsq(security,"rt_opt_margin",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOptNrWsq(security:list,*args,**kwargs):
    # 获取指数属性实时行情
    return w.wsq(security,"rt_opt_nr",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOptVsWsq(security:list,*args,**kwargs):
    # 获取期权价值状态实时行情
    return w.wsq(security,"rt_opt_vs",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOptTheoryPriceWsq(security:list,*args,**kwargs):
    # 获取理论价格实时行情
    return w.wsq(security,"rt_opt_theoryprice",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtPreIvWsq(security:list,*args,**kwargs):
    # 获取前隐含波动率实时行情
    return w.wsq(security,"rt_pre_iv",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtIvChangeWsq(security:list,*args,**kwargs):
    # 获取隐含波动率涨跌幅实时行情
    return w.wsq(security,"rt_iv_change",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtBidAsKspreadWsq(security:list,*args,**kwargs):
    # 获取最优买卖价差实时行情
    return w.wsq(security,"rt_bidaskspread",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOptVolWsq(security:list,*args,**kwargs):
    # 获取期权成交量实时行情
    return w.wsq(security,"rt_opt_vol",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtOptOiWsq(security:list,*args,**kwargs):
    # 获取期权持仓量实时行情
    return w.wsq(security,"rt_opt_oi",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtVolPcrWsq(security:list,*args,**kwargs):
    # 获取成交量PCR实时行情
    return w.wsq(security,"rt_vol_pcr",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtUpTotalWsq(security:list,*args,**kwargs):
    # 获取上涨家数实时行情
    return w.wsq(security,"rt_up_total",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtSameTotalWsq(security:list,*args,**kwargs):
    # 获取平盘家数实时行情
    return w.wsq(security,"rt_same_total",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtDownTotalWsq(security:list,*args,**kwargs):
    # 获取下跌家数实时行情
    return w.wsq(security,"rt_down_total",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtLeadingIndicatorsWsq(security:list,*args,**kwargs):
    # 获取领先指标实时行情
    return w.wsq(security,"rt_leading_indicators",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtRsi6DWsq(security:list,*args,**kwargs):
    # 获取RSI_6指标实时行情
    return w.wsq(security,"rt_rsi_6d",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsq
def getRtRsi12DWsq(security:list,*args,**kwargs):
    # 获取RSI_12指标实时行情
    return w.wsq(security,"rt_rsi_12d",*args,**kwargs,usedf=True)