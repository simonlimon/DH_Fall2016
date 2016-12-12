# Script to merge Warren's grid data with our own data.
import glob
import os

import pandas as pd


def merge(warren_csv_path, marshall_csv_directory):
    grid = pd.DataFrame.from_csv(warren_csv_path)
    result = pd.DataFrame()
    for filename in glob.glob(os.path.join(marshall_csv_directory, '*.csv')):
        chapter = int(filename.split('_')[1].split('.')[0])
        df = pd.DataFrame.from_csv(filename)
        df['chapter'] = chapter
        for index, row in df.iterrows():
            if row.site != 'Sk' or not isinstance(row.coord, str): continue
            match = grid.loc[grid.GRID_ID == str(row.coord)]
            if match.shape[0] == 0: continue
            row = match.iloc[0].append(row)
            row['number'] = int(index)
            result = result.append(row, ignore_index=True)

    print result
    result.to_csv('merge.csv')

def merge_objects_rooms(rooms_csv, objects_csv):
    df = pd.DataFrame.from_csv(objects_csv)
    rooms = pd.DataFrame.from_csv(rooms_csv)
    result = pd.DataFrame()

    for index, row in rooms.iterrows():
        print index
        match = df.loc[df.index == row.GRID_ID]
        if match.shape[0] > 0:
            row = match.iloc[0].append(row)
            result = result.append(row, ignore_index=True)
        else:
            result = result.append(row)

    print result
    result.to_csv('merge.csv')


if __name__ == '__main__':
    merge_objects_rooms('data/rooms.csv', 'data/objects.csv')

