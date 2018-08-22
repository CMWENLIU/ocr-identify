import re
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def add_result(inputfile, compare):
    df = pd.read_csv(inputfile)
    df = df[df['fra'].str.len() > 2]
    df['word_counts'] = df['fra'].str.split().str.len()
    with open('ave_std.txt', 'w') as re:
        re.write('average_word_counts: ' + str(round(np.mean(df['word_counts'].tolist()), 1)) + '\n')
        re.write('std_word_counts: ' + str(round(np.std(df['word_counts'].tolist()), 1)))
    langlist = df['fra'].tolist()
    comdf = pd.read_csv(compare)
    comp = comdf[comdf['tocompare'] == 1]
    compList = comp['fra'].tolist()
    print(len(compList))
    for i, c in enumerate(compList):
        colName = 'Score_' + str(i)
        score = []
        for l in langlist:
            score.append(fuzz.partial_ratio(l, c))
        df[colName] = score
    df.to_csv('result_statistic.csv', index=False)	


def main():
    add_result('result.csv', 'compare.csv')
  
if __name__== "__main__":
    main()
