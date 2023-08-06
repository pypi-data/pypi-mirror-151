import importlib.machinery

from regex import R # to import files as module
pack = importlib.machinery.SourceFileLoader('wordcluster','wordcluster/__init__.py').load_module()
mylist = ['vanlı','vanda','vansız','vandan','vanlılar','mut','olmut','muttu','vanlılardan','muttulamak']
#for treshold in range(1,5):
treshold = 3  
wcu = pack.WordCluster(mylist,treshold, debug_mode = True)
cluster_categories = wcu.find_cluster_categories()
categorized_words =wcu.categorize_all_words(cluster_categories)
print(categorized_words)


