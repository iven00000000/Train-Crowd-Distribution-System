import os
from PIL import Image
import numpy as np
import operator
import csv
import fnmatch
from math import *
from matplotlib import pyplot as plt
import random 

#2017_06_05_24_24_24.123456.jpg

threshold = 1
dataDc = {}
for file in fnmatch.filter(os.listdir('.'), '*.p'):
	if not os.path.isfile(file):
		continue
	data = {}
	fn, extFn = os.path.splitext(file)
	# if '.py' in extFn or '.csv' == extFn or '.dat' == extFn:
	# 	continue

	if extFn == '.p':
		crowdLvHuman, fn, res, data['PostLv'] = fn.split('-')
		data['Res'] = tuple(int(val) for val in res.split('_'))
		data['CrowdLvHuman'] = crowdLvHuman
		with open(file, 'rb') as fd:		
			data['BlkSizes'] = pickle.load(fd)
	else:
		data['ImgFn'] = file
		print file
		crowdLvHuman, fn = fn.split('-')
	if fn not in dataDc:
		dataDc[fn] = data
	else:
		dataDc[fn].update(data)

maxRes = max([ data['Res'][0] * data['Res'][1] for fn, data in dataDc.iteritems() ])
bins = [ 2**i for i in range( 0, int(ceil(log(maxRes, 2)))+1 ) ]
print 'bins:', bins

csvfile = open('stat.csv', 'wb')
fieldnames = ['filename','QuietMean','QuietStd','QuietVar','QuietMax','QuietMin','QuietHist','CrowdLvHuman']
writer = csv.DictWriter(csvfile,fieldnames=fieldnames,extrasaction='ignore')
writer.writeheader()
#spamwriter.writerow('filename','Mean','Std','Var','Max','Min','Hist','Block amount')
for fn, data in dataDc.iteritems():
	quietSizeLs = filter(lambda a: a >= threshold, data['BlkSizes'])
	data['QuietBlkSizes'] = quietSizeLs
	#Image.open(data['ImgFn']).resize(data['Res']).show()
	data['QuietMean'] = np.mean(quietSizeLs)
	data['QuietStd'] = np.std(quietSizeLs)
	data['QuietVar'] = np.var(quietSizeLs)
	data['QuietMax'] = max(quietSizeLs)
	data['QuietMin'] = min(quietSizeLs)
	data['QuietHist'], data['Bins'] = np.histogram(quietSizeLs, bins=bins)
	data['filename'] = fn
	print 'filename:', fn
	print 'crowd level - human eye:', data['CrowdLvHuman']
	print 'mean:', data['QuietMean']
	print 'std:', data['QuietStd']
	print 'var:', data['QuietVar']
	print 'max:', data['QuietMax']
	print 'min:', data['QuietMin']
	print 'log-hist:', data['QuietHist']
	print 'amount:', len(quietSizeLs)
	writer.writerow(data)
	plt.figure(figsize=(16, 9))
	plt.xscale('log')
	plt.yscale('log')
	colors = [random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)]
	plt.hist( data['QuietBlkSizes'], bins=bins, label= '%s-%s-%s' %(fn, int(data['QuietMean']), int(data['CrowdLvHuman'])), color = colors )
	plt.title('filename' + fn)
	plt.legend(loc='upper right')
	# plt.show()
	plt.savefig('stat\\'+ data['CrowdLvHuman'] + '_' + fn)
csvfile.close()
x = [ data['QuietHist'][:-2] for fn, data in dataDc.iteritems()]
for i in range(len(x[0])):
	print [ xx[i] for xx in x ]
print len(x)
print len(x[0])

y = [ data['CrowdLvHuman'] for fn, data in dataDc.iteritems()]
print len(y)
print np.linalg.lstsq(x, y) 
a,e,r,s = np.linalg.lstsq(x, y) 


# plt.figure(figsize=(16, 9))
# plt.xscale('log')9
# plt.yscale('log')
# plt.hist([ data['QuietBlkSizes'] for fn, data in dataDc.iteritems() ], bins=bins, label=[ '%s-%s-%s' %(fn, int(data['QuietMean']), int(data['CrowdLvHuman'])) for fn, data in dataDc.iteritems() ])
# plt.title('filename')
# plt.legend(loc='upper right')
# plt.show()


#fd.write('\n%s' crowdAns)
