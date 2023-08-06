import pandas as pd
import numpy as np
import datetime

from zeno_etl_libs.db.db import PostGre

'''
Steps -
1. Get Auto short total time -> from creation to received data
2. If marked as lost make it 7
'''


def lead_time(store_id, cal_sales, reset_date, db, schema, logger=None):

    # =========================================
    # TEMPORARY - GET DATA FROM PG IF NOT IN RS
    pg = PostGre()
    pg.open_connection()
    # =========================================

    sb_creation_delay_ethical = 1
    sb_creation_delay_other = 1
    sb_creation_delay_generic = 2

    end_date = str(
        datetime.datetime.strptime(reset_date, '%Y-%m-%d') -
        datetime.timedelta(7))
    begin_date = str(cal_sales.date.dt.date.max() - datetime.timedelta(97))

    print(begin_date, end_date)
    lead_time_query = """
        select store_id, drug_id, drug_type, status, created_at, received_at
        from ops_fulfillment
        where request_type = 'Auto Short'
        and store_id = {store_id}
        and created_at <= '{end_date}'
        and created_at >= '{begin_date}'
        and status not in ('failed', 'deleted')
        """.format(store_id=store_id, end_date=end_date, begin_date=begin_date)
    lead_time = pd.read_sql_query(lead_time_query, pg.connection)  # FROM PG

    lead_time['created_at'] = pd.to_datetime(lead_time['created_at'])
    lead_time['received_at'].replace({'0000-00-00 00:00:00': ''}, inplace=True)
    lead_time['received_at'] = pd.to_datetime(lead_time['received_at'])

    lead_time['lead_time'] = (
        lead_time['received_at'] - lead_time['created_at']).\
        astype('timedelta64[h]')/24
    lead_time['lead_time'].fillna(7, inplace=True)
    lead_time['lead_time'] = np.select(
        [lead_time['drug_type'] == 'generic',
         lead_time['drug_type'] == 'ethical'],
        [lead_time['lead_time'] + sb_creation_delay_generic,
         lead_time['lead_time'] + sb_creation_delay_ethical],
        default=lead_time['lead_time'] + sb_creation_delay_other)

    lt_store_mean = round(lead_time.lead_time.mean(), 2)
    lt_store_std = round(lead_time.lead_time.std(ddof=0), 2)

    lt_drug = lead_time.groupby('drug_id').\
        agg({'lead_time': [np.mean, np.std]}).reset_index()
    lt_drug.columns = ['drug_id', 'lead_time_mean', 'lead_time_std']
    lt_drug['lead_time_std'] = np.where(
        lt_drug['lead_time_std'].isin([0, np.nan]),
        lt_store_std, lt_drug['lead_time_std'])

    # =========================================
    pg.close_connection()
    # =========================================

    return lt_drug, lt_store_mean, lt_store_std
