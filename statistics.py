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


def score_matrix(inputfile):
	df = pd.read_csv(inputfile)
	df = df[df['eng'].str.len() > 2]
	df['word_counts'] = df['eng'].str.split().str.len()
	with open('ave_std.txt', 'w') as re:
		re.write('average_word_counts: ' + str(round(np.mean(df['word_counts'].tolist()), 1)) + '\n')
		re.write('std_word_counts: ' + str(round(np.std(df['word_counts'].tolist()), 1)))
	langlist = df['eng'].tolist()
	complist = langlist
	filelist = df['file'].tolist()
	score_matrix = np.zeros((len(langlist), len(langlist)))
	for i, l in enumerate(langlist):
		for j, c in enumerate(complist):
			score_matrix[i][j] = fuzz.partial_ratio(l, c)
		print('Row ' + str(i+1) + '/' + str(len(langlist)) + ' has been finished!')
	df_score = pd.DataFrame(score_matrix)
	df_score.to_csv('score_matrix.csv', index=False)	

def top_n(score_matrix, n):
	df = pd.read_csv(score_matrix)
	matrix = df.values
	top_n = []
	for i, row in enumerate(matrix):
		res = np.argsort(row)[::-1][1:n+1].tolist()
		res.append(round(np.average(row), 1))
		res.append(row[res[0]])
		res.append(np.amin(row))
		top_n.append(res)
		
	topdf = pd.DataFrame(top_n)
	topdf.to_csv('top_n.csv')

def main():
	#add_result('result.csv', 'compare.csv')
	#score_matrix('result.csv')
	top_n('score_matrix.csv', 5)
if __name__== "__main__":
    main()
