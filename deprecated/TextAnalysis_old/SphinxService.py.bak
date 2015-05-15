"""
written for iom db. not updated for tweets
"""
from sphinxapi import SphinxClient
from IOMDataService import IOMService
import re  # used by mask method


class SphinxSearch(SphinxClient, IOMService):
    def __init__(self):
        # instantiate a new SphinxClient object
        SphinxClient.__init__(self)
        #Connection to mysql abstraction layer
        IOMService.__init__(self)
        self.connect_to_mysql('false')
        #Print reminder that searchd needs to be running
        print "Don't forget to start sphnix from the terminal: "
        print "cd /usr/local/sphinx"
        print "sudo searchd"
        #connection variables
        HOST = 'localhost'
        PORT = 9312
        # connect to server
        self.SetServer(HOST, PORT)
        #set the number of docs returned to be greater than the number we have (first argument is the offset)
        self.SetLimits(0, 5000, 5000)
        # known searchd status codes
        SEARCHD_OK = 0
        SEARCHD_ERROR = 1
        SEARCHD_RETRY = 2
        SEARCHD_WARNING = 3

        # known match modes
        self.SPH_MATCH_ALL = 0
        self.SPH_MATCH_ANY = 1
        self.SPH_MATCH_PHRASE = 2
        self.SPH_MATCH_BOOLEAN = 3
        self.SPH_MATCH_EXTENDED = 4
        self.SPH_MATCH_FULLSCAN = 5
        self.SPH_MATCH_EXTENDED2 = 6

        # known ranking modes (extended2 mode only)
        SPH_RANK_PROXIMITY_BM25 = 0  # default mode, phrase proximity major factor and BM25 minor one
        SPH_RANK_BM25 = 1  # statistical mode, BM25 ranking only (faster but worse quality)
        SPH_RANK_NONE = 2  # no ranking, all matches get a weight of 1
        SPH_RANK_WORDCOUNT = 3  # simple word-count weighting, rank is a weighted sum of per-field keyword occurence counts
        SPH_RANK_PROXIMITY = 4
        SPH_RANK_MATCHANY = 5
        SPH_RANK_FIELDMASK = 6
        SPH_RANK_SPH04 = 7
        SPH_RANK_EXPR = 8
        SPH_RANK_TOTAL = 9

        # known sort modes
        self.SPH_SORT_RELEVANCE = 0
        self.SPH_SORT_ATTR_DESC = 1
        self.SPH_SORT_ATTR_ASC = 2
        self.SPH_SORT_TIME_SEGMENTS = 3
        self.SPH_SORT_EXTENDED = 4
        self.SPH_SORT_EXPR = 5

        #lists to hold results
        self.resultIDs = []  #this contains the quoteID/RMIndex id's (depending on what's searched) in which the search string occurs
        self.search_results = []
        self.result_content = []
        self.excerpts = []
        #values
        self.num_docs_w_term = []
        self.total_occur_of_term = []

    def setPresetTables(self, which_preset):
        """
        @param which_preset one of the below valures
        iomAll Testimony_all table in iom_data ---all testimonials
        iomPatients Testimony_patients in iom_data ---all patient testimonials
        iomMain alias for iomAll (depreciated)
        iomQuotes alias for iomPatients (depreciated)
        onMain: [old, should avoid] NarrativeProject database's main table (containing all testimonials)
        """
        try:
            # Searching all testimony
            if which_preset == 'iomAll' or which_preset == 'iomMain':
                self.searchDB = 'iom_data'
                self.table_to_search = 'testimony'
                self.table_search_prim_key = 'quoteID'
                self.table_search_content = 'quoteText'
                self.table_to_insert_masked = 'masked_main'
                self.table_masked_prim_key = 'quoteID'
                self.table_masked_content = 'quoteText'
                self.excerpt_index = 'iom_data_idx'
                self.index_for_search = 'iom_data_idx'
                self.sortOn = 'quoteText'
                print 'Ready to search IOM testimony '

            #Searching patient testimony
            elif which_preset == 'iomPatients' or which_preset == 'onQuotes':
                self.searchDB = 'iom_data'
                self.table_to_search = 'testimony_patients'
                self.table_search_prim_key = 'quoteID'
                self.table_search_content = 'quoteText'
                self.table_to_insert_masked = 'masked_patients'
                self.table_masked_prim_key = 'quoteID'
                self.table_masked_content = 'quoteText'
                self.excerpt_index = 'test_patient_idx'
                self.index_for_search = 'test_patient_idx'
                self.sortOn = 'quoteText'
                print 'Ready to search IOM testimony_patients '
            #old database
            elif which_preset == 'onMain':
                self.searchDB = 'narrativeproject'
                self.table_to_search = 'main'
                self.table_search_prim_key = 'RM_INDEX'
                self.table_search_content = 'response'
                self.table_to_insert_masked = 'masked_main'
                self.table_masked_prim_key = 'RM_INDEX'
                self.table_masked_content = 'quoteText'
                self.excerpt_index = 'main_idx'
                self.index_for_search = 'main_idx'
                self.sortOn = 'RM_INDEX'
                print 'Ready to search narrative project main'

            try:
                #set sort mode
                self.SetSortMode(self.SPH_SORT_RELEVANCE, self.sortOn)
            #self.SetSortMode(self.SPH_SORT_ATTR_ASC, self.sortOn)
            except:
                print ('Error setting sort mode')
            try:
                #turn off ranking of results
                self.SetRankingMode(2)
            except:
                print('Error setting ranking mode')
            try:
                #set match mode (extended mode for phrase searches)
                #self.sphinx.SetMatchMode(SPH_MATCH_PHRASE)
                #sphinx.SetMatchMode(SPH_MATCH_BOOLEAN);
                self.SetMatchMode(self.SPH_MATCH_EXTENDED)
            except:
                print ('Error setting match mode')
        except:
            print 'error setting presets'
            self.sphinxErrorHandler()

    def setTables(self, array_with_tables):
        pass

        # foreach($array_with_tables as $k => $v){

    #		self.$k = $v;

    def sphinxErrorHandler(self):
        if self.search_results == 'FALSE':
            print "big problem: " + self.GetLastError();
        else:
            if self.GetLastWarning():
                print "WARNING: " + self.GetLastWarning() + "</br>"

    def search(self, search_string):
        try:
            # Stop if there is nothing to search
            if search_string == None:
                exit
            #Store string in property for use elsewhere
            self.search_string = search_string
            #run search
            self.search_results = self.Query(search_string, self.index_for_search);
            #error handler
            self.sphinxErrorHandler();
            #construct an array of quote/response id's
            [self.resultIDs.append(m['id']) for m in self.search_results['matches']]

        ##get information on the occurance of the string
        #self.num_docs_w_term = self.search_results['docs']
        #self.total_occur_of_term = self.search_results['hits']
        #for x in self.search_results:
        #for w in x['words']:
        #self.num_docs_w_term = w['docs']
        #self.total_occur_of_term = w['hits']
        except:
            print 'search failed'
            self.sphinxErrorHandler();

    def getContent(self):
        try:
            #self.sel = mysql_select_db(self.searchDB) or die(mysql_error());
            for idnum in self.resultIDs:
                self.query = "SELECT quoteID, quoteText FROM testimony_all WHERE quoteID = %s"
                #self.query = "SELECT * FROM %%s WHERE %%s = %idnum" % (self.table_to_search, self.table_search_prim_key)
                self.val = [idnum]
                self.returnAll()
                self.result_content.append(self.results[0])
        except:
            print 'Getting content failed'

    def buildExcerpts(self):
        """
        Note that exact phrase is set to true because I have a comprehensive list of variations.
        For projects which draw from other sources, this may need to be set to false
        """
        try:
            self.excerpt_options = {'exact_phrase': 'true',
                                    'query_mode': 'true',
                                    'before_match': '~',
                                    'after_match': '~',
                                    'around': 5000,
                                    'limit': 1000000}
            for r in self.result_content:
                ex = self.BuildExcerpts([r['quoteText']], self.excerpt_index, self.search_string, self.excerpt_options)
                d = {'quoteID': r['quoteID'], 'quoteText': ex[0]}
                self.excerpts.append(d)
        except:
            self.sphinxErrorHandler()
            print 'Failed to build excerpts'

    def mask_term(self, terms_to_mask):
        """
        Substitutes whitespace for the terms in term_to_masks.

        @type term_to_masks string
        @param term_to_masks A term or set of terms using sphinx extended search syntax
        @return: Returns a list of dictionaries with quoteID and quoteText keys
        @rtype: list
        """
        self.search(terms_to_mask)
        self.getContent()
        self.buildExcerpts()
        try:
            self.excerpts = [{'quoteID': e['quoteID'], 'quoteText': re.sub(r'~.+~', '', e['quoteText'])} for e in
                             self.excerpts]
        except:
            self.sphinxErrorHandler()
            print 'Failed to run re.sub on the excerpts and mask them'
        else:
            #Make a copy of the altered excerpts in case want to do something else with excerpts
            self.masked = self.excerpts
            print len(self.excerpts), ' records have been masked to remove ', terms_to_mask
            print 'The list is in self.masked; it has also been returned '
            return self.masked


    def insertExcerpts(self):
        #excerpt_options = array('exact_phrase' => 'true', 'before_match' => '<span class="mask"><strong>', 'after_match' => '</strong></span>', 'around' => 5000, 'limit' => 1000000);
        for recid, text in self.result_content:
            ex = self.BuildExcerpts(text, self.excerpt_index, self.search_string, self.excerpt_options)
            for k, v in ex:
                self.query = "INSERT INTO %%s  (%%s, %%s) VALUES(%s, %s)" % (
                self.table_to_insert_masked, self.table_masked_prim_key, self.table_masked_content)
                self.val = [k, v]
                self.executeQuery()

            #		/* This is a serious hack. The excerpt array doesn't hold the quoteID. So I'm relying on the
            #		array having the same order as the results array and stepping through it with the update query.
        i = 0;
        for idnum in self.resultIDs:
            self.query = "UPDATE quotes_masked SET quoteID = %s WHERE questionNumber = %s"
            self.val = [idnum, i]
            self.executeQuery
            i = i + 1