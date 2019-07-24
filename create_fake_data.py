import numpy as np
import pandas as pd


np.random.seed(0)

def load_data(path):
    df = pd.read_csv(path)
    df = df[['HO', 'DEM', 'TEN', 'GIOI_TINH', 'NGAY', 'THANG', 'NAM', 'MA_TINH_KS',
             'MA_HUYEN_KS', 'MA_XA_KS', 'SO_CMTND']]
    
    df['HO'] = df['HO'].astype(str)
    df['DEM'] = df['DEM'].astype(str)
    df['TEN'] = df['TEN'].astype(str)
    df['GIOI_TINH'] = df['GIOI_TINH'].astype(str)
    df['NGAY'] = df['NGAY'].astype(str)
    df['THANG'] = df['THANG'].astype(str)
    df['NAM'] = df['NAM'].astype(str)
    df['MA_TINH_KS'] = df['MA_TINH_KS'].astype(str)
    df['MA_HUYEN_KS'] = df['MA_HUYEN_KS'].astype(str)
    df['MA_XA_KS'] = df['MA_XA_KS'].astype(str)
    df['MA_XA_KS'] = df['MA_XA_KS'].apply(lambda x: '0'*(5-len(str(x))) + str(x))
    df['SO_CMTND'] = df['SO_CMTND'].astype(str)
    return df

def create_data(row, index):
    index.reverse()
    data = []
    for idx in index:
        sample = []
        for i in range(len(row)):
            if idx[i] == '0':
                sample.append(row[i])
            elif idx[i] == '1':
                temp = row[i]
                if i == 3:    #fake gioi_tinh
                    fake = str(1 - int(temp))
                    sample.append(fake)
                elif i == 4:    #fake ngay sinh
                    fake = np.random.randint(1, 32)
                    while fake == int(temp):
                        fake = np.random.randint(1, 32)
                    sample.append('0'*(2-len(str(fake))) + str(fake))
                elif i == 5:    #fake thang sinh
                    fake = np.random.randint(1, 13)
                    while fake == int(temp):
                        fake = np.random.randint(1, 13)
                    sample.append('0'*(2-len(str(fake))) + str(fake))
                elif i == 6:    #fake nam sinh
                    fake = np.random.randint(1990, 2019)
                    while fake == int(temp):
                        fake = np.random.randint(1990, 2019)
                    sample.append(str(fake))
                else:   #fake cac truong du lieu khac
                    j = np.random.randint(len(temp))
                    while 1:
                        try:
                            k = np.random.randint(len(d[temp[j]]))
                            break
                        except KeyError:
                            j = np.random.randint(len(temp))
    #                temp = temp.replace(u'\xa0', u' ')
                    fake = temp[:j] + d[temp[j]][k] + temp[j+1:]
                    sample.append(fake)
        data.append(sample)
    df = pd.DataFrame(data, columns=row.keys())
    df['LABEL'] = index
    return df

if __name__ == '__main__':
    path = './data/fixed_data.csv'
    df = load_data(path)
    count = 0
    d = {}
    with open('./data/replace.txt') as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
        f.close()
    
    binary = [bin(i)[2:] for i in range(2048)]
    index = ['0'*(11-len(i)) + str(i) for i in binary]
    
    import random
    random_index = [index[0]] + random.choices(index[1:], k=99)
    index = random_index
    print(index)

    fake_samples = []
    for idx, row in df.iterrows():
        print('Running sample ' + str(idx))
        fake_samples.append(create_data(row, index))
    fake_data = pd.concat(fake_samples)
    fake_data.to_csv('./data/fake_data_1e5.csv')
    


