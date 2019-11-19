import os

f = open('new_summary.txt', 'wt')
work_dir = '/root/ml-20m/movie_info'
for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
	f.write('%s,%d\n' %(parent,len(filenames)))
f.close()

