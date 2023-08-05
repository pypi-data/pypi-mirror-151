import pandas as pd

pd.set_option("display.float_format", lambda x: "%.7f" % x)

def html_to_df(page_source):
    """

    :param page_source:
    :returns:
    """
    tables = pd.read_html(page_source, decimal=",", thousands=".")[:-1]
    df = pd.concat(tables, axis=0, ignore_index=True)
    cols = df.columns
    df = df.drop([cols[2], cols[3], cols[8]], axis=1)
    colss = df.columns
    discard = [" TR"]
    df = df[~df[colss[0]].str.contains('|'.join(discard))]
    discard = [" IL"]
    df = df[~df[colss[0]].str.contains('|'.join(discard))]

    try:
        for col in df.columns[1:]:
            df[col] = df[col].astype(str).str.replace(" ", "")
            df[col] = df[col].astype(str).str.replace("kr", "")
            df[col] = df[col].astype(str).str.replace(u"\xa0", "")
            df[col] = df[col].astype(str).str.replace(u"%", "")
            df[col] = df[col].astype(str).str.replace(u",", ".")
            df[col] = df[col].astype(str).str.replace("−", "-")
            df[col] = df[col].astype(str).str.replace("—", "-")
            df[col] = df[col].astype(float)
    except Exception as e:
        print(e)
        print(col)
        print(df.columns[1:])
        print(df)

    df[df.columns[5]] = df.fillna(0)[df.columns[5]] + df.fillna(0)[df.columns[6]]
    df = df.drop([df.columns[6]], axis=1)

    columns_new = []
    for column in df.columns:
        columns_new.append(column.replace("▲", "").replace("▼", "").strip())

    df.columns = columns_new

    return df
