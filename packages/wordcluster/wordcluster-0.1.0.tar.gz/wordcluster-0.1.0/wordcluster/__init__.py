class WordCluster:
    
    def __init__(self, list_of_strings, threshold_for_clustering):
        """
        @param list_of_strings ['str1','str2']
        @param threshold_for_clustering: number of sequence in string 3-4 is best
        """
        self.list_of_strings = list_of_strings
        self.threshold_for_clustering = threshold_for_clustering
        self.cluster_categories = None # will be calculated
        self.categorized_words = None # will be calculated
        

    def str_intersection(self, str_left, str_right, ignore_order = True ):
        common_letters = set(str_left) & set(str_right)
        str_intersected = ''
        for c in str_left:
            if (c in common_letters) and (c not in str_intersected):
                str_intersected += c
        if ignore_order:
            pass
        else:
            if str_intersected in str_left and str_intersected in str_right:
                return str_intersected
            else:
                return None
        return str_intersected

    def remove_blanks(self, x): return x.replace(" ","")

    def find_cluster_categories(self):
        MYLIST = self.list_of_strings
        # Finding Clusters
        threshold_for_clustering = self.threshold_for_clustering
        seed_words=MYLIST.copy()
        
        for x in MYLIST:
            for y in seed_words:
                try:
                    # If these words are same pass
                    if x == y:
                        pass
                    else:
                        # if similarity exists and similar charts are more than threshold
                        if self.str_intersection(x, y, False) is not None:
                            if len(self.str_intersection(self.remove_blanks(x), self.remove_blanks(y), False))>self.threshold_for_clustering:
                                print(f"{x},{y}")
                                # then check whether this word in the seed_words
                                for seed in seed_words:
                                    print(f"--->{seed}")
                                    if self.str_intersection(x, seed, False) != None:
                                        print(f"----->Seed word removed: {seed}")
                                        seed_words.remove(x)
                                    if self.str_intersection(y, seed, False) != None:
                                        seed_words.remove(y)
                                        print(f"----->Seed word removed: {seed}")
                except:
                    pass
        seed_words = [self.remove_blanks(sw) for sw in seed_words]
        self.cluster_categories = seed_words
        return seed_words

    def find_cluster_for_this_word(self, word, cluster_categories):
        """
        @word: str
        @cluster_categories: set
        """
        seed_words = cluster_categories
        print(f"Seed words: {seed_words}")
        for cluster in seed_words:
            try:
                print(f"{word}-vs-{cluster}")
                if word == cluster:
                    return cluster
                else:
                    if self.str_intersection(self.remove_blanks(word), self.remove_blanks(cluster), False) is not None:
                            if len(self.str_intersection(self.remove_blanks(word),self.remove_blanks(cluster), False))>self.threshold_for_clustering:
                                return cluster
                            else:
                                return None
                    else:
                        return None
            except:
                return None

    def categorize_all_words(self, cluster_categories):
        """
        @cluster_categories: set
        """
        assignments= []
        for word in self.list_of_strings:
            assignments.append({
                "word": word,
                "cluster": self.find_cluster_for_this_word(word, cluster_categories)
            })
        self.categorized_words = assignments
        return assignments