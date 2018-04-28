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

    # from environment import *
    # /Users/adam/Dropbox/PainNarrativesLab/TwitterDataAnalysis/
    rc = ipp.Client()

    print(rc.ids)
    with rc[:].sync_imports():
        import Servers
        from Servers import DatabaseServerGrumble as DSG
        import Executables
        from Executables import process_user_descriptions_into_words as Runner

    j = rc[:].apply_sync(DSG.main)

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
# def run():
#     print('running')
#     return Runner.main()

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


