#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from WindPy import w
def convertInputSecurityTypeForWsee(func):
    def convertedFunc(*args):
        args = tuple((i.strftime("%Y%m%d") if hasattr(i,"strftime") else i for i in args))
        if type(args[0])==type(''):
            return func(*args)[1].fillna(np.nan)
        else:
            security = args[0]
            args = args[1:]
            return func(",".join(security),*args)[1].fillna(np.nan)
    return convertedFunc
@convertInputSecurityTypeForWsee
def getSecCloseAvgWsee(security:list,*args,**kwargs):
    # 获取收盘价(算术平均)板块多维
    return w.wsee(security,"sec_close_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCloseTsWavGWsee(security:list,*args,**kwargs):
    # 获取收盘价(总股本加权平均)板块多维
    return w.wsee(security,"sec_close_tswavg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCloseFfsWavGChNWsee(security:list,*args,**kwargs):
    # 获取收盘价(流通股本加权平均)(中国)板块多维
    return w.wsee(security,"sec_close_ffswavg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTurnAvgWsee(security:list,*args,**kwargs):
    # 获取换手率(算术平均)板块多维
    return w.wsee(security,"sec_turn_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTurnTMcWavGWsee(security:list,*args,**kwargs):
    # 获取换手率(总市值加权平均)板块多维
    return w.wsee(security,"sec_turn_tmc_wavg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTurnFfMcWavGWsee(security:list,*args,**kwargs):
    # 获取换手率(流通市值加权平均)板块多维
    return w.wsee(security,"sec_turn_ffmc_wavg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqPctChgAvgWsee(security:list,*args,**kwargs):
    # 获取区间涨跌幅(算术平均)板块多维
    return w.wsee(security,"sec_pq_pct_chg_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqPctChgTMcWavGWsee(security:list,*args,**kwargs):
    # 获取区间涨跌幅(总市值加权平均)板块多维
    return w.wsee(security,"sec_pq_pct_chg_tmc_wavg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqPctChgFfMcWavGChNWsee(security:list,*args,**kwargs):
    # 获取区间涨跌幅(流通市值加权平均)(中国)板块多维
    return w.wsee(security,"sec_pq_pct_chg_ffmc_wavg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqVolSumWsee(security:list,*args,**kwargs):
    # 获取区间成交量(合计)板块多维
    return w.wsee(security,"sec_pq_vol_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqAmtSumWsee(security:list,*args,**kwargs):
    # 获取区间成交金额(合计)板块多维
    return w.wsee(security,"sec_pq_amt_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqTurnAvgWsee(security:list,*args,**kwargs):
    # 获取区间换手率(算术平均)板块多维
    return w.wsee(security,"sec_pq_turn_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqAvgTurnAvgWsee(security:list,*args,**kwargs):
    # 获取区间日均换手率(算术平均)板块多维
    return w.wsee(security,"sec_pq_avgturn_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareTotalSumWsee(security:list,*args,**kwargs):
    # 获取总股本(合计)板块多维
    return w.wsee(security,"sec_share_total_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareTotalAvgWsee(security:list,*args,**kwargs):
    # 获取总股本(算术平均)板块多维
    return w.wsee(security,"sec_share_total_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareFloatASumWsee(security:list,*args,**kwargs):
    # 获取流通A股(合计)板块多维
    return w.wsee(security,"sec_share_float_a_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareFloatAAvgWsee(security:list,*args,**kwargs):
    # 获取流通A股(算术平均)板块多维
    return w.wsee(security,"sec_share_float_a_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareFloatBSumWsee(security:list,*args,**kwargs):
    # 获取流通B股(合计)板块多维
    return w.wsee(security,"sec_share_float_b_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareFloatBAvgWsee(security:list,*args,**kwargs):
    # 获取流通B股(算术平均)板块多维
    return w.wsee(security,"sec_share_float_b_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareFloatHSumWsee(security:list,*args,**kwargs):
    # 获取流通H股(合计)板块多维
    return w.wsee(security,"sec_share_float_h_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareFloatHAvgWsee(security:list,*args,**kwargs):
    # 获取流通H股(算术平均)板块多维
    return w.wsee(security,"sec_share_float_h_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareFloatTotalSumChNWsee(security:list,*args,**kwargs):
    # 获取总流通股本(合计)(中国)板块多维
    return w.wsee(security,"sec_share_float_total_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareFloatTotalAvgChNWsee(security:list,*args,**kwargs):
    # 获取总流通股本(算术平均)(中国)板块多维
    return w.wsee(security,"sec_share_float_total_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareTotalNonLiqSumChNWsee(security:list,*args,**kwargs):
    # 获取非流通股(合计)(中国)板块多维
    return w.wsee(security,"sec_share_totalnonliq_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecShareTotalNonLiqAvgChNWsee(security:list,*args,**kwargs):
    # 获取非流通股(算术平均)(中国)板块多维
    return w.wsee(security,"sec_share_totalnonliq_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecWestEpsOverallChNWsee(security:list,*args,**kwargs):
    # 获取预测每股收益(整体法)板块多维
    return w.wsee(security,"sec_west_eps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecWestEpsAvgChNWsee(security:list,*args,**kwargs):
    # 获取预测每股收益(算术平均)板块多维
    return w.wsee(security,"sec_west_eps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecWestNpSumChNWsee(security:list,*args,**kwargs):
    # 获取预测净利润(合计)板块多维
    return w.wsee(security,"sec_west_np_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecWestNpAvgChNWsee(security:list,*args,**kwargs):
    # 获取预测净利润(算术平均)板块多维
    return w.wsee(security,"sec_west_np_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecWestRevenueSumChNWsee(security:list,*args,**kwargs):
    # 获取预测主营业务收入(合计)板块多维
    return w.wsee(security,"sec_west_revenue_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecWestRevenueAvgChNWsee(security:list,*args,**kwargs):
    # 获取预测主营业务收入(算术平均)板块多维
    return w.wsee(security,"sec_west_revenue_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNCashInFlowDSumChNWsee(security:list,*args,**kwargs):
    # 获取(日)净流入资金(合计)板块多维
    return w.wsee(security,"sec_ncashinflow_d_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNCashInFlowDAvgChNWsee(security:list,*args,**kwargs):
    # 获取(日)净流入资金(算术平均)板块多维
    return w.wsee(security,"sec_ncashinflow_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNVolInFlowDSumChNWsee(security:list,*args,**kwargs):
    # 获取(日)净流入量(合计)板块多维
    return w.wsee(security,"sec_nvolinflow_d_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNVolInFlowDAvgChNWsee(security:list,*args,**kwargs):
    # 获取(日)净流入量(算术平均)板块多维
    return w.wsee(security,"sec_nvolinflow_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNClosingInFlowDSumChNWsee(security:list,*args,**kwargs):
    # 获取(日)尾盘净流入资金(合计)板块多维
    return w.wsee(security,"sec_nclosinginflow_d_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNClosingInFlowDAvgChNWsee(security:list,*args,**kwargs):
    # 获取(日)尾盘净流入资金(算术平均)板块多维
    return w.wsee(security,"sec_nclosinginflow_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNOpeningInFlowDSumChNWsee(security:list,*args,**kwargs):
    # 获取(日)开盘净流入资金(合计)板块多维
    return w.wsee(security,"sec_nopeninginflow_d_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNOpeningInFlowDAvgChNWsee(security:list,*args,**kwargs):
    # 获取(日)开盘净流入资金(算术平均)板块多维
    return w.wsee(security,"sec_nopeninginflow_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCInFlowRateDOverallChNWsee(security:list,*args,**kwargs):
    # 获取(日)金额流入率(整体法)板块多维
    return w.wsee(security,"sec_cinflowrate_d_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCInFlowRateDAvgChNWsee(security:list,*args,**kwargs):
    # 获取(日)金额流入率(算术平均)板块多维
    return w.wsee(security,"sec_cinflowrate_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCashDirectionPecDOverallChNWsee(security:list,*args,**kwargs):
    # 获取(日)资金流向占比(整体法)板块多维
    return w.wsee(security,"sec_cashdirectionpec_d_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCashDirectionPecDAvgChNWsee(security:list,*args,**kwargs):
    # 获取(日)资金流向占比(算术平均)板块多维
    return w.wsee(security,"sec_cashdirectionpec_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqNCashInFlowSumChNWsee(security:list,*args,**kwargs):
    # 获取(区间)净流入资金(合计)板块多维
    return w.wsee(security,"sec_pq_ncashinflow_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqNCashInFlowAvgChNWsee(security:list,*args,**kwargs):
    # 获取(区间)净流入资金(算术平均)板块多维
    return w.wsee(security,"sec_pq_ncashinflow_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqNVolInFlowSumChNWsee(security:list,*args,**kwargs):
    # 获取(区间)净流入量(合计)板块多维
    return w.wsee(security,"sec_pq_nvolinflow_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqNVolInFlowAvgChNWsee(security:list,*args,**kwargs):
    # 获取(区间)净流入量(算术平均)板块多维
    return w.wsee(security,"sec_pq_nvolinflow_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqNClosingInFlowSumChNWsee(security:list,*args,**kwargs):
    # 获取(区间)尾盘净流入资金(合计)板块多维
    return w.wsee(security,"sec_pq_nclosinginflow_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqNClosingInFlowAvgChNWsee(security:list,*args,**kwargs):
    # 获取(区间)尾盘净流入资金(算术平均)板块多维
    return w.wsee(security,"sec_pq_nclosinginflow_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqNOpeningInFlowSumChNWsee(security:list,*args,**kwargs):
    # 获取(区间)开盘净流入资金(合计)板块多维
    return w.wsee(security,"sec_pq_nopeninginflow_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqNOpeningInFlowAvgChNWsee(security:list,*args,**kwargs):
    # 获取(区间)开盘净流入资金(算术平均)板块多维
    return w.wsee(security,"sec_pq_nopeninginflow_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqCInFlowRateOverallChNWsee(security:list,*args,**kwargs):
    # 获取(区间)金额流入率(整体法)板块多维
    return w.wsee(security,"sec_pq_cinflowrate_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqCInFlowRateAvgChNWsee(security:list,*args,**kwargs):
    # 获取(区间)金额流入率(算术平均)板块多维
    return w.wsee(security,"sec_pq_cinflowrate_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqCashDirectionPecOverallChNWsee(security:list,*args,**kwargs):
    # 获取(区间)资金流向占比(整体法)板块多维
    return w.wsee(security,"sec_pq_cashdirectionpec_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPqCashDirectionPecAvgChNWsee(security:list,*args,**kwargs):
    # 获取(区间)资金流向占比(算术平均)板块多维
    return w.wsee(security,"sec_pq_cashdirectionpec_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapSumGLbWsee(security:list,*args,**kwargs):
    # 获取总市值(合计)板块多维
    return w.wsee(security,"sec_mkt_cap_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapAvgGLbWsee(security:list,*args,**kwargs):
    # 获取总市值(算术平均)板块多维
    return w.wsee(security,"sec_mkt_cap_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMvArdSumGLbWsee(security:list,*args,**kwargs):
    # 获取总市值2(合计)板块多维
    return w.wsee(security,"sec_mv_ard_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMvArdAvgGLbWsee(security:list,*args,**kwargs):
    # 获取总市值2(算术平均)板块多维
    return w.wsee(security,"sec_mv_ard_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPeTtMAvgChNWsee(security:list,*args,**kwargs):
    # 获取市盈率(TTM-算术平均法)板块多维
    return w.wsee(security,"sec_pe_ttm_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPetTmMediaChNWsee(security:list,*args,**kwargs):
    # 获取市盈率(TTM-中值)板块多维
    return w.wsee(security,"sec_pettm_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPeAvgChNWsee(security:list,*args,**kwargs):
    # 获取市盈率(算术平均)板块多维
    return w.wsee(security,"sec_pe_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPeMediaChNWsee(security:list,*args,**kwargs):
    # 获取市盈率(中值)板块多维
    return w.wsee(security,"sec_pe_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPbAvgChNWsee(security:list,*args,**kwargs):
    # 获取市净率(算术平均)板块多维
    return w.wsee(security,"sec_pb_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPbMediaChNWsee(security:list,*args,**kwargs):
    # 获取市净率(中值)板块多维
    return w.wsee(security,"sec_pb_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPcfAvgChNWsee(security:list,*args,**kwargs):
    # 获取市现率(算术平均)板块多维
    return w.wsee(security,"sec_pcf_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPcfMediaChNWsee(security:list,*args,**kwargs):
    # 获取市现率(中值)板块多维
    return w.wsee(security,"sec_pcf_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPsAvgChNWsee(security:list,*args,**kwargs):
    # 获取市销率(算术平均)板块多维
    return w.wsee(security,"sec_ps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPsMediaChNWsee(security:list,*args,**kwargs):
    # 获取市销率(中值)板块多维
    return w.wsee(security,"sec_ps_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPeTtMOverallChNWsee(security:list,*args,**kwargs):
    # 获取市盈率(TTM-整体法)板块多维
    return w.wsee(security,"sec_pe_ttm_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPbOverallChNWsee(security:list,*args,**kwargs):
    # 获取市净率(整体法)板块多维
    return w.wsee(security,"sec_pb_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPcfOverallChNWsee(security:list,*args,**kwargs):
    # 获取市现率(整体法)板块多维
    return w.wsee(security,"sec_pcf_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecPsOverallChNWsee(security:list,*args,**kwargs):
    # 获取市销率(整体法)板块多维
    return w.wsee(security,"sec_ps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapTodaySumChNWsee(security:list,*args,**kwargs):
    # 获取当日总市值(合计)板块多维
    return w.wsee(security,"sec_mkt_cap_today_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapTodayAvgChNWsee(security:list,*args,**kwargs):
    # 获取当日总市值(算术平均)板块多维
    return w.wsee(security,"sec_mkt_cap_today_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapFloatASharesSumChNWsee(security:list,*args,**kwargs):
    # 获取流通A股市值(合计)板块多维
    return w.wsee(security,"sec_mkt_cap_float_ashares_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapFloatASharesAvgChNWsee(security:list,*args,**kwargs):
    # 获取流通A股市值(算术平均)板块多维
    return w.wsee(security,"sec_mkt_cap_float_ashares_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapFloatBSharesSumChNWsee(security:list,*args,**kwargs):
    # 获取流通B股市值(合计)板块多维
    return w.wsee(security,"sec_mkt_cap_float_bshares_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapFloatBSharesAvgChNWsee(security:list,*args,**kwargs):
    # 获取流通B股市值(算术平均)板块多维
    return w.wsee(security,"sec_mkt_cap_float_bshares_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapFloatFreeSharesSumChNWsee(security:list,*args,**kwargs):
    # 获取自由流通市值(合计)板块多维
    return w.wsee(security,"sec_mkt_cap_float_freeshares_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMktCapFloatFreeSharesAvgChNWsee(security:list,*args,**kwargs):
    # 获取自由流通市值(算术平均)板块多维
    return w.wsee(security,"sec_mkt_cap_float_freeshares_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskAnnualYeIlD100WAvgChNWsee(security:list,*args,**kwargs):
    # 获取年化收益率算术平均(最近100周)板块多维
    return w.wsee(security,"sec_risk_annualyeild_100w_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskAnnualYeIlD24MAvgChNWsee(security:list,*args,**kwargs):
    # 获取年化收益率算术平均(最近24个月)板块多维
    return w.wsee(security,"sec_risk_annualyeild_24m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskAnnualYeIlD60MAvgChNWsee(security:list,*args,**kwargs):
    # 获取年化收益率算术平均(最近60个月)板块多维
    return w.wsee(security,"sec_risk_annualyeild_60m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskStDevYearly100WAvgChNWsee(security:list,*args,**kwargs):
    # 获取年化波动率算术平均(最近100周)板块多维
    return w.wsee(security,"sec_risk_stdevyearly_100w_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskStDevYearly24MAvgChNWsee(security:list,*args,**kwargs):
    # 获取年化波动率算术平均(最近24个月)板块多维
    return w.wsee(security,"sec_risk_stdevyearly_24m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskStDevYearly60MAvgChNWsee(security:list,*args,**kwargs):
    # 获取年化波动率算术平均(最近60个月)板块多维
    return w.wsee(security,"sec_risk_stdevyearly_60m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskBeta100WAvgChNWsee(security:list,*args,**kwargs):
    # 获取BETA值算术平均(最近100周)板块多维
    return w.wsee(security,"sec_risk_beta_100w_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskBeta24MAvgChNWsee(security:list,*args,**kwargs):
    # 获取BETA值算术平均(最近24个月)板块多维
    return w.wsee(security,"sec_risk_beta_24m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRiskBeta60MAvgChNWsee(security:list,*args,**kwargs):
    # 获取BETA值算术平均(最近60个月)板块多维
    return w.wsee(security,"sec_risk_beta_60m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCsrCStatListCompNumChNWsee(security:list,*args,**kwargs):
    # 获取上市公司家数板块多维
    return w.wsee(security,"sec_csrc_statlistcompnum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCsrCStatShareTotalChNWsee(security:list,*args,**kwargs):
    # 获取上市公司境内总股本板块多维
    return w.wsee(security,"sec_csrc_stat_sharetotal_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCsrCStatMvChNWsee(security:list,*args,**kwargs):
    # 获取上市公司境内总市值板块多维
    return w.wsee(security,"sec_csrc_stat_mv_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCsrCStatPeChNWsee(security:list,*args,**kwargs):
    # 获取市场静态市盈率板块多维
    return w.wsee(security,"sec_csrc_stat_pe_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCsrCStatPbChNWsee(security:list,*args,**kwargs):
    # 获取市场静态市净率板块多维
    return w.wsee(security,"sec_csrc_stat_pb_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCsrCStatNpTtMChNWsee(security:list,*args,**kwargs):
    # 获取上市公司境内股本对应的归属母公司净利润TTM板块多维
    return w.wsee(security,"sec_csrc_stat_np_ttm_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCsrCStatPeTtMChNWsee(security:list,*args,**kwargs):
    # 获取市场滚动市盈率板块多维
    return w.wsee(security,"sec_csrc_stat_pe_ttm_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEpsBasic2AvgChNWsee(security:list,*args,**kwargs):
    # 获取每股收益EPS-基本(算术平均)板块多维
    return w.wsee(security,"sec_eps_basic2_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEpsDiluted4AvgChNWsee(security:list,*args,**kwargs):
    # 获取每股收益EPS-稀释(算术平均)板块多维
    return w.wsee(security,"sec_eps_diluted4_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEndingSharesEpsBasic2OverallChNWsee(security:list,*args,**kwargs):
    # 获取每股收益EPS-期末股本摊薄(整体法)板块多维
    return w.wsee(security,"sec_endingshareseps_basic2_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEndingSharesEpsBasic2AvgChNWsee(security:list,*args,**kwargs):
    # 获取每股收益EPS-期末股本摊薄(算术平均)板块多维
    return w.wsee(security,"sec_endingshareseps_basic2_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecBpSOverallChNWsee(security:list,*args,**kwargs):
    # 获取每股净资产(整体法)板块多维
    return w.wsee(security,"sec_bps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecBpSAvgChNWsee(security:list,*args,**kwargs):
    # 获取每股净资产(算术平均)板块多维
    return w.wsee(security,"sec_bps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrpSOverallChNWsee(security:list,*args,**kwargs):
    # 获取每股营业总收入(整体法)板块多维
    return w.wsee(security,"sec_grps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrpSAvgChNWsee(security:list,*args,**kwargs):
    # 获取每股营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_grps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRetainedPsOverallChNWsee(security:list,*args,**kwargs):
    # 获取每股留存收益(整体法)板块多维
    return w.wsee(security,"sec_retainedps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRetainedPsAvgChNWsee(security:list,*args,**kwargs):
    # 获取每股留存收益(算术平均)板块多维
    return w.wsee(security,"sec_retainedps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCfpSOverallChNWsee(security:list,*args,**kwargs):
    # 获取每股现金流量净额(整体法)板块多维
    return w.wsee(security,"sec_cfps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCfpSAvgChNWsee(security:list,*args,**kwargs):
    # 获取每股现金流量净额(算术平均)板块多维
    return w.wsee(security,"sec_cfps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOcFps2OverallChNWsee(security:list,*args,**kwargs):
    # 获取每股经营活动产生的现金流量净额(整体法)板块多维
    return w.wsee(security,"sec_ocfps2_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOcFps2AvgChNWsee(security:list,*args,**kwargs):
    # 获取每股经营活动产生的现金流量净额(算术平均)板块多维
    return w.wsee(security,"sec_ocfps2_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEbItPsAvgGLbWsee(security:list,*args,**kwargs):
    # 获取每股息税前利润(算术平均)板块多维
    return w.wsee(security,"sec_ebitps_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFcFFpsOverallGLbWsee(security:list,*args,**kwargs):
    # 获取每股企业自由现金流量(整体法)板块多维
    return w.wsee(security,"sec_fcffps_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFcFFpsAvgGLbWsee(security:list,*args,**kwargs):
    # 获取每股企业自由现金流量(算术平均)板块多维
    return w.wsee(security,"sec_fcffps_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFcFEpsOverallGLbWsee(security:list,*args,**kwargs):
    # 获取每股股东自由现金流量(整体法)板块多维
    return w.wsee(security,"sec_fcfeps_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFcFEpsAvgGLbWsee(security:list,*args,**kwargs):
    # 获取每股股东自由现金流量(算术平均)板块多维
    return w.wsee(security,"sec_fcfeps_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoeAvgOverallChNWsee(security:list,*args,**kwargs):
    # 获取净资产收益率-平均(整体法)板块多维
    return w.wsee(security,"sec_roe_avg_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoeAvgAvgChNWsee(security:list,*args,**kwargs):
    # 获取净资产收益率-平均(算术平均)板块多维
    return w.wsee(security,"sec_roe_avg_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoeDilutedOverallChNWsee(security:list,*args,**kwargs):
    # 获取净资产收益率-摊薄(整体法)板块多维
    return w.wsee(security,"sec_roe_diluted_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoeDilutedAvgChNWsee(security:list,*args,**kwargs):
    # 获取净资产收益率-摊薄(算术平均)板块多维
    return w.wsee(security,"sec_roe_diluted_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDeductedRoeAvgOverallChNWsee(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净资产收益率-平均(整体法)板块多维
    return w.wsee(security,"sec_deductedroe_avg_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDeductedRoeAvgAvgChNWsee(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净资产收益率-平均(算术平均)板块多维
    return w.wsee(security,"sec_deductedroe_avg_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDeductedRoeDilutedOverallChNWsee(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净资产收益率-摊薄(整体法)板块多维
    return w.wsee(security,"sec_deductedroe_diluted_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDeductedRoeDilutedAvgChNWsee(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净资产收益率-摊薄(算术平均)板块多维
    return w.wsee(security,"sec_deductedroe_diluted_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoa2OverallGLbWsee(security:list,*args,**kwargs):
    # 获取总资产报酬率(整体法)板块多维
    return w.wsee(security,"sec_roa2_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoa2AvgGLbWsee(security:list,*args,**kwargs):
    # 获取总资产报酬率(算术平均)板块多维
    return w.wsee(security,"sec_roa2_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoaOverallChNWsee(security:list,*args,**kwargs):
    # 获取总资产净利率(整体法)板块多维
    return w.wsee(security,"sec_roa_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoaAvgChNWsee(security:list,*args,**kwargs):
    # 获取总资产净利率(算术平均)板块多维
    return w.wsee(security,"sec_roa_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrossProfitMarginOverallChNWsee(security:list,*args,**kwargs):
    # 获取销售毛利率(整体法)板块多维
    return w.wsee(security,"sec_grossprofitmargin_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrossProfitMarginAvgChNWsee(security:list,*args,**kwargs):
    # 获取销售毛利率(算术平均)板块多维
    return w.wsee(security,"sec_grossprofitmargin_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNetProfitMarginOverallChNWsee(security:list,*args,**kwargs):
    # 获取销售净利率(整体法)板块多维
    return w.wsee(security,"sec_netprofitmargin_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNetProfitMarginAvgChNWsee(security:list,*args,**kwargs):
    # 获取销售净利率(算术平均)板块多维
    return w.wsee(security,"sec_netprofitmargin_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGcToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取营业总成本/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_gctogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGcToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取营业总成本/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_gctogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOpToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取营业利润/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_optogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOpToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取营业利润/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_optogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDupontNpToSalesOverallChNWsee(security:list,*args,**kwargs):
    # 获取净利润/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_dupont_nptosales_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDupontNpToSalesAvgChNWsee(security:list,*args,**kwargs):
    # 获取净利润/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_dupont_nptosales_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOperateExpenseToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取销售费用/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_operateexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSEcfAAdminExpenseToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取管理费用/营业总收入(算术平均)板块多维
    return w.wsee(security,"secfa_adminexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFinaExpenseToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取财务费用/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_finaexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDupontEbItToSalesAvgGLbWsee(security:list,*args,**kwargs):
    # 获取息税前利润/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_dupont_ebittosales_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEbItDatoSalesOverallGLbWsee(security:list,*args,**kwargs):
    # 获取EBITDA/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_ebitdatosales_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEbItDatoSalesAvgGLbWsee(security:list,*args,**kwargs):
    # 获取EBITDA/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_ebitdatosales_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRoiCAvgGLbWsee(security:list,*args,**kwargs):
    # 获取投入资本回报率(算术平均)板块多维
    return w.wsee(security,"sec_roic_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOpToEBTAvgGLbWsee(security:list,*args,**kwargs):
    # 获取营业利润/利润总额(算术平均)板块多维
    return w.wsee(security,"sec_optoebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvestIncomeToEBTAvgChNWsee(security:list,*args,**kwargs):
    # 获取价值变动净收益/利润总额(算术平均)板块多维
    return w.wsee(security,"sec_investincometoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTaxToEBTAvgChNWsee(security:list,*args,**kwargs):
    # 获取所得税/利润总额(算术平均)板块多维
    return w.wsee(security,"sec_taxtoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDeductedProfitToProfitAvgChNWsee(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净利润/净利润(算术平均)板块多维
    return w.wsee(security,"sec_deductedprofittoprofit_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOperateIncomeToEBTAvgChNWsee(security:list,*args,**kwargs):
    # 获取经营活动净收益/利润总额(算术平均)板块多维
    return w.wsee(security,"sec_operateincometoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOCFToOrOverallChNWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/营业收入(整体法)板块多维
    return w.wsee(security,"sec_ocftoor_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOCFToOrAvgChNWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/营业收入(算术平均)板块多维
    return w.wsee(security,"sec_ocftoor_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOCFToOperateIncomeOverallChNWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/经营活动净收益(整体法)板块多维
    return w.wsee(security,"sec_ocftooperateincome_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOCFToOperateIncomeAvgChNWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/经营活动净收益(算术平均)板块多维
    return w.wsee(security,"sec_ocftooperateincome_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCapitalizedTodaOverallGLbWsee(security:list,*args,**kwargs):
    # 获取资本支出/折旧和摊销(整体法)板块多维
    return w.wsee(security,"sec_capitalizedtoda_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCapitalizedTodaAvgChNWsee(security:list,*args,**kwargs):
    # 获取资本支出/折旧和摊销(算术平均)板块多维
    return w.wsee(security,"sec_capitalizedtoda_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDebtToAssetsOverallChNWsee(security:list,*args,**kwargs):
    # 获取资产负债率(整体法)板块多维
    return w.wsee(security,"sec_debttoassets_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDebtToAssetsAvgChNWsee(security:list,*args,**kwargs):
    # 获取资产负债率(算术平均)板块多维
    return w.wsee(security,"sec_debttoassets_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCatoAssetsOverallChNWsee(security:list,*args,**kwargs):
    # 获取流动资产/总资产(整体法)板块多维
    return w.wsee(security,"sec_catoassets_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCatoAssetsAvgChNWsee(security:list,*args,**kwargs):
    # 获取流动资产/总资产(算术平均)板块多维
    return w.wsee(security,"sec_catoassets_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNcaToAssetsOverallChNWsee(security:list,*args,**kwargs):
    # 获取非流动资产/总资产(整体法)板块多维
    return w.wsee(security,"sec_ncatoassets_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNcaToAssetsAvgChNWsee(security:list,*args,**kwargs):
    # 获取非流动资产/总资产(算术平均)板块多维
    return w.wsee(security,"sec_ncatoassets_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTangibleAssetsToAssetsOverallChNWsee(security:list,*args,**kwargs):
    # 获取有形资产/总资产(整体法)板块多维
    return w.wsee(security,"sec_tangibleassetstoassets_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTangibleAssetsToAssetsAvgChNWsee(security:list,*args,**kwargs):
    # 获取有形资产/总资产(算术平均)板块多维
    return w.wsee(security,"sec_tangibleassetstoassets_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentDebtToDebtOverallChNWsee(security:list,*args,**kwargs):
    # 获取流动负债/负债合计(整体法)板块多维
    return w.wsee(security,"sec_currentdebttodebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentDebtToDebtAvgChNWsee(security:list,*args,**kwargs):
    # 获取流动负债/负债合计(算术平均)板块多维
    return w.wsee(security,"sec_currentdebttodebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecLongDebToDebtOverallChNWsee(security:list,*args,**kwargs):
    # 获取非流动负债/负债合计(整体法)板块多维
    return w.wsee(security,"sec_longdebtodebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecLongDebToDebtAvgChNWsee(security:list,*args,**kwargs):
    # 获取非流动负债/负债合计(算术平均)板块多维
    return w.wsee(security,"sec_longdebtodebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentOverallChNWsee(security:list,*args,**kwargs):
    # 获取流动比率(整体法)板块多维
    return w.wsee(security,"sec_current_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentAvgChNWsee(security:list,*args,**kwargs):
    # 获取流动比率(算术平均)板块多维
    return w.wsee(security,"sec_current_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQuickOverallChNWsee(security:list,*args,**kwargs):
    # 获取速动比率(整体法)板块多维
    return w.wsee(security,"sec_quick_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQuickAvgChNWsee(security:list,*args,**kwargs):
    # 获取速动比率(算术平均)板块多维
    return w.wsee(security,"sec_quick_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityToDebtOverallGLbWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益/负债合计(整体法)板块多维
    return w.wsee(security,"sec_equitytodebt_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityToDebtAvgGLbWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益/负债合计(算术平均)板块多维
    return w.wsee(security,"sec_equitytodebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityToInterestDebtOverallGLbWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益/带息债务(整体法)板块多维
    return w.wsee(security,"sec_equitytointerestdebt_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityToInterestDebtAvgGLbWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益/带息债务(算术平均)板块多维
    return w.wsee(security,"sec_equitytointerestdebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEbItDatoDebtOverallGLbWsee(security:list,*args,**kwargs):
    # 获取息税折旧摊销前利润/负债合计(整体法)板块多维
    return w.wsee(security,"sec_ebitdatodebt_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEbItDatoDebtAvgGLbWsee(security:list,*args,**kwargs):
    # 获取息税折旧摊销前利润/负债合计(算术平均)板块多维
    return w.wsee(security,"sec_ebitdatodebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOCFToDebtOverallChNWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/负债合计(整体法)板块多维
    return w.wsee(security,"sec_ocftodebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOCFToDebtAvgChNWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/负债合计(算术平均)板块多维
    return w.wsee(security,"sec_ocftodebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInterestCoverageAvgChNWsee(security:list,*args,**kwargs):
    # 获取已获利息倍数(算术平均)板块多维
    return w.wsee(security,"sec_interestcoverage_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvTurnOverallChNWsee(security:list,*args,**kwargs):
    # 获取存货周转率(整体法)板块多维
    return w.wsee(security,"sec_invturn_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvTurnAvgChNWsee(security:list,*args,**kwargs):
    # 获取存货周转率(算术平均)板块多维
    return w.wsee(security,"sec_invturn_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecArturNOverallChNWsee(security:list,*args,**kwargs):
    # 获取应收账款周转率(整体法)板块多维
    return w.wsee(security,"sec_arturn_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecArturNAvgChNWsee(security:list,*args,**kwargs):
    # 获取应收账款周转率(算术平均)板块多维
    return w.wsee(security,"sec_arturn_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFaTurnOverallChNWsee(security:list,*args,**kwargs):
    # 获取固定资产周转率(整体法)板块多维
    return w.wsee(security,"sec_faturn_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFaTurnAvgChNWsee(security:list,*args,**kwargs):
    # 获取固定资产周转率(算术平均)板块多维
    return w.wsee(security,"sec_faturn_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecAssetsTurnOverallChNWsee(security:list,*args,**kwargs):
    # 获取总资产周转率(整体法)板块多维
    return w.wsee(security,"sec_assetsturn_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecAssetsTurnAvgChNWsee(security:list,*args,**kwargs):
    # 获取总资产周转率(算术平均)板块多维
    return w.wsee(security,"sec_assetsturn_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTurnDaysOverallChNWsee(security:list,*args,**kwargs):
    # 获取营业周期(整体法)板块多维
    return w.wsee(security,"sec_turndays_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTurnDaysAvgChNWsee(security:list,*args,**kwargs):
    # 获取营业周期(算术平均)板块多维
    return w.wsee(security,"sec_turndays_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvTurnDaysOverallChNWsee(security:list,*args,**kwargs):
    # 获取存货周转天数(整体法)板块多维
    return w.wsee(security,"sec_invturndays_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvTurnDaysAvgChNWsee(security:list,*args,**kwargs):
    # 获取存货周转天数(算术平均)板块多维
    return w.wsee(security,"sec_invturndays_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecArturNDaysOverallChNWsee(security:list,*args,**kwargs):
    # 获取应收账款周转天数(整体法)板块多维
    return w.wsee(security,"sec_arturndays_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecArturNDaysAvgChNWsee(security:list,*args,**kwargs):
    # 获取应收账款周转天数(算术平均)板块多维
    return w.wsee(security,"sec_arturndays_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrSumChNWsee(security:list,*args,**kwargs):
    # 获取营业总收入(合计)板块多维
    return w.wsee(security,"sec_gr_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_gr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRevenueSumGLbWsee(security:list,*args,**kwargs):
    # 获取主营收入(合计)板块多维
    return w.wsee(security,"sec_revenue_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRevenueAvgGLbWsee(security:list,*args,**kwargs):
    # 获取主营收入(算术平均)板块多维
    return w.wsee(security,"sec_revenue_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOtherRevenueSumGLbWsee(security:list,*args,**kwargs):
    # 获取其他营业收入(合计)板块多维
    return w.wsee(security,"sec_otherrevenue_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOtherRevenueAvgGLbWsee(security:list,*args,**kwargs):
    # 获取其他营业收入(算术平均)板块多维
    return w.wsee(security,"sec_otherrevenue_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGcSumGLbWsee(security:list,*args,**kwargs):
    # 获取总营业支出(合计)板块多维
    return w.wsee(security,"sec_gc_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGcAvgGLbWsee(security:list,*args,**kwargs):
    # 获取总营业支出(算术平均)板块多维
    return w.wsee(security,"sec_gc_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOcSumChNWsee(security:list,*args,**kwargs):
    # 获取营业成本(合计)板块多维
    return w.wsee(security,"sec_oc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOcAvgChNWsee(security:list,*args,**kwargs):
    # 获取营业成本(算术平均)板块多维
    return w.wsee(security,"sec_oc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecExpenseSumGLbWsee(security:list,*args,**kwargs):
    # 获取营业开支(合计)板块多维
    return w.wsee(security,"sec_expense_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecExpenseAvgGLbWsee(security:list,*args,**kwargs):
    # 获取营业开支(算术平均)板块多维
    return w.wsee(security,"sec_expense_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityInvpnLSumGLbWsee(security:list,*args,**kwargs):
    # 获取权益性投资损益(合计)板块多维
    return w.wsee(security,"sec_equityinvpnl_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityInvpnLAvgGLbWsee(security:list,*args,**kwargs):
    # 获取权益性投资损益(算术平均)板块多维
    return w.wsee(security,"sec_equityinvpnl_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOpSumChNWsee(security:list,*args,**kwargs):
    # 获取营业利润(合计)板块多维
    return w.wsee(security,"sec_op_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOpAvgChNWsee(security:list,*args,**kwargs):
    # 获取营业利润(算术平均)板块多维
    return w.wsee(security,"sec_op_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEBtSumGLbWsee(security:list,*args,**kwargs):
    # 获取除税前利润(合计)板块多维
    return w.wsee(security,"sec_ebt_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEBtAvgGLbWsee(security:list,*args,**kwargs):
    # 获取除税前利润(算术平均)板块多维
    return w.wsee(security,"sec_ebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTaxSumChNWsee(security:list,*args,**kwargs):
    # 获取所得税(合计)板块多维
    return w.wsee(security,"sec_tax_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTaxAvgChNWsee(security:list,*args,**kwargs):
    # 获取所得税(算术平均)板块多维
    return w.wsee(security,"sec_tax_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNpSumChNWsee(security:list,*args,**kwargs):
    # 获取净利润(合计)板块多维
    return w.wsee(security,"sec_np_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNpAvgChNWsee(security:list,*args,**kwargs):
    # 获取净利润(算术平均)板块多维
    return w.wsee(security,"sec_np_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNpaSpcSumGLbWsee(security:list,*args,**kwargs):
    # 获取归属普通股东净利润(合计)板块多维
    return w.wsee(security,"sec_npaspc_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNpaSpcAvgGLbWsee(security:list,*args,**kwargs):
    # 获取归属普通股东净利润(算术平均)板块多维
    return w.wsee(security,"sec_npaspc_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrossMargin2SumChNWsee(security:list,*args,**kwargs):
    # 获取毛利(合计)板块多维
    return w.wsee(security,"sec_grossmargin2_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrossMargin2AvgChNWsee(security:list,*args,**kwargs):
    # 获取毛利(算术平均)板块多维
    return w.wsee(security,"sec_grossmargin2_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEbItSumGLbWsee(security:list,*args,**kwargs):
    # 获取EBIT(合计)板块多维
    return w.wsee(security,"sec_ebit_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEbItAvgGLbWsee(security:list,*args,**kwargs):
    # 获取EBIT(算术平均)板块多维
    return w.wsee(security,"sec_ebit_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecAssetTotalSumChNWsee(security:list,*args,**kwargs):
    # 获取资产总计(合计)板块多维
    return w.wsee(security,"sec_asset_total_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecAssetTotalAvgChNWsee(security:list,*args,**kwargs):
    # 获取资产总计(算术平均)板块多维
    return w.wsee(security,"sec_asset_total_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCCeSumGLbWsee(security:list,*args,**kwargs):
    # 获取现金及现金等价物(合计)板块多维
    return w.wsee(security,"sec_cce_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCCeAvgGLbWsee(security:list,*args,**kwargs):
    # 获取现金及现金等价物(算术平均)板块多维
    return w.wsee(security,"sec_cce_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTradingFinancialAssetSumChNWsee(security:list,*args,**kwargs):
    # 获取交易性金融资产(合计)板块多维
    return w.wsee(security,"sec_tradingfinancialasset_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTradingFinancialAssetAvgChNWsee(security:list,*args,**kwargs):
    # 获取交易性金融资产(算术平均)板块多维
    return w.wsee(security,"sec_tradingfinancialasset_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecArSumGLbWsee(security:list,*args,**kwargs):
    # 获取应收账款及票据(合计)板块多维
    return w.wsee(security,"sec_ar_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecArAvgGLbWsee(security:list,*args,**kwargs):
    # 获取应收账款及票据(算术平均)板块多维
    return w.wsee(security,"sec_ar_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecIvNenTorySumChNWsee(security:list,*args,**kwargs):
    # 获取存货(合计)板块多维
    return w.wsee(security,"sec_ivnentory_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecIvNenToryAvgChNWsee(security:list,*args,**kwargs):
    # 获取存货(算术平均)板块多维
    return w.wsee(security,"sec_ivnentory_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentAssetSumChNWsee(security:list,*args,**kwargs):
    # 获取流动资产(合计)板块多维
    return w.wsee(security,"sec_currentasset_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentAssetAvgChNWsee(security:list,*args,**kwargs):
    # 获取流动资产(算术平均)板块多维
    return w.wsee(security,"sec_currentasset_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityInvSumGLbWsee(security:list,*args,**kwargs):
    # 获取权益性投资(合计)板块多维
    return w.wsee(security,"sec_equityinv_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityInvAvgGLbWsee(security:list,*args,**kwargs):
    # 获取权益性投资(算术平均)板块多维
    return w.wsee(security,"sec_equityinv_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFixAssetNetValueSumChNWsee(security:list,*args,**kwargs):
    # 获取固定资产净值(合计)板块多维
    return w.wsee(security,"sec_fixassetnetvalue_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFixAssetNetValueAvgChNWsee(security:list,*args,**kwargs):
    # 获取固定资产净值(算术平均)板块多维
    return w.wsee(security,"sec_fixassetnetvalue_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCIpNetValueSumChNWsee(security:list,*args,**kwargs):
    # 获取在建工程(合计)板块多维
    return w.wsee(security,"sec_cipnetvalue_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCIpNetValueAvgChNWsee(security:list,*args,**kwargs):
    # 获取在建工程(算术平均)板块多维
    return w.wsee(security,"sec_cipnetvalue_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNonCurrentAssetSumChNWsee(security:list,*args,**kwargs):
    # 获取非流动资产(合计)板块多维
    return w.wsee(security,"sec_noncurrentasset_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNonCurrentAssetAvgChNWsee(security:list,*args,**kwargs):
    # 获取非流动资产(算术平均)板块多维
    return w.wsee(security,"sec_noncurrentasset_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecApSumGLbWsee(security:list,*args,**kwargs):
    # 获取应付账款及票据(合计)板块多维
    return w.wsee(security,"sec_ap_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecApAvgGLbWsee(security:list,*args,**kwargs):
    # 获取应付账款及票据(算术平均)板块多维
    return w.wsee(security,"sec_ap_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentMaturityOfBorrowingSSumGLbWsee(security:list,*args,**kwargs):
    # 获取短期借贷及长期借贷当期到期部分(合计)板块多维
    return w.wsee(security,"sec_currentmaturityofborrowings_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentMaturityOfBorrowingSAvgGLbWsee(security:list,*args,**kwargs):
    # 获取短期借贷及长期借贷当期到期部分(算术平均)板块多维
    return w.wsee(security,"sec_currentmaturityofborrowings_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentLiabilitySumChNWsee(security:list,*args,**kwargs):
    # 获取流动负债(合计)板块多维
    return w.wsee(security,"sec_currentliability_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCurrentLiabilityAvgChNWsee(security:list,*args,**kwargs):
    # 获取流动负债(算术平均)板块多维
    return w.wsee(security,"sec_currentliability_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecLtDebtSumChNWsee(security:list,*args,**kwargs):
    # 获取长期借款(合计)板块多维
    return w.wsee(security,"sec_ltdebt_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecLtDebtAvgChNWsee(security:list,*args,**kwargs):
    # 获取长期借款(算术平均)板块多维
    return w.wsee(security,"sec_ltdebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNonCurrentLiabilitySumChNWsee(security:list,*args,**kwargs):
    # 获取非流动负债(合计)板块多维
    return w.wsee(security,"sec_noncurrentliability_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNonCurrentLiabilityAvgChNWsee(security:list,*args,**kwargs):
    # 获取非流动负债(算术平均)板块多维
    return w.wsee(security,"sec_noncurrentliability_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquitySumChNWsee(security:list,*args,**kwargs):
    # 获取股东权益(合计)板块多维
    return w.wsee(security,"sec_equity_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEquityAvgChNWsee(security:list,*args,**kwargs):
    # 获取股东权益(算术平均)板块多维
    return w.wsee(security,"sec_equity_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMinorityQuitYSumChNWsee(security:list,*args,**kwargs):
    # 获取少数股东权益(合计)板块多维
    return w.wsee(security,"sec_minorityquity_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMinorityQuitYAvgChNWsee(security:list,*args,**kwargs):
    # 获取少数股东权益(算术平均)板块多维
    return w.wsee(security,"sec_minorityquity_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecReAtAInEarningSumGLbWsee(security:list,*args,**kwargs):
    # 获取留存收益(合计)板块多维
    return w.wsee(security,"sec_reatainearning_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecReAtAInEarningAvgGLbWsee(security:list,*args,**kwargs):
    # 获取留存收益(算术平均)板块多维
    return w.wsee(security,"sec_reatainearning_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecWCapSumGLbWsee(security:list,*args,**kwargs):
    # 获取营运资本(合计)板块多维
    return w.wsee(security,"sec_wcap_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecWCapAvgGLbWsee(security:list,*args,**kwargs):
    # 获取营运资本(算术平均)板块多维
    return w.wsee(security,"sec_wcap_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEAsPcSumChNWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益(合计)板块多维
    return w.wsee(security,"sec_easpc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEAsPcAvgChNWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益(算术平均)板块多维
    return w.wsee(security,"sec_easpc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNcFoASumGLbWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额(合计)板块多维
    return w.wsee(security,"sec_ncfoa_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNcFoAAvgGLbWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额(算术平均)板块多维
    return w.wsee(security,"sec_ncfoa_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNcFiaSumGLbWsee(security:list,*args,**kwargs):
    # 获取投资活动产生的现金流量净额(合计)板块多维
    return w.wsee(security,"sec_ncfia_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNcFiaAvgGLbWsee(security:list,*args,**kwargs):
    # 获取投资活动产生的现金流量净额(算术平均)板块多维
    return w.wsee(security,"sec_ncfia_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNcFfaSumGLbWsee(security:list,*args,**kwargs):
    # 获取筹资活动产生的现金流量净额(合计)板块多维
    return w.wsee(security,"sec_ncffa_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNcFfaAvgGLbWsee(security:list,*args,**kwargs):
    # 获取筹资活动产生的现金流量净额(算术平均)板块多维
    return w.wsee(security,"sec_ncffa_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEffectOfForExonCashSumGLbWsee(security:list,*args,**kwargs):
    # 获取汇率变动对现金的影响(合计)板块多维
    return w.wsee(security,"sec_effectofforexoncash_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEffectOfForExonCashAvgGLbWsee(security:list,*args,**kwargs):
    # 获取汇率变动对现金的影响(算术平均)板块多维
    return w.wsee(security,"sec_effectofforexoncash_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNetIncreaseIncCeSumGLbWsee(security:list,*args,**kwargs):
    # 获取现金及现金等价物净增加额(合计)板块多维
    return w.wsee(security,"sec_netincreaseincce_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNetIncreaseIncCeAvgGLbWsee(security:list,*args,**kwargs):
    # 获取现金及现金等价物净增加额(算术平均)板块多维
    return w.wsee(security,"sec_netincreaseincce_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFcFe2SumGLbWsee(security:list,*args,**kwargs):
    # 获取股权自由现金流量FCFE(合计)板块多维
    return w.wsee(security,"sec_fcfe2_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFcFe2AvgGLbWsee(security:list,*args,**kwargs):
    # 获取股权自由现金流量FCFE(算术平均)板块多维
    return w.wsee(security,"sec_fcfe2_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFcFfSumGLbWsee(security:list,*args,**kwargs):
    # 获取企业自由现金流量(合计)板块多维
    return w.wsee(security,"sec_fcff_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFcFfAvgGLbWsee(security:list,*args,**kwargs):
    # 获取企业自由现金流量(算术平均)板块多维
    return w.wsee(security,"sec_fcff_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNetProfitMarginTtMOverallChNWsee(security:list,*args,**kwargs):
    # 获取销售净利率(TTM)(整体法)板块多维
    return w.wsee(security,"sec_netprofitmargin_ttm_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNetProfitMarginTtMAvgChNWsee(security:list,*args,**kwargs):
    # 获取销售净利率(TTM)(算术平均)板块多维
    return w.wsee(security,"sec_netprofitmargin_ttm_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOperateExpenseToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取销售费用/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_operateexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFaAdminExpenseToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取管理费用/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_fa_adminexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFinaExpenseToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取财务费用/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_finaexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOperateIncomeToEBTOverallChNWsee(security:list,*args,**kwargs):
    # 获取经营活动净收益/利润总额(整体法)板块多维
    return w.wsee(security,"sec_operateincometoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvestIncomeToEBTOverallChNWsee(security:list,*args,**kwargs):
    # 获取价值变动净收益/利润总额(整体法)板块多维
    return w.wsee(security,"sec_investincometoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTaxToEBTOverallChNWsee(security:list,*args,**kwargs):
    # 获取所得税/利润总额(整体法)板块多维
    return w.wsee(security,"sec_taxtoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDeductedProfitToProfitOverallChNWsee(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净利润/净利润(整体法)板块多维
    return w.wsee(security,"sec_deductedprofittoprofit_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecSalesCashIntoOrOverallChNWsee(security:list,*args,**kwargs):
    # 获取销售商品提供劳务收到的现金/营业收入(整体法)板块多维
    return w.wsee(security,"sec_salescashintoor_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecSalesCashIntoOrAvgChNWsee(security:list,*args,**kwargs):
    # 获取销售商品提供劳务收到的现金/营业收入(算术平均)板块多维
    return w.wsee(security,"sec_salescashintoor_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCapeXTodaOverallChNWsee(security:list,*args,**kwargs):
    # 获取资本支出/旧和摊销(整体法)板块多维
    return w.wsee(security,"sec_capextoda_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTotalLiabilityToeAsPcOverallChNWsee(security:list,*args,**kwargs):
    # 获取负债合计/归属母公司股东的权益(整体法)板块多维
    return w.wsee(security,"sec_totalliabilitytoeaspc_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTotalLiabilityToeAsPcAvgChNWsee(security:list,*args,**kwargs):
    # 获取负债合计/归属母公司股东的权益(算术平均)板块多维
    return w.wsee(security,"sec_totalliabilitytoeaspc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInterestBearingDebtToeAsPcOverallChNWsee(security:list,*args,**kwargs):
    # 获取带息债务/归属母公司股东的权益(整体法)板块多维
    return w.wsee(security,"sec_interestbearingdebttoeaspc_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNetLiabilityToeAsPcOverallChNWsee(security:list,*args,**kwargs):
    # 获取净债务/归属母公司股东的权益(整体法)板块多维
    return w.wsee(security,"sec_netliabilitytoeaspc_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecAssetsTurnTtMOverallChNWsee(security:list,*args,**kwargs):
    # 获取资产周转率(TTM)(整体法)板块多维
    return w.wsee(security,"sec_assetsturn_ttm_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecAssetsTurnTtMAvgChNWsee(security:list,*args,**kwargs):
    # 获取资产周转率(TTM)(算术平均)板块多维
    return w.wsee(security,"sec_assetsturn_ttm_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaEpsOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.每股收益EPS(整体法)板块多维
    return w.wsee(security,"sec_qfa_eps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaEpsAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.每股收益EPS(算术平均)板块多维
    return w.wsee(security,"sec_qfa_eps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaRoeDilutedOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.净资产收益率ROE-摊薄(整体法)板块多维
    return w.wsee(security,"sec_qfa_roe_diluted_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaRoeDilutedAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.净资产收益率ROE-摊薄(算术平均)板块多维
    return w.wsee(security,"sec_qfa_roe_diluted_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaDeductedRoeDilutedOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.扣除非经常损益后的净资产收益率-摊薄(整体法)板块多维
    return w.wsee(security,"sec_qfa_deductedroe_diluted_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaDeductedRoeDilutedAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.扣除非经常损益后的净资产收益率-摊薄(算术平均)板块多维
    return w.wsee(security,"sec_qfa_deductedroe_diluted_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaRoaOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.总资产净利率(整体法)板块多维
    return w.wsee(security,"sec_qfa_roa_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaRoaAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.总资产净利率(算术平均)板块多维
    return w.wsee(security,"sec_qfa_roa_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaNetProfitMarginOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.销售净利率(整体法)板块多维
    return w.wsee(security,"sec_qfa_netprofitmargin_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaNetProfitMarginAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.销售净利率(算术平均)板块多维
    return w.wsee(security,"sec_qfa_netprofitmargin_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaGrossProfitMarginOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.销售毛利率(整体法)板块多维
    return w.wsee(security,"sec_qfa_grossprofitmargin_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaGrossProfitMarginAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.销售毛利率(算术平均)板块多维
    return w.wsee(security,"sec_qfa_grossprofitmargin_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaGcToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业总成本/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_qfa_gctogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaGcToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业总成本/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_qfa_gctogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOpToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业利润/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_qfa_optogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOpToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业利润/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_qfa_optogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaProfitToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.净利润/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_qfa_profittogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaProfitToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.净利润/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_qfa_profittogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOperateExpenseToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.销售费用/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_qfa_operateexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOperateExpenseToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.销售费用/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_qfa_operateexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaAdminExpenseToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.管理费用/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_qfa_adminexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaAdminExpenseToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.管理费用/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_qfa_adminexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaFinaExpenseToGrOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.财务费用/营业总收入(整体法)板块多维
    return w.wsee(security,"sec_qfa_finaexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaFinaExpenseToGrAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.财务费用/营业总收入(算术平均)板块多维
    return w.wsee(security,"sec_qfa_finaexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOperateIncomeToEBTOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.经营活动净收益/利润总额(整体法)板块多维
    return w.wsee(security,"sec_qfa_operateincometoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOperateIncomeToEBTAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.经营活动净收益/利润总额(算术平均)板块多维
    return w.wsee(security,"sec_qfa_operateincometoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaInvestIncomeToEBTOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.价值变动净收益/利润总额(整体法)板块多维
    return w.wsee(security,"sec_qfa_investincometoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaInvestIncomeToEBTAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.价值变动净收益/利润总额(算术平均)板块多维
    return w.wsee(security,"sec_qfa_investincometoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaDeductedProfitToProfitOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.扣除非经常损益后的净利润/净利润(整体法)板块多维
    return w.wsee(security,"sec_qfa_deductedprofittoprofit_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaDeductedProfitToProfitAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.扣除非经常损益后的净利润/净利润(算术平均)板块多维
    return w.wsee(security,"sec_qfa_deductedprofittoprofit_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaSalesCashIntoOrOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.销售商品提供劳务收到的现金/营业收入(整体法)板块多维
    return w.wsee(security,"sec_qfa_salescashintoor_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaSalesCashIntoOrAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.销售商品提供劳务收到的现金/营业收入(算术平均)板块多维
    return w.wsee(security,"sec_qfa_salescashintoor_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOCFToOrOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.经营活动产生的现金流量净额/营业收入(整体法)板块多维
    return w.wsee(security,"sec_qfa_ocftoor_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOCFToOrAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.经营活动产生的现金流量净额/营业收入(算术平均)板块多维
    return w.wsee(security,"sec_qfa_ocftoor_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOCFToOperateIncomeOverallChNWsee(security:list,*args,**kwargs):
    # 获取单季度.经营活动产生的现金流量净额/经营活动净收益(整体法)板块多维
    return w.wsee(security,"sec_qfa_ocftooperateincome_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOCFToOperateIncomeAvgChNWsee(security:list,*args,**kwargs):
    # 获取单季度.经营活动产生的现金流量净额/经营活动净收益(算术平均)板块多维
    return w.wsee(security,"sec_qfa_ocftooperateincome_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaGrTotalYoYChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业总收入合计(同比增长率)板块多维
    return w.wsee(security,"sec_qfa_gr_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaGrTotalMomChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业总收入合计(环比增长率)板块多维
    return w.wsee(security,"sec_qfa_gr_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaRevenueTotalYoYChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业收入合计(同比增长率)板块多维
    return w.wsee(security,"sec_qfa_revenue_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaRevenueTotalMomChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业收入合计(环比增长率)板块多维
    return w.wsee(security,"sec_qfa_revenue_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOpTotalYoYChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业利润合计(同比增长率)板块多维
    return w.wsee(security,"sec_qfa_op_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaOpTotalMomChNWsee(security:list,*args,**kwargs):
    # 获取单季度.营业利润合计(环比增长率)板块多维
    return w.wsee(security,"sec_qfa_op_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaNpTotalYoYChNWsee(security:list,*args,**kwargs):
    # 获取单季度.净利润合计(同比增长率)板块多维
    return w.wsee(security,"sec_qfa_np_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaNpTotalMomChNWsee(security:list,*args,**kwargs):
    # 获取单季度.净利润合计(环比增长率)板块多维
    return w.wsee(security,"sec_qfa_np_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaNpaSpcTotalYoYChNWsee(security:list,*args,**kwargs):
    # 获取单季度.归属母公司股东的净利润合计(同比增长率)板块多维
    return w.wsee(security,"sec_qfa_npaspc_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecQfaNpaSpcTotalMomChNWsee(security:list,*args,**kwargs):
    # 获取单季度.归属母公司股东的净利润合计(环比增长率)板块多维
    return w.wsee(security,"sec_qfa_npaspc_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGcSumChNWsee(security:list,*args,**kwargs):
    # 获取营业总成本(合计)板块多维
    return w.wsee(security,"sec_gc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGcAvgChNWsee(security:list,*args,**kwargs):
    # 获取营业总成本(算术平均)板块多维
    return w.wsee(security,"sec_gc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOrSumChNWsee(security:list,*args,**kwargs):
    # 获取营业收入(合计)板块多维
    return w.wsee(security,"sec_or_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOrAvgChNWsee(security:list,*args,**kwargs):
    # 获取营业收入(算术平均)板块多维
    return w.wsee(security,"sec_or_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecSellingExpSumChNWsee(security:list,*args,**kwargs):
    # 获取销售费用(合计)板块多维
    return w.wsee(security,"sec_sellingexp_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecSellingExpAvgChNWsee(security:list,*args,**kwargs):
    # 获取销售费用(算术平均)板块多维
    return w.wsee(security,"sec_sellingexp_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMNgtExpSumChNWsee(security:list,*args,**kwargs):
    # 获取管理费用(合计)板块多维
    return w.wsee(security,"sec_mngtexp_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecMNgtExpAvgChNWsee(security:list,*args,**kwargs):
    # 获取管理费用(算术平均)板块多维
    return w.wsee(security,"sec_mngtexp_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFineXpSumChNWsee(security:list,*args,**kwargs):
    # 获取财务费用(合计)板块多维
    return w.wsee(security,"sec_finexp_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecFineXpAvgChNWsee(security:list,*args,**kwargs):
    # 获取财务费用(算术平均)板块多维
    return w.wsee(security,"sec_finexp_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNiOnInvestmentSumChNWsee(security:list,*args,**kwargs):
    # 获取投资净收益(合计)板块多维
    return w.wsee(security,"sec_nioninvestment_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNiOnInvestmentAvgChNWsee(security:list,*args,**kwargs):
    # 获取投资净收益(算术平均)板块多维
    return w.wsee(security,"sec_nioninvestment_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNiOnForExSumChNWsee(security:list,*args,**kwargs):
    # 获取汇兑净收益(合计)板块多维
    return w.wsee(security,"sec_nionforex_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNiOnForExAvgChNWsee(security:list,*args,**kwargs):
    # 获取汇兑净收益(算术平均)板块多维
    return w.wsee(security,"sec_nionforex_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNiFromChangesInFvSumChNWsee(security:list,*args,**kwargs):
    # 获取公允价值变动净收益(合计)板块多维
    return w.wsee(security,"sec_nifromchangesinfv_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNiFromChangesInFvAvgChNWsee(security:list,*args,**kwargs):
    # 获取公允价值变动净收益(算术平均)板块多维
    return w.wsee(security,"sec_nifromchangesinfv_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEBtSumChNWsee(security:list,*args,**kwargs):
    # 获取利润总额(合计)板块多维
    return w.wsee(security,"sec_ebt_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEBtAvgChNWsee(security:list,*args,**kwargs):
    # 获取利润总额(算术平均)板块多维
    return w.wsee(security,"sec_ebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNpaSpcSumChNWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润(合计)板块多维
    return w.wsee(security,"sec_npaspc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNpaSpcAvgChNWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润(算术平均)板块多维
    return w.wsee(security,"sec_npaspc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecExNonRecurringPnLnPasPcSumChNWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润-扣除非经常损益(合计)板块多维
    return w.wsee(security,"sec_exnonrecurringpnlnpaspc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecExNonRecurringPnLnPasPcAvgChNWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润-扣除非经常损益(算术平均)板块多维
    return w.wsee(security,"sec_exnonrecurringpnlnpaspc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOperateIncomeSumChNWsee(security:list,*args,**kwargs):
    # 获取经营活动净收益(合计)板块多维
    return w.wsee(security,"sec_operateincome_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOperateIncomeAvgChNWsee(security:list,*args,**kwargs):
    # 获取经营活动净收益(算术平均)板块多维
    return w.wsee(security,"sec_operateincome_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvestIncomeSumChNWsee(security:list,*args,**kwargs):
    # 获取价值变动净收益(合计)板块多维
    return w.wsee(security,"sec_investincome_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvestIncomeAvgChNWsee(security:list,*args,**kwargs):
    # 获取价值变动净收益(算术平均)板块多维
    return w.wsee(security,"sec_investincome_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCashSumChNWsee(security:list,*args,**kwargs):
    # 获取货币资金(合计)板块多维
    return w.wsee(security,"sec_cash_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCashAvgChNWsee(security:list,*args,**kwargs):
    # 获取货币资金(算术平均)板块多维
    return w.wsee(security,"sec_cash_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNotErSumChNWsee(security:list,*args,**kwargs):
    # 获取应收票据(合计)板块多维
    return w.wsee(security,"sec_noter_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNotErAvgChNWsee(security:list,*args,**kwargs):
    # 获取应收票据(算术平均)板块多维
    return w.wsee(security,"sec_noter_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecArSumChNWsee(security:list,*args,**kwargs):
    # 获取应收账款(合计)板块多维
    return w.wsee(security,"sec_ar_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecArAvgChNWsee(security:list,*args,**kwargs):
    # 获取应收账款(算术平均)板块多维
    return w.wsee(security,"sec_ar_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecLteQtInvestmentSumChNWsee(security:list,*args,**kwargs):
    # 获取长期股权投资(合计)板块多维
    return w.wsee(security,"sec_lteqtinvestment_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecLteQtInvestmentAvgChNWsee(security:list,*args,**kwargs):
    # 获取长期股权投资(算术平均)板块多维
    return w.wsee(security,"sec_lteqtinvestment_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvestmentReSumChNWsee(security:list,*args,**kwargs):
    # 获取投资性房地产(合计)板块多维
    return w.wsee(security,"sec_investmentre_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecInvestmentReAvgChNWsee(security:list,*args,**kwargs):
    # 获取投资性房地产(算术平均)板块多维
    return w.wsee(security,"sec_investmentre_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecStDebtSumChNWsee(security:list,*args,**kwargs):
    # 获取短期借款(合计)板块多维
    return w.wsee(security,"sec_stdebt_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecStDebtAvgChNWsee(security:list,*args,**kwargs):
    # 获取短期借款(算术平均)板块多维
    return w.wsee(security,"sec_stdebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNotEpSumChNWsee(security:list,*args,**kwargs):
    # 获取应付票据(合计)板块多维
    return w.wsee(security,"sec_notep_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNotEpAvgChNWsee(security:list,*args,**kwargs):
    # 获取应付票据(算术平均)板块多维
    return w.wsee(security,"sec_notep_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecApSumChNWsee(security:list,*args,**kwargs):
    # 获取应付账款(合计)板块多维
    return w.wsee(security,"sec_ap_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecApAvgChNWsee(security:list,*args,**kwargs):
    # 获取应付账款(算术平均)板块多维
    return w.wsee(security,"sec_ap_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecGrYoYTotalChNWsee(security:list,*args,**kwargs):
    # 获取营业总收入合计(同比增长率)板块多维
    return w.wsee(security,"sec_gr_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecRevenueYoYTotalChNWsee(security:list,*args,**kwargs):
    # 获取营业收入合计(同比增长率)板块多维
    return w.wsee(security,"sec_revenue_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecOpYoYTotalChNWsee(security:list,*args,**kwargs):
    # 获取营业利润合计(同比增长率)板块多维
    return w.wsee(security,"sec_op_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNpSumYoYGLbWsee(security:list,*args,**kwargs):
    # 获取净利润合计(同比增长率)板块多维
    return w.wsee(security,"sec_np_sum_yoy_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecNpaSpcYoYTotalChNWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润合计(同比增长率)板块多维
    return w.wsee(security,"sec_npaspc_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCfOAYoYTotalChNWsee(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额合计(同比增长率)板块多维
    return w.wsee(security,"sec_cfoa_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCFiaSumYoYGLbWsee(security:list,*args,**kwargs):
    # 获取投资活动产生的现金流量净额合计(同比增长率)板块多维
    return w.wsee(security,"sec_cfia_sum_yoy_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCffASumYoYGLbWsee(security:list,*args,**kwargs):
    # 获取筹资活动产生的现金流量净额合计(同比增长率)板块多维
    return w.wsee(security,"sec_cffa_sum_yoy_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecCCeNetIncreaseSumYoYGLbWsee(security:list,*args,**kwargs):
    # 获取现金及现金等价物净增加额合计(同比增长率)板块多维
    return w.wsee(security,"sec_cce_netincrease_sum_yoy_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDupontRoeOverallYoYChNWsee(security:list,*args,**kwargs):
    # 获取净资产收益率(整体法)(同比增长率)板块多维
    return w.wsee(security,"sec_dupont_roe_overall_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecDupontRoeAvgYoYChNWsee(security:list,*args,**kwargs):
    # 获取净资产收益率(算术平均)(同比增长率)板块多维
    return w.wsee(security,"sec_dupont_roe_avg_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecBpSOverallGtBYearChNWsee(security:list,*args,**kwargs):
    # 获取每股净资产(整体法)(相对年初增长率)板块多维
    return w.wsee(security,"sec_bps_overall_gtbyear_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecBpSAvgGtBgYearChNWsee(security:list,*args,**kwargs):
    # 获取每股净资产(算术平均)(相对年初增长率)板块多维
    return w.wsee(security,"sec_bps_avg_gtbgyear_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTotalAssetTotalGtBYearChNWsee(security:list,*args,**kwargs):
    # 获取资产总计合计(相对年初增长率)板块多维
    return w.wsee(security,"sec_totalasset_total_gtbyear_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecTotalEquityAsPcTotalGtBYearChNWsee(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益合计(相对年初增长率)板块多维
    return w.wsee(security,"sec_totalequityaspc_total_gtbyear_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWsee
def getSecEBtYoYTotalChNWsee(security:list,*args,**kwargs):
    # 获取利润总额合计(同比增长率)板块多维
    return w.wsee(security,"sec_ebt_yoy_total_chn",*args,**kwargs,usedf=True)