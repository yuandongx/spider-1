from datetime import datetime, date
import math

from loguru import logger
import akshare as ak

def sanitize_dtypes(obj):
    if isinstance(obj, float):
        if math.isinf(obj):
            return "Infinity"  # 或 None / 字符串标记
        elif math.isnan(obj):
            return "NaN"
    elif isinstance(obj, dict):
        return {k: sanitize_dtypes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_dtypes(v) for v in obj]
    elif isinstance(obj, date):
        return obj.strftime("%Y%m%d")
    return obj


def get_realtime_data():
    """
    获取实时数据
    """
    # 获取实时数据
    sh_a = ak.stock_sh_a_spot_em()
    sh_a['区域'] = 'sh'
    sz_a = ak.stock_sz_a_spot_em()
    sz_a['区域'] = 'sz'
    bj_a = ak.stock_bj_a_spot_em()
    bj_a['区域'] = 'bj'
    result = []
    for df in [sh_a, sz_a, bj_a]:
        # 处理数据
        tmp_df = df.copy()
        tmp_df['idx'] = tmp_df['代码'].apply(lambda x: f'{df["区域"].values[0]}@{x}')
        for col in tmp_df.columns:
            tmp_df[col] = tmp_df[col].apply(sanitize_dtypes)
        result.extend(tmp_df.to_dict(orient='records'))
    return result
        
def get_stock_zh_a_history(symbol="000001", q=0, limit=0):
    """
    获取股票-个股历史行情
    """
    now = datetime.now()
    last_year = now.year - 1
    start_date = f"{last_year}{now.month:0>2}{now.day:0>2}"
    end_date = f"{now.year}{now.month:0>2}{now.day:0>2}"
    period = "daily"
    adjust = "qfq"
    logger.info(f"获取股票 {symbol}【{symbol}】 日历史数据，时间范围: {start_date} - {end_date}")
    # 获取历史数据
    if q==0:
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, adjust=adjust, end_date=end_date)
    elif q==1:
        stock_zh_a_hist_df = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, adjust=adjust, end_date=end_date)
    elif q==2:
        stock_zh_a_hist_df = ak.stock_zh_a_hist_tx(symbol=symbol, start_date=start_date, adjust=adjust, end_date=end_date)
    if not stock_zh_a_hist_df.empty:
        logger.info(f"获取股票 {symbol}[{start_date}-{end_date}] 日历史数据成功，数据量: {stock_zh_a_hist_df.shape[0]}")
        # 处理数据
        for col in stock_zh_a_hist_df.columns:  
            stock_zh_a_hist_df[col] = stock_zh_a_hist_df[col].apply(sanitize_dtypes)
        stock_zh_a_hist_df['idx'] = stock_zh_a_hist_df['日期']
        if limit > 0:
            stock_zh_a_hist_df = stock_zh_a_hist_df.sort_values(by='日期',ascending=False).head(10)
        return stock_zh_a_hist_df.to_dict(orient="records")
    return []
    

def get_all_zh_stocks():
    """
    获取所有股票
    """
    stock_zh_a_spot_df = ak.stock_zh_a_spot_em()
    stock_zh_a_spot_df['idx'] = stock_zh_a_spot_df['代码'].apply(lambda x: f'sh@{x}')
    stock_zh_a_spot_df['区域'] = 'sh'
    stock_zh_b_spot_df = ak.stock_zh_b_spot_em()
    stock_zh_b_spot_df['idx'] = stock_zh_b_spot_df['代码'].apply(lambda x: f'sz@{x}')
    stock_zh_b_spot_df['区域'] = 'sz'
    result = []
    for df in [stock_zh_a_spot_df, stock_zh_b_spot_df]:
        # 处理数据
        tmp_df = df.copy()
        for col in tmp_df.columns:
            tmp_df[col] = tmp_df[col].apply(sanitize_floats)
        result.extend(tmp_df.to_dict(orient='records'))
    return result
if __name__ == '__main__':
    res = get_realtime_data()
    print(res)
    print(len(res))
    # get_realtime_data()