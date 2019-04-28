from simpledbf import Dbf5
import pandas as pd
import numpy as np
import re


def CVAPfileCheck(filename):
    check = re.findall(r'cvap', filename)
    if check:
        return True
    else:
        return False


def CVAPcolumnChange(df):
    df.rename(index=str, columns={"BLOCK": "block_key"}, inplace=True)

    return df


def importDBF(filename):
    dbf = Dbf5(filename)
    df = dbf.to_dataframe()
    column_names = df.columns

    return df


def importCSV(filename):
    df = pd.read_csv(filename)
    columnNames = df.columns
    dictOfWords = {i: 'object' for i in columnNames}
    df = pd.read_csv(filename, dtype=dictOfWords)

    return df


## Combination of two functions above
def importData(filename):

    check = CVAPfileCheck(filename)
    # Match file names based on if .csv or .dbf to properly import as a dataframe
    if filename.endswith('.csv'):

        df = importCSV(filename)

        if check:
            df = CVAPcolumnChange(df)
        else:
            pass

        df.columns = map(str.lower, df.columns)

        return df

    elif filename.endswith('.dbf'):
        df = importDBF(filename)

        if check:
            df = CVAPcolumnChange(df)
        else:
            pass

        df.columns = map(str.lower, df.columns)

        return df

    else:
        print('Imported data format not supported.')


def filterData(df, filterVar):
    if filterVar == None:
        return df
    else:
        for key, value in filterVar.items():
            df = df[df[key].isin(value)]

        return df


def mergeCvapBlk(df1, df2, left, right, filterVar=None):
    merged = pd.merge(df1, df2, left_on=left, right_on=right, how='inner')

    merged = filterData(merged, filterVar)

    return merged


def partialBlck(df):
    df['pctblk'] = pd.to_numeric(df['pctblk'])
    partialVec = df.loc[:, 'pctblk'] / 100
    cvap_df = df.loc[:, 'citizen':'cvap']
    ## Multiply out partial blocks using pctblk, or % of the block in precinct n
    cvap_by_sr = cvap_df.mul(partialVec, axis=0)

    return cvap_by_sr


def concatPartialCVAP(df1, df2):
    df = pd.concat([df1, df2], axis=1)

    return df