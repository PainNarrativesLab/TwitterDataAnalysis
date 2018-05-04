"""
Created by adam on 4/24/18
"""
__author__ = 'adam'


if __name__ == '__main__':
    import os
    import sys
    import ipyparallel as ipp
    ROOT = os.getenv( "HOME" )
    BASE = '%s/Dropbox/PainNarrativesLab' % ROOT
    sys.path.append("%s/TwitterDataAnalysis" % ROOT)

    import environment
    # /Users/adam/Dropbox/PainNarrativesLab/TwitterDataAnalysis/
    import Servers.DatabaseServerGrumble as DSG
    from Executables import process_user_descriptions_into_words as Runner

    def run():
        print('running')
        return Runner.main()


    # from environment import *
    # /Users/adam/Dropbox/PainNarrativesLab/TwitterDataAnalysis/
    rc = ipp.Client()
    print(rc.ids)

    dview1 = rc[:]
    # dview2 = rc[:]
    dview1.block = False
    # dview2.block = False

    dview1.targets = [0]
    dview1.targets = [1]

    # dview.execute('run')
    dview1.apply(run)

    # dview1.apply_async(DSG.main())

    # dview2.apply_async(run)

    # dview.execute('DSG.main()')
    print('j')

    # with rc[:].sync_imports():
        # import Servers
        # from Servers import DatabaseServerGrumble as DSG
        # from Executables import process_user_descriptions_into_words as Runner

    #
    #
    # e1 = rc[0]
    # e2 = rc[1]
    # e1.block = False
    # e2.block = False
    # j = e1.apply_sync(os.getpid)
    # print(j)
    # a = e1.apply( Servers.DatabaseServerGrumble.main)
    # print(a.get())
    # # a.get()
    # b = e2.apply(Executables.process_user_descriptions_into_words.main)
    # b.get()

    # with rc[:].sync_imports():
    #     from Servers import DatabaseServerGrumble as DSG
    #     from Executables import process_user_descriptions_into_words as Runner

#
# # @lview.parallel()
# def start_db():
#     print('started')
#     DSG.main()
#
# # @lview.parallel()

    import numpy
    # print(rc.ids)
    #
    # e1 = rc[0]
    # e2 = rc[1]
    # e1.block = False
    # e2.block = False
    #
    # a = e1.apply(start_db)
    # a.get()
    # b = e2.apply(run)
    # b.get()
    # print(e2.id)
    # e1.apply(DSG.main())


