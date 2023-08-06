class WordCluster:
    def __init__(self, list_of_strings, threshold_for_clustering, debug_mode = False):
        """
        @param list_of_strings ['str1','str2']
        @param threshold_for_clustering: number of sequence in string 3-4 is best
        @param debug_mode: bool If true prints will be shonw
        """
        self.list_of_strings = list_of_strings
        self.threshold_for_clustering = threshold_for_clustering
        self.cluster_categories = None # will be calculated
        self.categorized_words = None # will be calculated
        self.debug_mode = debug_mode

    def log(self, message, level =1):
        if self.debug_mode:
            lines = '-'*level
            print(f"{lines}>{message}")
        else:
            pass

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

    def remove_blanks(self, x): 
        return x.replace(" ","") if x is not None else x

    def intersection_exists_and_more_than_treshold(self, x, y):
        if self.str_intersection(x, y, False) is not None:
            self.log("Lenx:", level = 1)
            self.log(len(self.str_intersection(self.remove_blanks(x), self.remove_blanks(y), False)))
            if len(self.str_intersection(self.remove_blanks(x), self.remove_blanks(y), False))>=self.threshold_for_clustering:
                return True
            else:
                return False
        else:
           return False

    def find_cluster_categories(self):
        MYLIST = self.list_of_strings
        initial_seed_words = [item[0:self.threshold_for_clustering] for item in MYLIST]
        #cleaned_from_shorts = [x if len(x)>self.threshold_for_clustering else None for x in initial_seed_words]
        seed_words=set(initial_seed_words) # initial cluster list
        seed_words = [self.remove_blanks(sw) for sw in seed_words]
        self.cluster_categories = seed_words
        return seed_words

    def find_cluster_for_this_word(self, word, cluster_categories):
        """
        @word: str
        @cluster_categories: set
        """
        seed_words = cluster_categories.copy()
        self.log(f"Seed words: {seed_words}")
        rt = ''
        for seed in seed_words:
            self.log(f"Whether {word} is in the category ~{seed}")
            if seed in word:
                rt= seed
            else:
                pass
        return rt

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