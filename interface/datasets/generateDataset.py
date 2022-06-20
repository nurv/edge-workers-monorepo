import pandas as pd
import pymongo
from ludwig.utils.data_utils import add_sequence_feature_column
from pymongo.collection import Collection


def generateDataset(collection: Collection, metric, feature_name, window_size=20, lookahead=1, train=0.6, vali=0.2,
                    test=0.2, normalize=True):
    objects = collection.find().sort("timestamp", 1)
    values = []

    for object in objects:
        values.append(object["metrics"][metric])

    df = pd.DataFrame(values)
    df.columns = [feature_name]
    df.fillna(method='backfill').fillna(method='ffill')

    # normalize
    if normalize:
        mean = df[feature_name].mean()
        std = df[feature_name].std()
        df[feature_name] = ((df[feature_name] - df[feature_name].mean()) /
                          df[feature_name].std())
    else:
        mean = 0
        std = 0

    train_size = int(train * len(df))
    vali_size = int(vali * len(df))

    # train, validation, test split
    df['split'] = 0
    df.loc[
        (
                (df.index.values >= train_size) &
                (df.index.values < train_size + vali_size)
        ),
        ('split')
    ] = 1
    df.loc[
        df.index.values >= train_size + vali_size,
        ('split')
    ] = 2

    add_sequence_feature_column(df, feature_name, window_size)
    return df.to_csv(), mean, std
