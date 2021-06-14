#!/usr/bin/env python
'''
file: mtsp_json
author: adh
created_at: 6/14/21 12:03 PM
'''
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def json_to_df(path):
    logger.debug(f"Reading json data from {path}")
    df = pd.read_json(path,orient="index")
    logger.info(f"Read {len(df)} records from {path}")
    return df


def clean_df(df):
    cols = ['path', 'name', 'disclosure_date', 'type', 'description', 'platform', 'arch', 'mod_time']

    df = df.reset_index().rename(columns={'index': 'filepath'})
    df['mod_time'] = pd.to_datetime(df['mod_time'])

    # references is a column of lists
    # need to break it into one row per item in each list
    df2 = (pd.melt(df.references.apply(pd.Series).reset_index(),
                   id_vars=['index'],
                   value_name='references')
           .set_index(['index'])
           .drop('variable', axis=1)
           .dropna()
           .sort_index()
           )
    # merge the broken out rows back into the original data
    df3 = df[cols].join(df2).dropna()
    df3 = df3.rename(columns={'references': 'reference', })
    df3['reference'] = df3['reference'].str.strip()
    df3 = df3.set_index('reference')
    df3 = df3.sort_values(by="mod_time",ascending=True)

    return df3

def only_cves(df):
    df2 = pd.DataFrame(df.loc[df.index.str.startswith('CVE')])
    return df2


def main():
    pass


if __name__ == '__main__':
    main()
