import math
from datetime import datetime, timedelta

import akshare as ak


from .app import app


def sanitize_floats(obj):
    if isinstance(obj, float):
        if math.isinf(obj):
            return "Infinity"  # 或 None / 字符串标记
        elif math.isnan(obj):
            return "NaN"
    elif isinstance(obj, dict):
        return {k: sanitize_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_floats(v) for v in obj]
    return obj

@app.get("/ak/stock/sse_summary")
async def get_stock_sse_summary():
    """
    获取上海证券交易所-股票数据总貌
    """
    data = ak.stock_sse_summary()
    if not data.empty:
        return {
            "statusCode": 200,
            "data": sanitize_floats(data.to_dict())
        }
    return {
        "statusCode": 404,
        "message": "not found"
    }

@app.get("/ak/stock/szse_summary")
async def stock_szse_summary():
    """
    获取深圳证券交易所-股票数据总貌
    """
    # 获取当前日期
    now = datetime.now()
    days = [now - timedelta(days=i) for i in range(0, 10)]
    last_days = [day.strftime("%Y%m%d") for day in days]
    for day in last_days:
        # 格式化日期
        data = ak.stock_szse_summary(date=day)
        if not data.empty:
            return {
                "statusCode": 200,
                "data": sanitize_floats(data.to_dict())
            }
    return {
        "statusCode": 404,
        "message": "not found"
    }


@app.get("/ak/stock/individual_info/{symbol}")
async def get_stock_individual_info(symbol: str):
    """"
    "获取股票-个股信息"
    """
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol=symbol)
    print(stock_individual_info_em_df)
    if not stock_individual_info_em_df.empty:
        return {
            "statusCode": 200,
            "data": sanitize_floats(stock_individual_info_em_df.to_records())
        }
    return {
        "statusCode": 404,
        "message": "not found"
    }


@app.get("/ak/stock/bid_ask_em/{symbol}")
async def get_stock_bid_ask_em(symbol: str):
    """
    获取股票-个股买卖盘
    """
    stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol=symbol)
    if not stock_bid_ask_em_df.empty:
        return {
            "statusCode": 200,
            "data": sanitize_floats(stock_bid_ask_em_df.to_dict())
        }
    return {
        "statusCode": 404,
        "message": "not found"
    }


@app.get("/ak/stock/realtime/{tag}")
async def get_stock_realtime(tag: str, page: int = 1, page_size: int = 100, sort: str = "成交额"):
    """
    获取股票-个股实时行情
    """
    result = {
        "statusCode": 200,
        "message": "success"
    }
    if tag == 'sh':
        stock_realtime_df = ak.stock_sh_a_spot_em()
    elif tag == 'sz':
        stock_realtime_df = ak.stock_sz_a_spot_em()
    elif tag == 'bj':
        stock_realtime_df = ak.stock_bj_a_spot_em()
    else:
        stock_realtime_df = None
    if stock_realtime_df is not None and not stock_realtime_df.empty:
        # 处理数据
        rs_df = stock_realtime_df.sort_values(by=sort, ascending=False)
        rs_df = rs_df.iloc[(page - 1) * page_size:page * page_size]
        result["data"] = sanitize_floats(rs_df.to_dict(orient="records"))
        result["total"] = stock_realtime_df.shape[0]
    else:
        result["statusCode"] = 404
        result["message"] = "not found"
    return result



@app.get("/ak/stock/history/")
async def get_stock_zh_a_history(symbol="000001", 
                                 period="daily",
                                 start_date="20500101",
                                 end_date="20250401", 
                                 adjust="qfq",
                                #  timeout=None,
                                 q=0):
    """
    获取股票-个股历史行情
    """
    if q==0:
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, adjust=adjust, end_date=end_date)
    elif q==1:
        stock_zh_a_hist_df = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, adjust=adjust, end_date=end_date)
    elif q==2:
        stock_zh_a_hist_df = ak.stock_zh_a_hist_tx(symbol=symbol, start_date=start_date, adjust=adjust, end_date=end_date)
    if not stock_zh_a_hist_df.empty:
        return {
            "statusCode": 200,
            "data": sanitize_floats(stock_zh_a_hist_df.to_dict(orient="records"))
        }
    return {
        "statusCode": 404,
        "message": "not found"
    }