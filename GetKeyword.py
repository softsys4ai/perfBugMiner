#coding:utf-8
from matplotlib import pyplot as plt
from wordcloud import WordCloud
 
string = 'SSD mobilenet inference is slower w/ MKL.From the benchmark_model results, we could see that _MklConv2DWithBias is the culprit'

font = r'C:\Windows\Fonts\FZSTK.TTF'

def GetKeyword(s):
	s = s.replace("tf","tensorflow")
	wc = WordCloud().generate(s)
	max1 = ''
	max1in = 0.0
	max2 = ''
	max2in = 0.0
	for k in wc.words_:
		# print k,wc.words_[k]
		if wc.words_[k] > max1in:
			max2 = max1
			max1 = k
			max2in = max1in
			max1in = wc.words_[k]
			continue
		if wc.words_[k] > max2in:
			max2 = k
			max2in = wc.words_[k]
	return (max1,max2)



# plt.imshow(wc)
# plt.axis('off')
# plt.show()
# print GetKeyword(string)
