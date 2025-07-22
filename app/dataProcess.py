import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
from sklearn.preprocessing import OrdinalEncoder


class DataCleaner:
    def __init__(self):
        self.encoder = None

    def fit(self, df):
        # Fit encoder on categorical columns
        categorical_cols = ['merchant_category', 'transaction_type']
        self.encoder = OrdinalEncoder()
        self.encoder.fit(df[categorical_cols].astype('category'))
        return self

    def transform(self, df):
        df = df.copy()
        df_orig = df.copy()


        # categorical columns handling
        categorical_cols = ['merchant_category', 'location', 'transaction_type']
        df[categorical_cols] = df[categorical_cols].astype('category')
        df["transaction_datetime"] = pd.to_datetime(df["transaction_datetime"])


        # feature engineering
        df = df.sort_values(by=['customer_id', 'transaction_datetime'])
        df['last_transaction_datetime'] = df.groupby('customer_id')['transaction_datetime'].shift(1)
        df['days_since_last_txn'] = (df['transaction_datetime'] - df['last_transaction_datetime']).dt.days



        location_freq = df.groupby(['customer_id', 'location'], observed=True).size().reset_index(
                name='location_freq_for_customer')
        df = df.merge(location_freq, on=['customer_id', 'location'], how='left')


        df['is_night_transaction'] = (df['transaction_datetime'].dt.hour).apply(lambda x: 1 if x < 6 else 0)


        df["transaction_week"] = df["transaction_datetime"].dt.to_period("W").apply(lambda r: r.start_time)
        weekly_freq = df.groupby(["customer_id", "transaction_week"]).size().reset_index(name="weekly_txn_count")
        df = df.merge(weekly_freq, on=["customer_id", "transaction_week"], how="left")


        df["transaction_amount_log"] = (np.log1p(df["transaction_amount"]))


        df = df.dropna()


        # categorical encoding

        cat_enc_cols = ['merchant_category', 'transaction_type']
        df[cat_enc_cols] = self.encoder.transform(df[cat_enc_cols])

        return df

    def fit_transform(self, df):
        self.fit(df)
        return self.transform(df)

def process(df):
    cleaner = DataCleaner()
    df_clean = cleaner.fit_transform(df)
    # Save the fitted cleaner for later use

    return df_clean

