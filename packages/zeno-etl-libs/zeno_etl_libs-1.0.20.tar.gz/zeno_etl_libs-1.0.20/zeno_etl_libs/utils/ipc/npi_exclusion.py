import pandas as pd

def omit_npi_drugs(safety_stock_df, store_id, reset_date, db, schema, logger=None):
    logger.info(f"Omit NPI drugs for SID: {store_id}")
    npi_drugs_query = """
            select distinct "drug-id"  as drug_id
            from "{schema}"."omit-ss-reset" 
            where "store-id" = {0}
            and "is-active" = 1
            and "start-date" <= '{1}'
            and "end-date" >= '{1}'
            """.format(store_id, reset_date, schema=schema)
    df_npi_drugs = db.get_df(npi_drugs_query)
    df_npi_drugs["is_npi"] = 'Y'

    safety_stock_df = safety_stock_df.merge(df_npi_drugs, on="drug_id", how="left")
    safety_stock_df["is_npi"] = safety_stock_df["is_npi"].fillna('N')

    npi_df = safety_stock_df.loc[safety_stock_df["is_npi"]=='Y']
    rest_df = safety_stock_df.loc[safety_stock_df["is_npi"]!='Y']

    # set SS, ROP, OUP = 0 for all NPI drugs
    npi_df["safety_stock"] = 0
    npi_df["reorder_point"] = 0
    npi_df["order_upto_point"] = 0

    safety_stock_df = pd.concat([rest_df, npi_df], axis=0, ignore_index=True)
    safety_stock_df = safety_stock_df.drop(['is_npi'], axis=1)

    return safety_stock_df