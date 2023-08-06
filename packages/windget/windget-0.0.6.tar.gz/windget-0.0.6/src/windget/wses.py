#!/usr/bin/python
# coding = utf-8
import numpy as np
import pandas as pd
from WindPy import w
def convertInputSecurityTypeForWses(func):
    def convertedFunc(*args):
        args = tuple((i.strftime("%Y-%m-%d") if hasattr(i,"strftime") else i for i in args))
        if type(args[0])==type(''):
            return func(*args)[1].fillna(np.nan)
        else:
            security = args[0]
            args = args[1:]
            return func(",".join(security),*args)[1].fillna(np.nan)
    return convertedFunc
@convertInputSecurityTypeForWses
def getSecCloseAvgWses(security:list,*args,**kwargs):
    # 获取收盘价(算术平均)板块序列
    return w.wses(security,"sec_close_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCloseTsWavGWses(security:list,*args,**kwargs):
    # 获取收盘价(总股本加权平均)板块序列
    return w.wses(security,"sec_close_tswavg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCloseFfsWavGChNWses(security:list,*args,**kwargs):
    # 获取收盘价(流通股本加权平均)(中国)板块序列
    return w.wses(security,"sec_close_ffswavg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTurnAvgWses(security:list,*args,**kwargs):
    # 获取换手率(算术平均)板块序列
    return w.wses(security,"sec_turn_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTurnTMcWavGWses(security:list,*args,**kwargs):
    # 获取换手率(总市值加权平均)板块序列
    return w.wses(security,"sec_turn_tmc_wavg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTurnFfMcWavGWses(security:list,*args,**kwargs):
    # 获取换手率(流通市值加权平均)板块序列
    return w.wses(security,"sec_turn_ffmc_wavg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecVolumeSumWses(security:list,*args,**kwargs):
    # 获取成交量(合计)板块序列
    return w.wses(security,"sec_volume_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecAmountSumWses(security:list,*args,**kwargs):
    # 获取成交金额(合计)板块序列
    return w.wses(security,"sec_amount_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareTotalSumWses(security:list,*args,**kwargs):
    # 获取总股本(合计)板块序列
    return w.wses(security,"sec_share_total_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareTotalAvgWses(security:list,*args,**kwargs):
    # 获取总股本(算术平均)板块序列
    return w.wses(security,"sec_share_total_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareFloatASumWses(security:list,*args,**kwargs):
    # 获取流通A股(合计)板块序列
    return w.wses(security,"sec_share_float_a_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareFloatAAvgWses(security:list,*args,**kwargs):
    # 获取流通A股(算术平均)板块序列
    return w.wses(security,"sec_share_float_a_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareFloatBSumWses(security:list,*args,**kwargs):
    # 获取流通B股(合计)板块序列
    return w.wses(security,"sec_share_float_b_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareFloatBAvgWses(security:list,*args,**kwargs):
    # 获取流通B股(算术平均)板块序列
    return w.wses(security,"sec_share_float_b_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareFloatHSumWses(security:list,*args,**kwargs):
    # 获取流通H股(合计)板块序列
    return w.wses(security,"sec_share_float_h_sum",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareFloatHAvgWses(security:list,*args,**kwargs):
    # 获取流通H股(算术平均)板块序列
    return w.wses(security,"sec_share_float_h_avg",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareFloatTotalSumChNWses(security:list,*args,**kwargs):
    # 获取总流通股本(合计)(中国)板块序列
    return w.wses(security,"sec_share_float_total_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareFloatTotalAvgChNWses(security:list,*args,**kwargs):
    # 获取总流通股本(算术平均)(中国)板块序列
    return w.wses(security,"sec_share_float_total_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareTotalNonLiqSumChNWses(security:list,*args,**kwargs):
    # 获取非流通股(合计)(中国)板块序列
    return w.wses(security,"sec_share_totalnonliq_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecShareTotalNonLiqAvgChNWses(security:list,*args,**kwargs):
    # 获取非流通股(算术平均)(中国)板块序列
    return w.wses(security,"sec_share_totalnonliq_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecWestEpsOverallChNWses(security:list,*args,**kwargs):
    # 获取预测每股收益(整体法)板块序列
    return w.wses(security,"sec_west_eps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecWestEpsAvgChNWses(security:list,*args,**kwargs):
    # 获取预测每股收益(算术平均)板块序列
    return w.wses(security,"sec_west_eps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecWestNpSumChNWses(security:list,*args,**kwargs):
    # 获取预测净利润(合计)板块序列
    return w.wses(security,"sec_west_np_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecWestNpAvgChNWses(security:list,*args,**kwargs):
    # 获取预测净利润(算术平均)板块序列
    return w.wses(security,"sec_west_np_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecWestRevenueSumChNWses(security:list,*args,**kwargs):
    # 获取预测主营业务收入(合计)板块序列
    return w.wses(security,"sec_west_revenue_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecWestRevenueAvgChNWses(security:list,*args,**kwargs):
    # 获取预测主营业务收入(算术平均)板块序列
    return w.wses(security,"sec_west_revenue_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNCashInFlowDSumChNWses(security:list,*args,**kwargs):
    # 获取(日)净流入资金(合计)板块序列
    return w.wses(security,"sec_ncashinflow_d_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNCashInFlowDAvgChNWses(security:list,*args,**kwargs):
    # 获取(日)净流入资金(算术平均)板块序列
    return w.wses(security,"sec_ncashinflow_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNVolInFlowDSumChNWses(security:list,*args,**kwargs):
    # 获取(日)净流入量(合计)板块序列
    return w.wses(security,"sec_nvolinflow_d_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNVolInFlowDAvgChNWses(security:list,*args,**kwargs):
    # 获取(日)净流入量(算术平均)板块序列
    return w.wses(security,"sec_nvolinflow_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNClosingInFlowDSumChNWses(security:list,*args,**kwargs):
    # 获取(日)尾盘净流入资金(合计)板块序列
    return w.wses(security,"sec_nclosinginflow_d_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNClosingInFlowDAvgChNWses(security:list,*args,**kwargs):
    # 获取(日)尾盘净流入资金(算术平均)板块序列
    return w.wses(security,"sec_nclosinginflow_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNOpeningInFlowDSumChNWses(security:list,*args,**kwargs):
    # 获取(日)开盘净流入资金(合计)板块序列
    return w.wses(security,"sec_nopeninginflow_d_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNOpeningInFlowDAvgChNWses(security:list,*args,**kwargs):
    # 获取(日)开盘净流入资金(算术平均)板块序列
    return w.wses(security,"sec_nopeninginflow_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCInFlowRateDOverallChNWses(security:list,*args,**kwargs):
    # 获取(日)金额流入率(整体法)板块序列
    return w.wses(security,"sec_cinflowrate_d_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCInFlowRateDAvgChNWses(security:list,*args,**kwargs):
    # 获取(日)金额流入率(算术平均)板块序列
    return w.wses(security,"sec_cinflowrate_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCashDirectionPecDOverallChNWses(security:list,*args,**kwargs):
    # 获取(日)资金流向占比(整体法)板块序列
    return w.wses(security,"sec_cashdirectionpec_d_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCashDirectionPecDAvgChNWses(security:list,*args,**kwargs):
    # 获取(日)资金流向占比(算术平均)板块序列
    return w.wses(security,"sec_cashdirectionpec_d_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapSumGLbWses(security:list,*args,**kwargs):
    # 获取总市值(合计)板块序列
    return w.wses(security,"sec_mkt_cap_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapAvgGLbWses(security:list,*args,**kwargs):
    # 获取总市值(算术平均)板块序列
    return w.wses(security,"sec_mkt_cap_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMvArdSumGLbWses(security:list,*args,**kwargs):
    # 获取总市值2(合计)板块序列
    return w.wses(security,"sec_mv_ard_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMvArdAvgGLbWses(security:list,*args,**kwargs):
    # 获取总市值2(算术平均)板块序列
    return w.wses(security,"sec_mv_ard_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPeTtMAvgChNWses(security:list,*args,**kwargs):
    # 获取市盈率(TTM-算术平均法)板块序列
    return w.wses(security,"sec_pe_ttm_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPetTmMediaChNWses(security:list,*args,**kwargs):
    # 获取市盈率(TTM-中值)板块序列
    return w.wses(security,"sec_pettm_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPeAvgChNWses(security:list,*args,**kwargs):
    # 获取市盈率(算术平均)板块序列
    return w.wses(security,"sec_pe_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPeMediaChNWses(security:list,*args,**kwargs):
    # 获取市盈率(中值)板块序列
    return w.wses(security,"sec_pe_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPbAvgChNWses(security:list,*args,**kwargs):
    # 获取市净率(算术平均)板块序列
    return w.wses(security,"sec_pb_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPbMediaChNWses(security:list,*args,**kwargs):
    # 获取市净率(中值)板块序列
    return w.wses(security,"sec_pb_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPcfAvgChNWses(security:list,*args,**kwargs):
    # 获取市现率(算术平均)板块序列
    return w.wses(security,"sec_pcf_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPcfMediaChNWses(security:list,*args,**kwargs):
    # 获取市现率(中值)板块序列
    return w.wses(security,"sec_pcf_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPsAvgChNWses(security:list,*args,**kwargs):
    # 获取市销率(算术平均)板块序列
    return w.wses(security,"sec_ps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPsMediaChNWses(security:list,*args,**kwargs):
    # 获取市销率(中值)板块序列
    return w.wses(security,"sec_ps_media_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPeTtMOverallChNWses(security:list,*args,**kwargs):
    # 获取市盈率(TTM-整体法)板块序列
    return w.wses(security,"sec_pe_ttm_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPbOverallChNWses(security:list,*args,**kwargs):
    # 获取市净率(整体法)板块序列
    return w.wses(security,"sec_pb_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPcfOverallChNWses(security:list,*args,**kwargs):
    # 获取市现率(整体法)板块序列
    return w.wses(security,"sec_pcf_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPcfMediaLastEstChNWses(security:list,*args,**kwargs):
    # 获取市净率(最新-中值)板块序列
    return w.wses(security,"sec_pcf_media_lastest_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecPsOverallChNWses(security:list,*args,**kwargs):
    # 获取市销率(整体法)板块序列
    return w.wses(security,"sec_ps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapTodaySumChNWses(security:list,*args,**kwargs):
    # 获取当日总市值(合计)板块序列
    return w.wses(security,"sec_mkt_cap_today_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapTodayAvgChNWses(security:list,*args,**kwargs):
    # 获取当日总市值(算术平均)板块序列
    return w.wses(security,"sec_mkt_cap_today_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapFloatASharesSumChNWses(security:list,*args,**kwargs):
    # 获取流通A股市值(合计)板块序列
    return w.wses(security,"sec_mkt_cap_float_ashares_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapFloatASharesAvgChNWses(security:list,*args,**kwargs):
    # 获取流通A股市值(算术平均)板块序列
    return w.wses(security,"sec_mkt_cap_float_ashares_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapFloatBSharesSumChNWses(security:list,*args,**kwargs):
    # 获取流通B股市值(合计)板块序列
    return w.wses(security,"sec_mkt_cap_float_bshares_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapFloatBSharesAvgChNWses(security:list,*args,**kwargs):
    # 获取流通B股市值(算术平均)板块序列
    return w.wses(security,"sec_mkt_cap_float_bshares_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapFloatFreeSharesSumChNWses(security:list,*args,**kwargs):
    # 获取自由流通市值(合计)板块序列
    return w.wses(security,"sec_mkt_cap_float_freeshares_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMktCapFloatFreeSharesAvgChNWses(security:list,*args,**kwargs):
    # 获取自由流通市值(算术平均)板块序列
    return w.wses(security,"sec_mkt_cap_float_freeshares_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskAnnualYeIlD100WAvgChNWses(security:list,*args,**kwargs):
    # 获取年化收益率算术平均(最近100周)板块序列
    return w.wses(security,"sec_risk_annualyeild_100w_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskAnnualYeIlD24MAvgChNWses(security:list,*args,**kwargs):
    # 获取年化收益率算术平均(最近24个月)板块序列
    return w.wses(security,"sec_risk_annualyeild_24m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskAnnualYeIlD60MAvgChNWses(security:list,*args,**kwargs):
    # 获取年化收益率算术平均(最近60个月)板块序列
    return w.wses(security,"sec_risk_annualyeild_60m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskStDevYearly100WAvgChNWses(security:list,*args,**kwargs):
    # 获取年化波动率算术平均(最近100周)板块序列
    return w.wses(security,"sec_risk_stdevyearly_100w_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskStDevYearly24MAvgChNWses(security:list,*args,**kwargs):
    # 获取年化波动率算术平均(最近24个月)板块序列
    return w.wses(security,"sec_risk_stdevyearly_24m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskStDevYearly60MAvgChNWses(security:list,*args,**kwargs):
    # 获取年化波动率算术平均(最近60个月)板块序列
    return w.wses(security,"sec_risk_stdevyearly_60m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskBeta100WAvgChNWses(security:list,*args,**kwargs):
    # 获取BETA值算术平均(最近100周)板块序列
    return w.wses(security,"sec_risk_beta_100w_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskBeta24MAvgChNWses(security:list,*args,**kwargs):
    # 获取BETA值算术平均(最近24个月)板块序列
    return w.wses(security,"sec_risk_beta_24m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRiskBeta60MAvgChNWses(security:list,*args,**kwargs):
    # 获取BETA值算术平均(最近60个月)板块序列
    return w.wses(security,"sec_risk_beta_60m_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCsrCStatListCompNumChNWses(security:list,*args,**kwargs):
    # 获取上市公司家数板块序列
    return w.wses(security,"sec_csrc_statlistcompnum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCsrCStatShareTotalChNWses(security:list,*args,**kwargs):
    # 获取上市公司境内总股本板块序列
    return w.wses(security,"sec_csrc_stat_sharetotal_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCsrCStatMvChNWses(security:list,*args,**kwargs):
    # 获取上市公司境内总市值板块序列
    return w.wses(security,"sec_csrc_stat_mv_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCsrCStatPeChNWses(security:list,*args,**kwargs):
    # 获取市场静态市盈率板块序列
    return w.wses(security,"sec_csrc_stat_pe_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCsrCStatPbChNWses(security:list,*args,**kwargs):
    # 获取市场静态市净率板块序列
    return w.wses(security,"sec_csrc_stat_pb_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCsrCStatNpTtMChNWses(security:list,*args,**kwargs):
    # 获取上市公司境内股本对应的归属母公司净利润TTM板块序列
    return w.wses(security,"sec_csrc_stat_np_ttm_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCsrCStatPeTtMChNWses(security:list,*args,**kwargs):
    # 获取市场滚动市盈率板块序列
    return w.wses(security,"sec_csrc_stat_pe_ttm_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEpsBasic2AvgChNWses(security:list,*args,**kwargs):
    # 获取每股收益EPS-基本(算术平均)板块序列
    return w.wses(security,"sec_eps_basic2_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEpsDiluted4AvgChNWses(security:list,*args,**kwargs):
    # 获取每股收益EPS-稀释(算术平均)板块序列
    return w.wses(security,"sec_eps_diluted4_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEndingSharesEpsBasic2OverallChNWses(security:list,*args,**kwargs):
    # 获取每股收益EPS-期末股本摊薄(整体法)板块序列
    return w.wses(security,"sec_endingshareseps_basic2_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEndingSharesEpsBasic2AvgChNWses(security:list,*args,**kwargs):
    # 获取每股收益EPS-期末股本摊薄(算术平均)板块序列
    return w.wses(security,"sec_endingshareseps_basic2_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecBpSOverallChNWses(security:list,*args,**kwargs):
    # 获取每股净资产(整体法)板块序列
    return w.wses(security,"sec_bps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecBpSAvgChNWses(security:list,*args,**kwargs):
    # 获取每股净资产(算术平均)板块序列
    return w.wses(security,"sec_bps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrpSOverallChNWses(security:list,*args,**kwargs):
    # 获取每股营业总收入(整体法)板块序列
    return w.wses(security,"sec_grps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrpSAvgChNWses(security:list,*args,**kwargs):
    # 获取每股营业总收入(算术平均)板块序列
    return w.wses(security,"sec_grps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRetainedPsOverallChNWses(security:list,*args,**kwargs):
    # 获取每股留存收益(整体法)板块序列
    return w.wses(security,"sec_retainedps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRetainedPsAvgChNWses(security:list,*args,**kwargs):
    # 获取每股留存收益(算术平均)板块序列
    return w.wses(security,"sec_retainedps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCfpSOverallChNWses(security:list,*args,**kwargs):
    # 获取每股现金流量净额(整体法)板块序列
    return w.wses(security,"sec_cfps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCfpSAvgChNWses(security:list,*args,**kwargs):
    # 获取每股现金流量净额(算术平均)板块序列
    return w.wses(security,"sec_cfps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOcFps2OverallChNWses(security:list,*args,**kwargs):
    # 获取每股经营活动产生的现金流量净额(整体法)板块序列
    return w.wses(security,"sec_ocfps2_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOcFps2AvgChNWses(security:list,*args,**kwargs):
    # 获取每股经营活动产生的现金流量净额(算术平均)板块序列
    return w.wses(security,"sec_ocfps2_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEbItPsAvgGLbWses(security:list,*args,**kwargs):
    # 获取每股息税前利润(算术平均)板块序列
    return w.wses(security,"sec_ebitps_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFcFFpsOverallGLbWses(security:list,*args,**kwargs):
    # 获取每股企业自由现金流量(整体法)板块序列
    return w.wses(security,"sec_fcffps_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFcFFpsAvgGLbWses(security:list,*args,**kwargs):
    # 获取每股企业自由现金流量(算术平均)板块序列
    return w.wses(security,"sec_fcffps_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFcFEpsOverallGLbWses(security:list,*args,**kwargs):
    # 获取每股股东自由现金流量(整体法)板块序列
    return w.wses(security,"sec_fcfeps_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFcFEpsAvgGLbWses(security:list,*args,**kwargs):
    # 获取每股股东自由现金流量(算术平均)板块序列
    return w.wses(security,"sec_fcfeps_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoeAvgOverallChNWses(security:list,*args,**kwargs):
    # 获取净资产收益率-平均(整体法)板块序列
    return w.wses(security,"sec_roe_avg_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoeAvgAvgChNWses(security:list,*args,**kwargs):
    # 获取净资产收益率-平均(算术平均)板块序列
    return w.wses(security,"sec_roe_avg_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoeDilutedOverallChNWses(security:list,*args,**kwargs):
    # 获取净资产收益率-摊薄(整体法)板块序列
    return w.wses(security,"sec_roe_diluted_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoeDilutedAvgChNWses(security:list,*args,**kwargs):
    # 获取净资产收益率-摊薄(算术平均)板块序列
    return w.wses(security,"sec_roe_diluted_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDeductedRoeAvgOverallChNWses(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净资产收益率-平均(整体法)板块序列
    return w.wses(security,"sec_deductedroe_avg_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDeductedRoeAvgAvgChNWses(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净资产收益率-平均(算术平均)板块序列
    return w.wses(security,"sec_deductedroe_avg_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDeductedRoeDilutedOverallChNWses(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净资产收益率-摊薄(整体法)板块序列
    return w.wses(security,"sec_deductedroe_diluted_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDeductedRoeDilutedAvgChNWses(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净资产收益率-摊薄(算术平均)板块序列
    return w.wses(security,"sec_deductedroe_diluted_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoa2OverallGLbWses(security:list,*args,**kwargs):
    # 获取总资产报酬率(整体法)板块序列
    return w.wses(security,"sec_roa2_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoa2AvgGLbWses(security:list,*args,**kwargs):
    # 获取总资产报酬率(算术平均)板块序列
    return w.wses(security,"sec_roa2_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoaOverallChNWses(security:list,*args,**kwargs):
    # 获取总资产净利率(整体法)板块序列
    return w.wses(security,"sec_roa_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoaAvgChNWses(security:list,*args,**kwargs):
    # 获取总资产净利率(算术平均)板块序列
    return w.wses(security,"sec_roa_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrossProfitMarginOverallChNWses(security:list,*args,**kwargs):
    # 获取销售毛利率(整体法)板块序列
    return w.wses(security,"sec_grossprofitmargin_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrossProfitMarginAvgChNWses(security:list,*args,**kwargs):
    # 获取销售毛利率(算术平均)板块序列
    return w.wses(security,"sec_grossprofitmargin_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNetProfitMarginOverallChNWses(security:list,*args,**kwargs):
    # 获取销售净利率(整体法)板块序列
    return w.wses(security,"sec_netprofitmargin_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNetProfitMarginAvgChNWses(security:list,*args,**kwargs):
    # 获取销售净利率(算术平均)板块序列
    return w.wses(security,"sec_netprofitmargin_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGcToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取营业总成本/营业总收入(整体法)板块序列
    return w.wses(security,"sec_gctogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGcToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取营业总成本/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_gctogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOpToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取营业利润/营业总收入(整体法)板块序列
    return w.wses(security,"sec_optogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOpToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取营业利润/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_optogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDupontNpToSalesOverallChNWses(security:list,*args,**kwargs):
    # 获取净利润/营业总收入(整体法)板块序列
    return w.wses(security,"sec_dupont_nptosales_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDupontNpToSalesAvgChNWses(security:list,*args,**kwargs):
    # 获取净利润/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_dupont_nptosales_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOperateExpenseToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取销售费用/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_operateexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSEcfAAdminExpenseToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取管理费用/营业总收入(算术平均)板块序列
    return w.wses(security,"secfa_adminexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFinaExpenseToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取财务费用/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_finaexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDupontEbItToSalesAvgGLbWses(security:list,*args,**kwargs):
    # 获取息税前利润/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_dupont_ebittosales_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEbItDatoSalesOverallGLbWses(security:list,*args,**kwargs):
    # 获取EBITDA/营业总收入(整体法)板块序列
    return w.wses(security,"sec_ebitdatosales_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEbItDatoSalesAvgGLbWses(security:list,*args,**kwargs):
    # 获取EBITDA/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_ebitdatosales_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRoiCAvgGLbWses(security:list,*args,**kwargs):
    # 获取投入资本回报率(算术平均)板块序列
    return w.wses(security,"sec_roic_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOpToEBTAvgGLbWses(security:list,*args,**kwargs):
    # 获取营业利润/利润总额(算术平均)板块序列
    return w.wses(security,"sec_optoebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvestIncomeToEBTAvgChNWses(security:list,*args,**kwargs):
    # 获取价值变动净收益/利润总额(算术平均)板块序列
    return w.wses(security,"sec_investincometoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTaxToEBTAvgChNWses(security:list,*args,**kwargs):
    # 获取所得税/利润总额(算术平均)板块序列
    return w.wses(security,"sec_taxtoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDeductedProfitToProfitAvgChNWses(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净利润/净利润(算术平均)板块序列
    return w.wses(security,"sec_deductedprofittoprofit_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOperateIncomeToEBTAvgChNWses(security:list,*args,**kwargs):
    # 获取经营活动净收益/利润总额(算术平均)板块序列
    return w.wses(security,"sec_operateincometoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOCFToOrOverallChNWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/营业收入(整体法)板块序列
    return w.wses(security,"sec_ocftoor_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOCFToOrAvgChNWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/营业收入(算术平均)板块序列
    return w.wses(security,"sec_ocftoor_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOCFToOperateIncomeOverallChNWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/经营活动净收益(整体法)板块序列
    return w.wses(security,"sec_ocftooperateincome_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOCFToOperateIncomeAvgChNWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/经营活动净收益(算术平均)板块序列
    return w.wses(security,"sec_ocftooperateincome_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCapeXTodaOverallChNWses(security:list,*args,**kwargs):
    # 获取资本支出/折旧和摊销(整体法)板块序列
    return w.wses(security,"sec_capextoda_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCapitalizedTodaAvgChNWses(security:list,*args,**kwargs):
    # 获取资本支出/折旧和摊销(算术平均)板块序列
    return w.wses(security,"sec_capitalizedtoda_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDebtToAssetsOverallChNWses(security:list,*args,**kwargs):
    # 获取资产负债率(整体法)板块序列
    return w.wses(security,"sec_debttoassets_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDebtToAssetsAvgChNWses(security:list,*args,**kwargs):
    # 获取资产负债率(算术平均)板块序列
    return w.wses(security,"sec_debttoassets_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCatoAssetsOverallChNWses(security:list,*args,**kwargs):
    # 获取流动资产/总资产(整体法)板块序列
    return w.wses(security,"sec_catoassets_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCatoAssetsAvgChNWses(security:list,*args,**kwargs):
    # 获取流动资产/总资产(算术平均)板块序列
    return w.wses(security,"sec_catoassets_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNcaToAssetsOverallChNWses(security:list,*args,**kwargs):
    # 获取非流动资产/总资产(整体法)板块序列
    return w.wses(security,"sec_ncatoassets_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNcaToAssetsAvgChNWses(security:list,*args,**kwargs):
    # 获取非流动资产/总资产(算术平均)板块序列
    return w.wses(security,"sec_ncatoassets_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTangibleAssetsToAssetsOverallChNWses(security:list,*args,**kwargs):
    # 获取有形资产/总资产(整体法)板块序列
    return w.wses(security,"sec_tangibleassetstoassets_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTangibleAssetsToAssetsAvgChNWses(security:list,*args,**kwargs):
    # 获取有形资产/总资产(算术平均)板块序列
    return w.wses(security,"sec_tangibleassetstoassets_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentDebtToDebtOverallChNWses(security:list,*args,**kwargs):
    # 获取流动负债/负债合计(整体法)板块序列
    return w.wses(security,"sec_currentdebttodebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentDebtToDebtAvgChNWses(security:list,*args,**kwargs):
    # 获取流动负债/负债合计(算术平均)板块序列
    return w.wses(security,"sec_currentdebttodebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecLongDebToDebtOverallChNWses(security:list,*args,**kwargs):
    # 获取非流动负债/负债合计(整体法)板块序列
    return w.wses(security,"sec_longdebtodebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecLongDebToDebtAvgChNWses(security:list,*args,**kwargs):
    # 获取非流动负债/负债合计(算术平均)板块序列
    return w.wses(security,"sec_longdebtodebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentOverallChNWses(security:list,*args,**kwargs):
    # 获取流动比率(整体法)板块序列
    return w.wses(security,"sec_current_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentAvgChNWses(security:list,*args,**kwargs):
    # 获取流动比率(算术平均)板块序列
    return w.wses(security,"sec_current_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQuickOverallChNWses(security:list,*args,**kwargs):
    # 获取速动比率(整体法)板块序列
    return w.wses(security,"sec_quick_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQuickAvgChNWses(security:list,*args,**kwargs):
    # 获取速动比率(算术平均)板块序列
    return w.wses(security,"sec_quick_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityToDebtOverallGLbWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益/负债合计(整体法)板块序列
    return w.wses(security,"sec_equitytodebt_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityToDebtAvgGLbWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益/负债合计(算术平均)板块序列
    return w.wses(security,"sec_equitytodebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityToInterestDebtOverallGLbWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益/带息债务(整体法)板块序列
    return w.wses(security,"sec_equitytointerestdebt_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityToInterestDebtAvgGLbWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益/带息债务(算术平均)板块序列
    return w.wses(security,"sec_equitytointerestdebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEbItDatoDebtOverallGLbWses(security:list,*args,**kwargs):
    # 获取息税折旧摊销前利润/负债合计(整体法)板块序列
    return w.wses(security,"sec_ebitdatodebt_overall_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEbItDatoDebtAvgGLbWses(security:list,*args,**kwargs):
    # 获取息税折旧摊销前利润/负债合计(算术平均)板块序列
    return w.wses(security,"sec_ebitdatodebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOCFToDebtOverallChNWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/负债合计(整体法)板块序列
    return w.wses(security,"sec_ocftodebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOCFToDebtAvgChNWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额/负债合计(算术平均)板块序列
    return w.wses(security,"sec_ocftodebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInterestCoverageAvgChNWses(security:list,*args,**kwargs):
    # 获取已获利息倍数(算术平均)板块序列
    return w.wses(security,"sec_interestcoverage_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvTurnOverallChNWses(security:list,*args,**kwargs):
    # 获取存货周转率(整体法)板块序列
    return w.wses(security,"sec_invturn_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvTurnAvgChNWses(security:list,*args,**kwargs):
    # 获取存货周转率(算术平均)板块序列
    return w.wses(security,"sec_invturn_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecArturNOverallChNWses(security:list,*args,**kwargs):
    # 获取应收账款周转率(整体法)板块序列
    return w.wses(security,"sec_arturn_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecArturNAvgChNWses(security:list,*args,**kwargs):
    # 获取应收账款周转率(算术平均)板块序列
    return w.wses(security,"sec_arturn_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFaTurnOverallChNWses(security:list,*args,**kwargs):
    # 获取固定资产周转率(整体法)板块序列
    return w.wses(security,"sec_faturn_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFaTurnAvgChNWses(security:list,*args,**kwargs):
    # 获取固定资产周转率(算术平均)板块序列
    return w.wses(security,"sec_faturn_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecAssetsTurnOverallChNWses(security:list,*args,**kwargs):
    # 获取总资产周转率(整体法)板块序列
    return w.wses(security,"sec_assetsturn_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecAssetsTurnAvgChNWses(security:list,*args,**kwargs):
    # 获取总资产周转率(算术平均)板块序列
    return w.wses(security,"sec_assetsturn_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTurnDaysOverallChNWses(security:list,*args,**kwargs):
    # 获取营业周期(整体法)板块序列
    return w.wses(security,"sec_turndays_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTurnDaysAvgChNWses(security:list,*args,**kwargs):
    # 获取营业周期(算术平均)板块序列
    return w.wses(security,"sec_turndays_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvTurnDaysOverallChNWses(security:list,*args,**kwargs):
    # 获取存货周转天数(整体法)板块序列
    return w.wses(security,"sec_invturndays_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvTurnDaysAvgChNWses(security:list,*args,**kwargs):
    # 获取存货周转天数(算术平均)板块序列
    return w.wses(security,"sec_invturndays_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecArturNDaysOverallChNWses(security:list,*args,**kwargs):
    # 获取应收账款周转天数(整体法)板块序列
    return w.wses(security,"sec_arturndays_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecArturNDaysAvgChNWses(security:list,*args,**kwargs):
    # 获取应收账款周转天数(算术平均)板块序列
    return w.wses(security,"sec_arturndays_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrYoYTotalChNWses(security:list,*args,**kwargs):
    # 获取营业总收入合计(同比增长率)板块序列
    return w.wses(security,"sec_gr_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRevenueYoYTotalChNWses(security:list,*args,**kwargs):
    # 获取营业收入合计(同比增长率)板块序列
    return w.wses(security,"sec_revenue_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOpYoYTotalChNWses(security:list,*args,**kwargs):
    # 获取营业利润合计(同比增长率)板块序列
    return w.wses(security,"sec_op_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNpSumYoYGLbWses(security:list,*args,**kwargs):
    # 获取净利润合计(同比增长率)板块序列
    return w.wses(security,"sec_np_sum_yoy_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNpaSpcYoYTotalChNWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润合计(同比增长率)板块序列
    return w.wses(security,"sec_npaspc_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCfOAYoYTotalChNWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额合计(同比增长率)板块序列
    return w.wses(security,"sec_cfoa_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCFiaSumYoYGLbWses(security:list,*args,**kwargs):
    # 获取投资活动产生的现金流量净额合计(同比增长率)板块序列
    return w.wses(security,"sec_cfia_sum_yoy_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCffASumYoYGLbWses(security:list,*args,**kwargs):
    # 获取筹资活动产生的现金流量净额合计(同比增长率)板块序列
    return w.wses(security,"sec_cffa_sum_yoy_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCCeNetIncreaseSumYoYGLbWses(security:list,*args,**kwargs):
    # 获取现金及现金等价物净增加额合计(同比增长率)板块序列
    return w.wses(security,"sec_cce_netincrease_sum_yoy_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDupontRoeOverallYoYChNWses(security:list,*args,**kwargs):
    # 获取净资产收益率(整体法)(同比增长率)板块序列
    return w.wses(security,"sec_dupont_roe_overall_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDupontRoeAvgYoYChNWses(security:list,*args,**kwargs):
    # 获取净资产收益率(算术平均)(同比增长率)板块序列
    return w.wses(security,"sec_dupont_roe_avg_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecBpSOverallGtBYearChNWses(security:list,*args,**kwargs):
    # 获取每股净资产(整体法)(相对年初增长率)板块序列
    return w.wses(security,"sec_bps_overall_gtbyear_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecBpSAvgGtBgYearChNWses(security:list,*args,**kwargs):
    # 获取每股净资产(算术平均)(相对年初增长率)板块序列
    return w.wses(security,"sec_bps_avg_gtbgyear_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTotalAssetTotalGtBYearChNWses(security:list,*args,**kwargs):
    # 获取资产总计合计(相对年初增长率)板块序列
    return w.wses(security,"sec_totalasset_total_gtbyear_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTotalEquityAsPcTotalGtBYearChNWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益合计(相对年初增长率)板块序列
    return w.wses(security,"sec_totalequityaspc_total_gtbyear_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrSumChNWses(security:list,*args,**kwargs):
    # 获取营业总收入(合计)板块序列
    return w.wses(security,"sec_gr_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrAvgChNWses(security:list,*args,**kwargs):
    # 获取营业总收入(算术平均)板块序列
    return w.wses(security,"sec_gr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRevenueSumGLbWses(security:list,*args,**kwargs):
    # 获取主营收入(合计)板块序列
    return w.wses(security,"sec_revenue_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecRevenueAvgGLbWses(security:list,*args,**kwargs):
    # 获取主营收入(算术平均)板块序列
    return w.wses(security,"sec_revenue_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOtherRevenueSumGLbWses(security:list,*args,**kwargs):
    # 获取其他营业收入(合计)板块序列
    return w.wses(security,"sec_otherrevenue_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOtherRevenueAvgGLbWses(security:list,*args,**kwargs):
    # 获取其他营业收入(算术平均)板块序列
    return w.wses(security,"sec_otherrevenue_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGcSumGLbWses(security:list,*args,**kwargs):
    # 获取总营业支出(合计)板块序列
    return w.wses(security,"sec_gc_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGcAvgGLbWses(security:list,*args,**kwargs):
    # 获取总营业支出(算术平均)板块序列
    return w.wses(security,"sec_gc_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOcSumChNWses(security:list,*args,**kwargs):
    # 获取营业成本(合计)板块序列
    return w.wses(security,"sec_oc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOcAvgChNWses(security:list,*args,**kwargs):
    # 获取营业成本(算术平均)板块序列
    return w.wses(security,"sec_oc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecExpenseSumGLbWses(security:list,*args,**kwargs):
    # 获取营业开支(合计)板块序列
    return w.wses(security,"sec_expense_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecExpenseAvgGLbWses(security:list,*args,**kwargs):
    # 获取营业开支(算术平均)板块序列
    return w.wses(security,"sec_expense_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityInvpnLSumGLbWses(security:list,*args,**kwargs):
    # 获取权益性投资损益(合计)板块序列
    return w.wses(security,"sec_equityinvpnl_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityInvpnLAvgGLbWses(security:list,*args,**kwargs):
    # 获取权益性投资损益(算术平均)板块序列
    return w.wses(security,"sec_equityinvpnl_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOpSumChNWses(security:list,*args,**kwargs):
    # 获取营业利润(合计)板块序列
    return w.wses(security,"sec_op_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOpAvgChNWses(security:list,*args,**kwargs):
    # 获取营业利润(算术平均)板块序列
    return w.wses(security,"sec_op_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEBtSumGLbWses(security:list,*args,**kwargs):
    # 获取除税前利润(合计)板块序列
    return w.wses(security,"sec_ebt_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEBtAvgGLbWses(security:list,*args,**kwargs):
    # 获取除税前利润(算术平均)板块序列
    return w.wses(security,"sec_ebt_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTaxSumChNWses(security:list,*args,**kwargs):
    # 获取所得税(合计)板块序列
    return w.wses(security,"sec_tax_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTaxAvgChNWses(security:list,*args,**kwargs):
    # 获取所得税(算术平均)板块序列
    return w.wses(security,"sec_tax_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNpSumChNWses(security:list,*args,**kwargs):
    # 获取净利润(合计)板块序列
    return w.wses(security,"sec_np_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNpAvgChNWses(security:list,*args,**kwargs):
    # 获取净利润(算术平均)板块序列
    return w.wses(security,"sec_np_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNpaSpcSumGLbWses(security:list,*args,**kwargs):
    # 获取归属普通股东净利润(合计)板块序列
    return w.wses(security,"sec_npaspc_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNpaSpcAvgGLbWses(security:list,*args,**kwargs):
    # 获取归属普通股东净利润(算术平均)板块序列
    return w.wses(security,"sec_npaspc_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrossMargin2SumChNWses(security:list,*args,**kwargs):
    # 获取毛利(合计)板块序列
    return w.wses(security,"sec_grossmargin2_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGrossMargin2AvgChNWses(security:list,*args,**kwargs):
    # 获取毛利(算术平均)板块序列
    return w.wses(security,"sec_grossmargin2_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEbItSumGLbWses(security:list,*args,**kwargs):
    # 获取EBIT(合计)板块序列
    return w.wses(security,"sec_ebit_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEbItAvgGLbWses(security:list,*args,**kwargs):
    # 获取EBIT(算术平均)板块序列
    return w.wses(security,"sec_ebit_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecAssetTotalSumChNWses(security:list,*args,**kwargs):
    # 获取资产总计(合计)板块序列
    return w.wses(security,"sec_asset_total_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecAssetTotalAvgChNWses(security:list,*args,**kwargs):
    # 获取资产总计(算术平均)板块序列
    return w.wses(security,"sec_asset_total_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCCeSumGLbWses(security:list,*args,**kwargs):
    # 获取现金及现金等价物(合计)板块序列
    return w.wses(security,"sec_cce_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCCeAvgGLbWses(security:list,*args,**kwargs):
    # 获取现金及现金等价物(算术平均)板块序列
    return w.wses(security,"sec_cce_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTradingFinancialAssetSumChNWses(security:list,*args,**kwargs):
    # 获取交易性金融资产(合计)板块序列
    return w.wses(security,"sec_tradingfinancialasset_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTradingFinancialAssetAvgChNWses(security:list,*args,**kwargs):
    # 获取交易性金融资产(算术平均)板块序列
    return w.wses(security,"sec_tradingfinancialasset_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecArSumGLbWses(security:list,*args,**kwargs):
    # 获取应收账款及票据(合计)板块序列
    return w.wses(security,"sec_ar_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecArAvgGLbWses(security:list,*args,**kwargs):
    # 获取应收账款及票据(算术平均)板块序列
    return w.wses(security,"sec_ar_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecIvNenTorySumChNWses(security:list,*args,**kwargs):
    # 获取存货(合计)板块序列
    return w.wses(security,"sec_ivnentory_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecIvNenToryAvgChNWses(security:list,*args,**kwargs):
    # 获取存货(算术平均)板块序列
    return w.wses(security,"sec_ivnentory_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentAssetSumChNWses(security:list,*args,**kwargs):
    # 获取流动资产(合计)板块序列
    return w.wses(security,"sec_currentasset_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentAssetAvgChNWses(security:list,*args,**kwargs):
    # 获取流动资产(算术平均)板块序列
    return w.wses(security,"sec_currentasset_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityInvSumGLbWses(security:list,*args,**kwargs):
    # 获取权益性投资(合计)板块序列
    return w.wses(security,"sec_equityinv_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityInvAvgGLbWses(security:list,*args,**kwargs):
    # 获取权益性投资(算术平均)板块序列
    return w.wses(security,"sec_equityinv_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFixAssetNetValueSumChNWses(security:list,*args,**kwargs):
    # 获取固定资产净值(合计)板块序列
    return w.wses(security,"sec_fixassetnetvalue_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFixAssetNetValueAvgChNWses(security:list,*args,**kwargs):
    # 获取固定资产净值(算术平均)板块序列
    return w.wses(security,"sec_fixassetnetvalue_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCIpNetValueSumChNWses(security:list,*args,**kwargs):
    # 获取在建工程(合计)板块序列
    return w.wses(security,"sec_cipnetvalue_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCIpNetValueAvgChNWses(security:list,*args,**kwargs):
    # 获取在建工程(算术平均)板块序列
    return w.wses(security,"sec_cipnetvalue_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNonCurrentAssetSumChNWses(security:list,*args,**kwargs):
    # 获取非流动资产(合计)板块序列
    return w.wses(security,"sec_noncurrentasset_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNonCurrentAssetAvgChNWses(security:list,*args,**kwargs):
    # 获取非流动资产(算术平均)板块序列
    return w.wses(security,"sec_noncurrentasset_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecApSumGLbWses(security:list,*args,**kwargs):
    # 获取应付账款及票据(合计)板块序列
    return w.wses(security,"sec_ap_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecApAvgGLbWses(security:list,*args,**kwargs):
    # 获取应付账款及票据(算术平均)板块序列
    return w.wses(security,"sec_ap_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentMaturityOfBorrowingSSumGLbWses(security:list,*args,**kwargs):
    # 获取短期借贷及长期借贷当期到期部分(合计)板块序列
    return w.wses(security,"sec_currentmaturityofborrowings_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentMaturityOfBorrowingSAvgGLbWses(security:list,*args,**kwargs):
    # 获取短期借贷及长期借贷当期到期部分(算术平均)板块序列
    return w.wses(security,"sec_currentmaturityofborrowings_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentLiabilitySumChNWses(security:list,*args,**kwargs):
    # 获取流动负债(合计)板块序列
    return w.wses(security,"sec_currentliability_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCurrentLiabilityAvgChNWses(security:list,*args,**kwargs):
    # 获取流动负债(算术平均)板块序列
    return w.wses(security,"sec_currentliability_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecLtDebtSumChNWses(security:list,*args,**kwargs):
    # 获取长期借款(合计)板块序列
    return w.wses(security,"sec_ltdebt_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecLtDebtAvgChNWses(security:list,*args,**kwargs):
    # 获取长期借款(算术平均)板块序列
    return w.wses(security,"sec_ltdebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNonCurrentLiabilitySumChNWses(security:list,*args,**kwargs):
    # 获取非流动负债(合计)板块序列
    return w.wses(security,"sec_noncurrentliability_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNonCurrentLiabilityAvgChNWses(security:list,*args,**kwargs):
    # 获取非流动负债(算术平均)板块序列
    return w.wses(security,"sec_noncurrentliability_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquitySumChNWses(security:list,*args,**kwargs):
    # 获取股东权益(合计)板块序列
    return w.wses(security,"sec_equity_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEquityAvgChNWses(security:list,*args,**kwargs):
    # 获取股东权益(算术平均)板块序列
    return w.wses(security,"sec_equity_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMinorityQuitYSumChNWses(security:list,*args,**kwargs):
    # 获取少数股东权益(合计)板块序列
    return w.wses(security,"sec_minorityquity_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMinorityQuitYAvgChNWses(security:list,*args,**kwargs):
    # 获取少数股东权益(算术平均)板块序列
    return w.wses(security,"sec_minorityquity_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecReAtAInEarningSumGLbWses(security:list,*args,**kwargs):
    # 获取留存收益(合计)板块序列
    return w.wses(security,"sec_reatainearning_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecReAtAInEarningAvgGLbWses(security:list,*args,**kwargs):
    # 获取留存收益(算术平均)板块序列
    return w.wses(security,"sec_reatainearning_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecWCapSumGLbWses(security:list,*args,**kwargs):
    # 获取营运资本(合计)板块序列
    return w.wses(security,"sec_wcap_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecWCapAvgGLbWses(security:list,*args,**kwargs):
    # 获取营运资本(算术平均)板块序列
    return w.wses(security,"sec_wcap_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEAsPcSumChNWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益(合计)板块序列
    return w.wses(security,"sec_easpc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEAsPcAvgChNWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的权益(算术平均)板块序列
    return w.wses(security,"sec_easpc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNcFoASumGLbWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额(合计)板块序列
    return w.wses(security,"sec_ncfoa_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNcFoAAvgGLbWses(security:list,*args,**kwargs):
    # 获取经营活动产生的现金流量净额(算术平均)板块序列
    return w.wses(security,"sec_ncfoa_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNcFiaSumGLbWses(security:list,*args,**kwargs):
    # 获取投资活动产生的现金流量净额(合计)板块序列
    return w.wses(security,"sec_ncfia_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNcFiaAvgGLbWses(security:list,*args,**kwargs):
    # 获取投资活动产生的现金流量净额(算术平均)板块序列
    return w.wses(security,"sec_ncfia_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNcFfaSumGLbWses(security:list,*args,**kwargs):
    # 获取筹资活动产生的现金流量净额(合计)板块序列
    return w.wses(security,"sec_ncffa_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNcFfaAvgGLbWses(security:list,*args,**kwargs):
    # 获取筹资活动产生的现金流量净额(算术平均)板块序列
    return w.wses(security,"sec_ncffa_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEffectOfForExonCashSumGLbWses(security:list,*args,**kwargs):
    # 获取汇率变动对现金的影响(合计)板块序列
    return w.wses(security,"sec_effectofforexoncash_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEffectOfForExonCashAvgGLbWses(security:list,*args,**kwargs):
    # 获取汇率变动对现金的影响(算术平均)板块序列
    return w.wses(security,"sec_effectofforexoncash_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNetIncreaseIncCeSumGLbWses(security:list,*args,**kwargs):
    # 获取现金及现金等价物净增加额(合计)板块序列
    return w.wses(security,"sec_netincreaseincce_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNetIncreaseIncCeAvgGLbWses(security:list,*args,**kwargs):
    # 获取现金及现金等价物净增加额(算术平均)板块序列
    return w.wses(security,"sec_netincreaseincce_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFcFe2SumGLbWses(security:list,*args,**kwargs):
    # 获取股权自由现金流量FCFE(合计)板块序列
    return w.wses(security,"sec_fcfe2_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFcFe2AvgGLbWses(security:list,*args,**kwargs):
    # 获取股权自由现金流量FCFE(算术平均)板块序列
    return w.wses(security,"sec_fcfe2_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFcFfSumGLbWses(security:list,*args,**kwargs):
    # 获取企业自由现金流量(合计)板块序列
    return w.wses(security,"sec_fcff_sum_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFcFfAvgGLbWses(security:list,*args,**kwargs):
    # 获取企业自由现金流量(算术平均)板块序列
    return w.wses(security,"sec_fcff_avg_glb",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNetProfitMarginTtMOverallChNWses(security:list,*args,**kwargs):
    # 获取销售净利率(TTM)(整体法)板块序列
    return w.wses(security,"sec_netprofitmargin_ttm_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNetProfitMarginTtMAvgChNWses(security:list,*args,**kwargs):
    # 获取销售净利率(TTM)(算术平均)板块序列
    return w.wses(security,"sec_netprofitmargin_ttm_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOperateExpenseToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取销售费用/营业总收入(整体法)板块序列
    return w.wses(security,"sec_operateexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFaAdminExpenseToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取管理费用/营业总收入(整体法)板块序列
    return w.wses(security,"sec_fa_adminexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFinaExpenseToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取财务费用/营业总收入(整体法)板块序列
    return w.wses(security,"sec_finaexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOperateIncomeToEBTOverallChNWses(security:list,*args,**kwargs):
    # 获取经营活动净收益/利润总额(整体法)板块序列
    return w.wses(security,"sec_operateincometoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvestIncomeToEBTOverallChNWses(security:list,*args,**kwargs):
    # 获取价值变动净收益/利润总额(整体法)板块序列
    return w.wses(security,"sec_investincometoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTaxToEBTOverallChNWses(security:list,*args,**kwargs):
    # 获取所得税/利润总额(整体法)板块序列
    return w.wses(security,"sec_taxtoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecDeductedProfitToProfitOverallChNWses(security:list,*args,**kwargs):
    # 获取扣除非经常损益后的净利润/净利润(整体法)板块序列
    return w.wses(security,"sec_deductedprofittoprofit_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecSalesCashIntoOrOverallChNWses(security:list,*args,**kwargs):
    # 获取销售商品提供劳务收到的现金/营业收入(整体法)板块序列
    return w.wses(security,"sec_salescashintoor_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecSalesCashIntoOrAvgChNWses(security:list,*args,**kwargs):
    # 获取销售商品提供劳务收到的现金/营业收入(算术平均)板块序列
    return w.wses(security,"sec_salescashintoor_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTotalLiabilityToeAsPcOverallChNWses(security:list,*args,**kwargs):
    # 获取负债合计/归属母公司股东的权益(整体法)板块序列
    return w.wses(security,"sec_totalliabilitytoeaspc_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecTotalLiabilityToeAsPcAvgChNWses(security:list,*args,**kwargs):
    # 获取负债合计/归属母公司股东的权益(算术平均)板块序列
    return w.wses(security,"sec_totalliabilitytoeaspc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInterestBearingDebtToeAsPcOverallChNWses(security:list,*args,**kwargs):
    # 获取带息债务/归属母公司股东的权益(整体法)板块序列
    return w.wses(security,"sec_interestbearingdebttoeaspc_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNetLiabilityToeAsPcOverallChNWses(security:list,*args,**kwargs):
    # 获取净债务/归属母公司股东的权益(整体法)板块序列
    return w.wses(security,"sec_netliabilitytoeaspc_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecAssetsTurnTtMOverallChNWses(security:list,*args,**kwargs):
    # 获取资产周转率(TTM)(整体法)板块序列
    return w.wses(security,"sec_assetsturn_ttm_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecAssetsTurnTtMAvgChNWses(security:list,*args,**kwargs):
    # 获取资产周转率(TTM)(算术平均)板块序列
    return w.wses(security,"sec_assetsturn_ttm_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEBtYoYTotalChNWses(security:list,*args,**kwargs):
    # 获取利润总额合计(同比增长率)板块序列
    return w.wses(security,"sec_ebt_yoy_total_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaEpsOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.每股收益EPS(整体法)板块序列
    return w.wses(security,"sec_qfa_eps_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaEpsAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.每股收益EPS(算术平均)板块序列
    return w.wses(security,"sec_qfa_eps_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaRoeDilutedOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.净资产收益率ROE-摊薄(整体法)板块序列
    return w.wses(security,"sec_qfa_roe_diluted_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaRoeDilutedAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.净资产收益率ROE-摊薄(算术平均)板块序列
    return w.wses(security,"sec_qfa_roe_diluted_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaDeductedRoeDilutedOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.扣除非经常损益后的净资产收益率-摊薄(整体法)板块序列
    return w.wses(security,"sec_qfa_deductedroe_diluted_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaDeductedRoeDilutedAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.扣除非经常损益后的净资产收益率-摊薄(算术平均)板块序列
    return w.wses(security,"sec_qfa_deductedroe_diluted_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaRoaOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.总资产净利率(整体法)板块序列
    return w.wses(security,"sec_qfa_roa_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaRoaAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.总资产净利率(算术平均)板块序列
    return w.wses(security,"sec_qfa_roa_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaNetProfitMarginOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.销售净利率(整体法)板块序列
    return w.wses(security,"sec_qfa_netprofitmargin_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaNetProfitMarginAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.销售净利率(算术平均)板块序列
    return w.wses(security,"sec_qfa_netprofitmargin_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaGrossProfitMarginOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.销售毛利率(整体法)板块序列
    return w.wses(security,"sec_qfa_grossprofitmargin_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaGrossProfitMarginAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.销售毛利率(算术平均)板块序列
    return w.wses(security,"sec_qfa_grossprofitmargin_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaGcToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业总成本/营业总收入(整体法)板块序列
    return w.wses(security,"sec_qfa_gctogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaGcToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业总成本/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_qfa_gctogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOpToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业利润/营业总收入(整体法)板块序列
    return w.wses(security,"sec_qfa_optogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOpToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业利润/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_qfa_optogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaProfitToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.净利润/营业总收入(整体法)板块序列
    return w.wses(security,"sec_qfa_profittogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaProfitToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.净利润/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_qfa_profittogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOperateExpenseToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.销售费用/营业总收入(整体法)板块序列
    return w.wses(security,"sec_qfa_operateexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOperateExpenseToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.销售费用/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_qfa_operateexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaAdminExpenseToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.管理费用/营业总收入(整体法)板块序列
    return w.wses(security,"sec_qfa_adminexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaAdminExpenseToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.管理费用/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_qfa_adminexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaFinaExpenseToGrOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.财务费用/营业总收入(整体法)板块序列
    return w.wses(security,"sec_qfa_finaexpensetogr_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaFinaExpenseToGrAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.财务费用/营业总收入(算术平均)板块序列
    return w.wses(security,"sec_qfa_finaexpensetogr_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOperateIncomeToEBTOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.经营活动净收益/利润总额(整体法)板块序列
    return w.wses(security,"sec_qfa_operateincometoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOperateIncomeToEBTAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.经营活动净收益/利润总额(算术平均)板块序列
    return w.wses(security,"sec_qfa_operateincometoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaInvestIncomeToEBTOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.价值变动净收益/利润总额(整体法)板块序列
    return w.wses(security,"sec_qfa_investincometoebt_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaInvestIncomeToEBTAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.价值变动净收益/利润总额(算术平均)板块序列
    return w.wses(security,"sec_qfa_investincometoebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaDeductedProfitToProfitOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.扣除非经常损益后的净利润/净利润(整体法)板块序列
    return w.wses(security,"sec_qfa_deductedprofittoprofit_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaDeductedProfitToProfitAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.扣除非经常损益后的净利润/净利润(算术平均)板块序列
    return w.wses(security,"sec_qfa_deductedprofittoprofit_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaSalesCashIntoOrOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.销售商品提供劳务收到的现金/营业收入(整体法)板块序列
    return w.wses(security,"sec_qfa_salescashintoor_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaSalesCashIntoOrAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.销售商品提供劳务收到的现金/营业收入(算术平均)板块序列
    return w.wses(security,"sec_qfa_salescashintoor_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOCFToOrOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.经营活动产生的现金流量净额/营业收入(整体法)板块序列
    return w.wses(security,"sec_qfa_ocftoor_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOCFToOrAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.经营活动产生的现金流量净额/营业收入(算术平均)板块序列
    return w.wses(security,"sec_qfa_ocftoor_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOCFToOperateIncomeOverallChNWses(security:list,*args,**kwargs):
    # 获取单季度.经营活动产生的现金流量净额/经营活动净收益(整体法)板块序列
    return w.wses(security,"sec_qfa_ocftooperateincome_overall_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOCFToOperateIncomeAvgChNWses(security:list,*args,**kwargs):
    # 获取单季度.经营活动产生的现金流量净额/经营活动净收益(算术平均)板块序列
    return w.wses(security,"sec_qfa_ocftooperateincome_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaGrTotalYoYChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业总收入合计(同比增长率)板块序列
    return w.wses(security,"sec_qfa_gr_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaGrTotalMomChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业总收入合计(环比增长率)板块序列
    return w.wses(security,"sec_qfa_gr_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaRevenueTotalYoYChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业收入合计(同比增长率)板块序列
    return w.wses(security,"sec_qfa_revenue_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaRevenueTotalMomChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业收入合计(环比增长率)板块序列
    return w.wses(security,"sec_qfa_revenue_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOpTotalYoYChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业利润合计(同比增长率)板块序列
    return w.wses(security,"sec_qfa_op_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaOpTotalMomChNWses(security:list,*args,**kwargs):
    # 获取单季度.营业利润合计(环比增长率)板块序列
    return w.wses(security,"sec_qfa_op_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaNpTotalYoYChNWses(security:list,*args,**kwargs):
    # 获取单季度.净利润合计(同比增长率)板块序列
    return w.wses(security,"sec_qfa_np_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaNpTotalMomChNWses(security:list,*args,**kwargs):
    # 获取单季度.净利润合计(环比增长率)板块序列
    return w.wses(security,"sec_qfa_np_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaNpaSpcTotalYoYChNWses(security:list,*args,**kwargs):
    # 获取单季度.归属母公司股东的净利润合计(同比增长率)板块序列
    return w.wses(security,"sec_qfa_npaspc_total_yoy_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecQfaNpaSpcTotalMomChNWses(security:list,*args,**kwargs):
    # 获取单季度.归属母公司股东的净利润合计(环比增长率)板块序列
    return w.wses(security,"sec_qfa_npaspc_total_mom_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGcSumChNWses(security:list,*args,**kwargs):
    # 获取营业总成本(合计)板块序列
    return w.wses(security,"sec_gc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecGcAvgChNWses(security:list,*args,**kwargs):
    # 获取营业总成本(算术平均)板块序列
    return w.wses(security,"sec_gc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOrSumChNWses(security:list,*args,**kwargs):
    # 获取营业收入(合计)板块序列
    return w.wses(security,"sec_or_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOrAvgChNWses(security:list,*args,**kwargs):
    # 获取营业收入(算术平均)板块序列
    return w.wses(security,"sec_or_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecSellingExpSumChNWses(security:list,*args,**kwargs):
    # 获取销售费用(合计)板块序列
    return w.wses(security,"sec_sellingexp_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecSellingExpAvgChNWses(security:list,*args,**kwargs):
    # 获取销售费用(算术平均)板块序列
    return w.wses(security,"sec_sellingexp_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMNgtExpSumChNWses(security:list,*args,**kwargs):
    # 获取管理费用(合计)板块序列
    return w.wses(security,"sec_mngtexp_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecMNgtExpAvgChNWses(security:list,*args,**kwargs):
    # 获取管理费用(算术平均)板块序列
    return w.wses(security,"sec_mngtexp_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFineXpSumChNWses(security:list,*args,**kwargs):
    # 获取财务费用(合计)板块序列
    return w.wses(security,"sec_finexp_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecFineXpAvgChNWses(security:list,*args,**kwargs):
    # 获取财务费用(算术平均)板块序列
    return w.wses(security,"sec_finexp_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNiOnInvestmentSumChNWses(security:list,*args,**kwargs):
    # 获取投资净收益(合计)板块序列
    return w.wses(security,"sec_nioninvestment_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNiOnInvestmentAvgChNWses(security:list,*args,**kwargs):
    # 获取投资净收益(算术平均)板块序列
    return w.wses(security,"sec_nioninvestment_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNiOnForExSumChNWses(security:list,*args,**kwargs):
    # 获取汇兑净收益(合计)板块序列
    return w.wses(security,"sec_nionforex_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNiOnForExAvgChNWses(security:list,*args,**kwargs):
    # 获取汇兑净收益(算术平均)板块序列
    return w.wses(security,"sec_nionforex_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNiFromChangesInFvSumChNWses(security:list,*args,**kwargs):
    # 获取公允价值变动净收益(合计)板块序列
    return w.wses(security,"sec_nifromchangesinfv_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNiFromChangesInFvAvgChNWses(security:list,*args,**kwargs):
    # 获取公允价值变动净收益(算术平均)板块序列
    return w.wses(security,"sec_nifromchangesinfv_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEBtSumChNWses(security:list,*args,**kwargs):
    # 获取利润总额(合计)板块序列
    return w.wses(security,"sec_ebt_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecEBtAvgChNWses(security:list,*args,**kwargs):
    # 获取利润总额(算术平均)板块序列
    return w.wses(security,"sec_ebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNpaSpcSumChNWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润(合计)板块序列
    return w.wses(security,"sec_npaspc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNpaSpcAvgChNWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润(算术平均)板块序列
    return w.wses(security,"sec_npaspc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecExNonRecurringPnLnPasPcSumChNWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润-扣除非经常损益(合计)板块序列
    return w.wses(security,"sec_exnonrecurringpnlnpaspc_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecExNonRecurringPnLnPasPcAvgChNWses(security:list,*args,**kwargs):
    # 获取归属母公司股东的净利润-扣除非经常损益(算术平均)板块序列
    return w.wses(security,"sec_exnonrecurringpnlnpaspc_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOperateIncomeSumChNWses(security:list,*args,**kwargs):
    # 获取经营活动净收益(合计)板块序列
    return w.wses(security,"sec_operateincome_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecOperateIncomeAvgChNWses(security:list,*args,**kwargs):
    # 获取经营活动净收益(算术平均)板块序列
    return w.wses(security,"sec_operateincome_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvestIncomeSumChNWses(security:list,*args,**kwargs):
    # 获取价值变动净收益(合计)板块序列
    return w.wses(security,"sec_investincome_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvestIncomeAvgChNWses(security:list,*args,**kwargs):
    # 获取价值变动净收益(算术平均)板块序列
    return w.wses(security,"sec_investincome_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCashSumChNWses(security:list,*args,**kwargs):
    # 获取货币资金(合计)板块序列
    return w.wses(security,"sec_cash_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecCashAvgChNWses(security:list,*args,**kwargs):
    # 获取货币资金(算术平均)板块序列
    return w.wses(security,"sec_cash_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNotErSumChNWses(security:list,*args,**kwargs):
    # 获取应收票据(合计)板块序列
    return w.wses(security,"sec_noter_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNotErAvgChNWses(security:list,*args,**kwargs):
    # 获取应收票据(算术平均)板块序列
    return w.wses(security,"sec_noter_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecArSumChNWses(security:list,*args,**kwargs):
    # 获取应收账款(合计)板块序列
    return w.wses(security,"sec_ar_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecArAvgChNWses(security:list,*args,**kwargs):
    # 获取应收账款(算术平均)板块序列
    return w.wses(security,"sec_ar_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecLteQtInvestmentSumChNWses(security:list,*args,**kwargs):
    # 获取长期股权投资(合计)板块序列
    return w.wses(security,"sec_lteqtinvestment_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecLteQtInvestmentAvgChNWses(security:list,*args,**kwargs):
    # 获取长期股权投资(算术平均)板块序列
    return w.wses(security,"sec_lteqtinvestment_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvestmentReSumChNWses(security:list,*args,**kwargs):
    # 获取投资性房地产(合计)板块序列
    return w.wses(security,"sec_investmentre_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecInvestmentReAvgChNWses(security:list,*args,**kwargs):
    # 获取投资性房地产(算术平均)板块序列
    return w.wses(security,"sec_investmentre_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecStDebtSumChNWses(security:list,*args,**kwargs):
    # 获取短期借款(合计)板块序列
    return w.wses(security,"sec_stdebt_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecStDebtAvgChNWses(security:list,*args,**kwargs):
    # 获取短期借款(算术平均)板块序列
    return w.wses(security,"sec_stdebt_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNotEpSumChNWses(security:list,*args,**kwargs):
    # 获取应付票据(合计)板块序列
    return w.wses(security,"sec_notep_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecNotEpAvgChNWses(security:list,*args,**kwargs):
    # 获取应付票据(算术平均)板块序列
    return w.wses(security,"sec_notep_avg_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecApSumChNWses(security:list,*args,**kwargs):
    # 获取应付账款(合计)板块序列
    return w.wses(security,"sec_ap_sum_chn",*args,**kwargs,usedf=True)
@convertInputSecurityTypeForWses
def getSecApAvgChNWses(security:list,*args,**kwargs):
    # 获取应付账款(算术平均)板块序列
    return w.wses(security,"sec_ap_avg_chn",*args,**kwargs,usedf=True)