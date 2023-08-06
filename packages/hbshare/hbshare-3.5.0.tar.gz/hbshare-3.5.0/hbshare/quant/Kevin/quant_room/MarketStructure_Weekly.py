"""
指增策略 - 市场结构Weekly
"""
import pandas as pd
import hbshare as hbs
import numpy as np
import os
from scipy import stats
import statsmodels.api as sm
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params, style_names
import datetime
import plotly.graph_objs as go
from plotly.offline import plot as plot_ly
from statsmodels.stats.weightstats import DescrStatsW
from hbshare.fe.common.util.data_loader import get_trading_day_list


def get_shift_date(date):
    trade_dt = datetime.datetime.strptime(date, '%Y%m%d')
    pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

    sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
        pre_date, date)
    res = hbs.db_data_query('readonly', sql_script, page_size=5000)
    df = pd.DataFrame(res['data']).rename(
        columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                 "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
    df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
    df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
    df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

    trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

    return trading_day_list[-1]


def get_benchmark_components(date):
    sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and " \
                 "SecuCode in ('000300', '000905', '000852')"
    res = hbs.db_data_query('readonly', sql_script)
    index_info = pd.DataFrame(res['data'])
    inner_code_series = index_info.set_index('SECUCODE')['INNERCODE']

    weight = []
    for benchmark_id in ['000300', '000905', '000852']:
        inner_code = inner_code_series.loc[benchmark_id]
        sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                     "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                     "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        weight_df = data.rename(
            columns={"SECUCODE": "ticker", "ENDDATE": "effDate", "WEIGHT": "weight"})
        weight_df['benchmark_id'] = benchmark_id
        weight.append(weight_df[['ticker', 'benchmark_id']])

    return pd.concat(weight)


def group_test(df, group_col, value_col):
    bins = [df[group_col].quantile(x) for x in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
    labels = ['group_' + str(x) for x in range(1, 6)]
    df['group'] = pd.cut(df[group_col], bins, right=False, labels=labels)

    return df.groupby('group')[value_col].mean()


class AlphaSeries:
    def __init__(self, start_date, end_date, fund_info, benchmark_id='000905'):
        self.start_date = start_date
        self.end_date = end_date
        self.fund_info = fund_info
        self.benchmark_id = benchmark_id

    def calculate(self):
        trading_day_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")
        fund_dict = self.fund_info.set_index('管理人')['产品ID'].to_dict()
        nav_series_list = []
        for name, fund_id in fund_dict.items():
            start_date = self.fund_info[self.fund_info['管理人'] == name]['运作起始日期'].values[0]
            start_date = pd.to_datetime(start_date).strftime('%Y%m%d')
            sql_script = "SELECT a.jjdm fund_id, b.jzrq TRADEDATE, b.fqdwjz as ADJ_NAV from " \
                         "st_hedge.t_st_jjxx a, st_hedge.t_st_rhb b where a.cpfl = '4' and a.jjdm = b.jjdm " \
                         "and a.jjzt not in ('3') " \
                         "and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                         "order by b.jzrq".format(fund_id, start_date, self.end_date)
            res = hbs.db_data_query("highuser", sql_script, page_size=5000)
            data = pd.DataFrame(res['data']).set_index('TRADEDATE')['ADJ_NAV']
            data.name = name
            nav_series_list.append(data)
        nav_df = pd.concat(nav_series_list, axis=1).sort_index().reindex(trading_day_list).dropna(how='all', axis=0)
        nav_df = nav_df.fillna(method='ffill')

        for col in nav_df.columns:
            nav_df[col] = nav_df[col] / nav_df[col].shift(1) - 1
        mean_alpha = nav_df.mean(axis=1).dropna()  # 策略周度平均收益

        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format(self.benchmark_id, self.start_date, self.end_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        index_return = data.set_index('TRADEDATE').reindex(trading_day_list)['TCLOSE'].pct_change().dropna()

        idx = mean_alpha.index.intersection(index_return.index)
        excess_return = mean_alpha.reindex(idx) - index_return.reindex(idx)

        return excess_return


class MarketLiquidity:
    def __init__(self, trade_date):
        self.trade_date = trade_date

    def run(self):
        # A股行情
        sql_script = "SELECT SYMBOL, SNAME, VOTURNOVER, PCHG FROM finchina.CHDQUOTE WHERE" \
                     " TDATE = {}".format(self.trade_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])
        data = data[data['SYMBOL'].str[0].isin(['0', '3', '6'])]
        data = data[data['VOTURNOVER'] > 1e-8]
        # data = data[~data['SNAME'].str.contains('ST')]
        # data = data[~data['SNAME'].str.contains('N')]
        # data = data[~data['SNAME'].str.contains('C')]
        data = data.rename(columns={"SYMBOL": "ticker", "VOTURNOVER": "trade_volume"})[
            ['ticker', 'trade_volume']].dropna()
        pre_date = get_shift_date(self.trade_date)
        bm_components = get_benchmark_components(pre_date)
        data = pd.merge(data, bm_components, on='ticker', how='left')
        data['benchmark_id'] = data['benchmark_id'].fillna('other')

        path = r'D:\kevin\risk_model_jy\RiskModel\data'
        date_t_rate = pd.read_json(os.path.join(path, 'common_data/turnover_rate/{0}.json'.format(self.trade_date)),
                                   typ='series').to_frame('turnover_rate')
        date_t_rate.index.name = 'ticker'
        date_t_rate = date_t_rate.reset_index()
        date_t_rate['ticker'] = date_t_rate['ticker'].apply(lambda x: str(x).zfill(6))
        data = pd.merge(data, date_t_rate, on='ticker')
        data['equity'] = data['trade_volume'] / data['turnover_rate']

        turnover_rate = data.groupby('benchmark_id').apply(lambda x: x['trade_volume'].sum() / x['equity'].sum())
        turnover_rate.loc['market_A'] = data['trade_volume'].sum() / data['equity'].sum()
        tmp = data[data['benchmark_id'].isin(['000852', 'other'])]
        turnover_rate.loc['1000_plus_other'] = tmp['trade_volume'].sum() / tmp['equity'].sum()
        turnover_rate = turnover_rate.to_frame('value').reset_index().rename(columns={"benchmark_id": "factor_name"})
        map_dict = {"000300": "to_300", "000905": "to_500", "000852": "to_1000", "other": "to_other",
                    "market_A": "to_A", "1000_plus_other": "to_small"}
        turnover_rate['factor_name'] = turnover_rate['factor_name'].map(map_dict)

        sql_script = "SELECT * FROM mac_stock_trading_cr WHERE TRADE_DATE = {}".format(self.trade_date)
        engine = create_engine(engine_params)
        tmp = pd.read_sql(sql_script, engine)
        liq_ratio = data.groupby('benchmark_id')['trade_volume'].sum() / data['trade_volume'].sum()
        liq_ratio.loc['1000_plus_other'] = liq_ratio.loc['000852'] + liq_ratio.loc['other']
        liq_ratio.loc['top_5p'] = tmp['cr5'].values[0]
        liq_ratio.loc['top_10p'] = tmp['cr10'].values[0]
        liq_ratio = liq_ratio.to_frame('value').reset_index().rename(columns={"benchmark_id": "factor_name"})
        map_dict = {"000300": "tr_300", "000905": "tr_500", "000852": "tr_1000", "other": "tr_other",
                    "1000_plus_other": "tr_small", "top_5p": "top_5p", "top_10p": "top_10p"}
        liq_ratio['factor_name'] = liq_ratio['factor_name'].map(map_dict)

        factor = pd.concat([turnover_rate, liq_ratio])

        factor.to_csv('D:\\AlphaMonitor\\MarketLiquidity\\{}.csv'.format(self.trade_date), index=False)


class LiquidityTest:
    def __init__(self, start_date, end_date, alpha):
        self.start_date = start_date
        self.end_date = end_date
        self.alpha_series = alpha

    def run(self):
        week_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")

        data_path = "D:\\AlphaMonitor\\MarketLiquidity"
        filenames = os.listdir(data_path)
        daily_data = []
        for file_name in filenames:
            data = pd.read_csv(os.path.join(data_path, file_name))
            data['trade_date'] = file_name.split('.')[0]
            daily_data.append(data)
        daily_data = pd.concat(daily_data)
        daily_data = pd.pivot_table(daily_data, index='trade_date', columns='factor_name', values='value').sort_index()

        factor_list = []
        for i in range(1, len(week_list)):
            pre_week = week_list[i - 1]
            current_week = week_list[i]
            period_data = daily_data[(daily_data.index > pre_week) & (daily_data.index <= current_week)]
            if len(period_data) >= 4:
                factor = period_data.mean().to_frame('value').reset_index()
                factor['trade_date'] = current_week
                factor_list.append(factor)
            else:
                pass

        factor_df = pd.concat(factor_list)
        factor_df = pd.pivot_table(factor_df, index='trade_date', columns='factor_name', values='value').sort_index()

        factor_df = pd.merge(factor_df, self.alpha_series.to_frame('alpha'), left_index=True, right_index=True)

        group_alpha = group_test(factor_df, 'tr_1000', 'alpha')

        return group_alpha


class StockDivergence:
    def __init__(self, start_date, end_date, alpha):
        self.start_date = start_date
        self.end_date = end_date
        self.alpha_series = alpha

    @staticmethod
    def get_mkt_info(start_date, end_date):
        path = r'D:\kevin\risk_model_jy\RiskModel\data\common_data\chg_pct'
        listdir = os.listdir(path)
        listdir = [x for x in listdir if start_date < x.split('.')[0] <= end_date]
        data = []
        for filename in listdir:
            date_t_rate = pd.read_csv(os.path.join(path, filename), dtype={"tradeDate": str})
            date_t_rate['ticker'] = date_t_rate['ticker'].apply(lambda x: str(x).zfill(6))
            data.append(date_t_rate)

        data = pd.concat(data)
        # filter
        data = data[(data['dailyReturnReinv'] >= -0.2) & (data['dailyReturnReinv'] <= 0.2)]
        data = pd.pivot_table(data, index='tradeDate', columns='ticker', values='dailyReturnReinv').sort_index()
        data = data.dropna(how='any', axis=1)

        return data

    @staticmethod
    def calculate_factor(df, date):
        factor = pd.DataFrame(index=[date], columns=['std_1', 'std_2', 'kurt_1', 'kurt_2'])
        # method1
        factor.loc[date, 'std_1'] = df.std(axis=1).mean()
        factor.loc[date, 'kurt_1'] = df.kurt(axis=1).mean()
        # method2
        factor.loc[date, 'std_2'] = ((1 + df).prod() - 1).std()
        factor.loc[date, 'kurt_2'] = ((1 + df).prod() - 1).kurt()

        factor = pd.melt(factor, var_name='factor_name')

        return factor

    def run(self):
        week_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")
        factor_list = []
        for i in range(len(week_list) - 1):
            pre_week = week_list[i]
            current_week = week_list[i + 1]
            period_data = self.get_mkt_info(pre_week, current_week)
            if period_data.shape[0] < 4:
                continue
            pre_date = get_shift_date(current_week)
            bm_components = get_benchmark_components(pre_date)

            factor_list_period = []

            # 300
            universe = bm_components[bm_components['benchmark_id'] == '000300']['ticker'].tolist()
            idx = set(universe).intersection(set(period_data.columns.tolist()))
            factor = self.calculate_factor(period_data[idx], current_week)
            factor['universe'] = 'hs300'
            factor_list_period.append(factor)
            # 500
            universe = bm_components[bm_components['benchmark_id'] == '000905']['ticker'].tolist()
            idx = set(universe).intersection(set(period_data.columns.tolist()))
            factor = self.calculate_factor(period_data[idx], current_week)
            factor['universe'] = 'zz500'
            factor_list_period.append(factor)
            # 1000
            universe = bm_components[bm_components['benchmark_id'] == '000852']['ticker'].tolist()
            idx = set(universe).intersection(set(period_data.columns.tolist()))
            factor = self.calculate_factor(period_data[idx], current_week)
            factor['universe'] = 'zz1000'
            factor_list_period.append(factor)
            factor_list_period.append(factor)
            # other
            universe = bm_components['ticker'].tolist()
            idx = set(period_data.columns.tolist()) - set(universe)
            factor = self.calculate_factor(period_data[idx], current_week)
            factor['universe'] = 'other'
            factor_list_period.append(factor)
            # 1000 + other
            universe = bm_components[bm_components['benchmark_id'].isin(['000300', '000905'])]['ticker'].tolist()
            idx = set(period_data.columns.tolist()) - set(universe)
            factor = self.calculate_factor(period_data[idx], current_week)
            factor['universe'] = 'small'
            factor_list_period.append(factor)
            # all_market
            factor = self.calculate_factor(period_data, current_week)
            factor['universe'] = 'all'
            factor_list_period.append(factor)

            t_date_factor = pd.concat(factor_list_period)
            t_date_factor['trade_date'] = current_week

            factor_list.append(t_date_factor)

        factor_df = pd.concat(factor_list)
        factor_df['f_name'] = factor_df['universe'] + '_' + factor_df['factor_name']
        factor_df = pd.pivot_table(factor_df, index='trade_date', columns='f_name', values='value').sort_index()
        factor_df = pd.merge(factor_df, self.alpha_series.to_frame('alpha'), left_index=True, right_index=True)

        group_alpha = group_test(factor_df, 'small_std_2', 'alpha')

        return group_alpha


class MarketSpread:
    def __init__(self, start_date, end_date, alpha):
        self.start_date = start_date
        self.end_date = end_date
        self.alpha_series = alpha

    @staticmethod
    def get_mkt_info(start_date, end_date):
        path = r'D:\kevin\risk_model_jy\RiskModel\data\common_data\chg_pct'
        listdir = os.listdir(path)
        listdir = [x for x in listdir if start_date < x.split('.')[0] <= end_date]
        data = []
        for filename in listdir:
            date_t_rate = pd.read_csv(os.path.join(path, filename), dtype={"tradeDate": str})
            date_t_rate['ticker'] = date_t_rate['ticker'].apply(lambda x: str(x).zfill(6))
            data.append(date_t_rate)

        data = pd.concat(data)
        # filter
        data = data[(data['dailyReturnReinv'] >= -0.2) & (data['dailyReturnReinv'] <= 0.2)]
        data = pd.pivot_table(data, index='tradeDate', columns='ticker', values='dailyReturnReinv').sort_index()
        data = data.dropna(how='any', axis=1)

        return data

    @staticmethod
    def _calculate(df, index_return):
        win_ratio = 100 - stats.percentileofscore(np.array(df['return']), index_return)
        win_med = df[df['return'] >= index_return]['return'].median()
        lose_med = df[df['return'] < index_return]['return'].median()

        return win_ratio, win_med, lose_med

    def run(self):
        week_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")
        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format('000905', self.start_date, self.end_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        data['index_return'] = data['TCLOSE'].pct_change()
        index_return = data.set_index('TRADEDATE')['index_return']
        win_ratio_df = pd.DataFrame(
            index=week_list, columns=['win_ratio_500', 'win_spread_500', 'lose_spread_500',
                                      'win_ratio_1000', 'win_spread_1000', 'lose_spread_1000',
                                      'win_ratio_other', 'win_spread_other', 'lose_spread_other',
                                      'win_ratio_small', 'win_spread_small', 'lose_spread_small',
                                      'win_ratio_all', 'win_spread_all', 'lose_spread_all'])
        from tqdm import tqdm
        for i in tqdm(range(len(week_list) - 1)):
            pre_week = week_list[i]
            current_week = week_list[i + 1]
            period_data = self.get_mkt_info(pre_week, current_week)
            period_return = (1 + index_return.loc[period_data.index]).prod() - 1
            period_ret = (1 + period_data).prod() - 1
            period_ret = period_ret.to_frame('return')
            if period_data.shape[0] < 4:
                continue
            pre_date = get_shift_date(current_week)
            bm_components = get_benchmark_components(pre_date)

            # 500
            universe = bm_components[bm_components['benchmark_id'] == '000905']['ticker'].tolist()
            idx = set(universe).intersection(set(period_data.columns.tolist()))
            win_ratio, win_med, lose_med = self._calculate(period_ret.loc[idx], period_return)
            win_ratio_df.loc[current_week, ['win_ratio_500', 'win_spread_500', 'lose_spread_500']] = \
                [win_ratio, win_med - period_return, period_return - lose_med]
            # 1000
            universe = bm_components[bm_components['benchmark_id'] == '000852']['ticker'].tolist()
            idx = set(universe).intersection(set(period_data.columns.tolist()))
            win_ratio, win_med, lose_med = self._calculate(period_ret.loc[idx], period_return)
            win_ratio_df.loc[current_week, ['win_ratio_1000', 'win_spread_1000', 'lose_spread_1000']] = \
                [win_ratio, win_med - period_return, period_return - lose_med]
            # other
            universe = bm_components['ticker'].tolist()
            idx = set(period_data.columns.tolist()) - set(universe)
            win_ratio, win_med, lose_med = self._calculate(period_ret.loc[idx], period_return)
            win_ratio_df.loc[current_week, ['win_ratio_other', 'win_spread_other', 'lose_spread_other']] = \
                [win_ratio, win_med - period_return, period_return - lose_med]
            # small
            universe = bm_components[bm_components['benchmark_id'].isin(['000300', '000905'])]['ticker'].tolist()
            idx = set(period_data.columns.tolist()) - set(universe)
            win_ratio, win_med, lose_med = self._calculate(period_ret.loc[idx], period_return)
            win_ratio_df.loc[current_week, ['win_ratio_small', 'win_spread_small', 'lose_spread_small']] = \
                [win_ratio, win_med - period_return, period_return - lose_med]
            # all
            win_ratio, win_med, lose_med = self._calculate(period_ret, period_return)
            win_ratio_df.loc[current_week, ['win_ratio_all', 'win_spread_all', 'lose_spread_all']] = \
                [win_ratio, win_med - period_return, period_return - lose_med]

        win_ratio_df = win_ratio_df.dropna(axis=0)
        factor_df = pd.merge(win_ratio_df, self.alpha_series.to_frame('alpha'), left_index=True, right_index=True)

        # group_alpha = group_test(factor_df, 'small_std_2', 'alpha')

        name_list = ['win_ratio_other', 'f1', 'f2', 'f3', 'f4']
        group_list = []
        for name in name_list:
            group_alpha = group_test(factor_df, name, 'alpha').to_frame(name)
            group_list.append(group_alpha)

        group_df = pd.concat(group_list, axis=1)

        return group_df


class StyleFactor:
    def __init__(self, start_date, end_date, alpha):
        self.start_date = start_date
        self.end_date = end_date
        self.alpha_series = alpha

    @staticmethod
    def get_style_factor(start_date, end_date):
        """
        风格因子收益率
        """
        trade_dt = datetime.datetime.strptime(start_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=30)).strftime('%Y%m%d')
        sql_script = "SELECT * FROM factor_return where trade_date >= {} and trade_date <= {}".format(pre_date,
                                                                                                      end_date)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        data = pd.pivot_table(
            data, index='trade_date', columns='factor_name', values='factor_ret').sort_index()[style_names]

        return data

    def run_factor_return(self):
        week_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")
        style_df = self.get_style_factor(self.start_date, self.end_date)

        factor_return = []

        for i in range(len(week_list) - 1):
            pre_week = week_list[i]
            current_week = week_list[i + 1]
            period_data = style_df[(style_df.index > pre_week) & (style_df.index <= current_week)]
            if period_data.shape[0] < 4:
                continue
            period_ret = (1 + period_data).prod() - 1
            period_ret = period_ret.to_frame(current_week).T
            factor_return.append(period_ret)

        factor_return = pd.concat(factor_return)
        factor_df = pd.merge(factor_return, self.alpha_series.to_frame('alpha'), left_index=True, right_index=True)

        # group_alpha = group_test(factor_df, 'momentum', 'alpha')

        name_list = ['size', 'btop', 'earnyield', 'leverage']
        group_list = []
        for name in name_list:
            group_alpha = group_test(factor_df, name, 'alpha').to_frame(name)
            group_list.append(group_alpha)

        group_df = pd.concat(group_list, axis=1)

        return group_df

    def run_factor_vol(self):
        week_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")
        style_df = self.get_style_factor(self.start_date, self.end_date)

        factor_vol = []

        for i in range(len(week_list) - 1):
            pre_week = week_list[i]
            current_week = week_list[i + 1]
            period_data = style_df[(style_df.index > pre_week) & (style_df.index <= current_week)]
            if period_data.shape[0] < 4:
                continue
            # period_data = style_df[style_df.index <= current_week][-10:]
            rolling_vol = period_data.std().to_frame(current_week).T
            factor_vol.append(rolling_vol)

        factor_vol = pd.concat(factor_vol)
        factor_df = pd.merge(factor_vol, self.alpha_series.to_frame('alpha'), left_index=True, right_index=True)

        # group_alpha = group_test(factor_df, 'momentum', 'alpha')

        name_list = ['size', 'btop', 'earnyield', 'leverage']
        group_list = []
        for name in name_list:
            group_alpha = group_test(factor_df, name, 'alpha').to_frame(name)
            group_list.append(group_alpha)

        group_df = pd.concat(group_list, axis=1)


if __name__ == '__main__':
    # 超额收益Y
    fund_data = pd.read_excel('D:\\研究基地\\G-专题报告\\量化超额市场微观环境分析\\数据相关.xlsx', sheet_name=0)
    alpha_series = AlphaSeries('20181228', '20220422', fund_data).calculate()

    # 流动性因子
    # start_date = '20190101'
    # end_date = '20220422'
    # trading_day_list = get_trading_day_list(start_date, end_date)
    # from tqdm import tqdm
    # for trading_day in tqdm(trading_day_list):
    #     MarketLiquidity(trading_day).run()
    # results = LiquidityTest('20181228', '20220422', alpha_series).run()

    # 个股分化度因子
    # StockDivergence('20181228', '20220422', alpha_series).run()

    # 胜率因子
    # MarketSpread('20181228', '20220422', alpha_series).run()

    # 风格因子
    StyleFactor('20181228', '20220422', alpha_series).run_factor_vol()