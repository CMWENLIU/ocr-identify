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
		vas = 	[row[j] for j in res]
		res += vas
		top_ave = round(np.average(vas), 1)
		total_ave = round(np.average(row), 1)
		top_total_ave = top_ave - total_ave
		res.extend((top_ave, total_ave, top_total_ave))
		top_n.append(res)
		
	topdf = pd.DataFrame(top_n)
	cols = ['idx_'+ str(i) for i in range(1,n+1)]
	cols += ['vals_'+ str(i) for i in range(1, n+1)]
	cols +=['top_ave', 'total_ave', 'top_total_ave']
	topdf.columns = cols
	topdf.to_csv('top_n.csv', index = False)

def top_n_show(idx_result, m_records, result, top_n):
	df_idx = pd.read_csv(idx_result)
	list_res = pd.read_csv(result)
	filelist = list_res['file'].tolist()
	englist = list_res['eng'].tolist()
	df_idx = df_idx.nlargest(m_records, 'top_total_ave')
	with open('top_n_result.html', 'w') as outf:
		with open('htmlhead.txt', 'r') as fh:
			for line in fh:
				outf.write(line)
		imghead = '<img src ="'
		imgtail = '" onclick="changesize(this)">'
		for index, row in df_idx.iterrows():
			outf.write('<p>Top n average Score: ' + str(row['top_ave']) + '</p>' + '\n')
			outf.write('<p>Total average Score: ' + str(row['total_ave']) + '</p>' + '\n')
			outf.write(imghead + list_res['file'][index] + imgtail)
			outf.write('<p>--English:' + list_res['eng'][index] + '</p>' + '\n')
			for i in range(top_n):	
				outf.write('<p> Similarity Score: ' + str(row[i+top_n]) + '</p>')
				outf.write(imghead + list_res['file'][row[i]] + imgtail)	
						
			#outf.write('<p>--French:' + item['fra']+ '</p>' + '\n')
			#outf.write('<p>--Spanish:' + item['spa'] + '</p>' + '\n')
			#outf.write('<p>--Chinese:' + item['chi_sim'] + '</p>' + '\n')
			outf.write('<hr>' + '\n')
		with open('htmltail.txt', 'r') as ft:
			for line in ft:
				outf.write(line)


def main():
	#add_result('result.csv', 'compare.csv')
	#score_matrix('result.csv')
	#top_n('score_matrix.csv', 5)
	top_n_show('top_n.csv', 10, 'result.csv', 5)
if __name__== "__main__":
    main()
