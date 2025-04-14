import akshare as ak
import math


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
            tmp_df[col] = tmp_df[col].apply(sanitize_floats)
        result.extend(tmp_df.to_dict(orient='records'))
    return result
        

if __name__ == '__main__':
    res = get_realtime_data()
    print(res)
    print(len(res))
    # get_realtime_data()