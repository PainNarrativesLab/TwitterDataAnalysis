"""
Created by adam on 4/24/18
"""
import asyncio

__author__ = 'adam'

if __name__ == '__main__':
    import os
    import sys
    import aiohttp


    import ipyparallel as ipp
    ROOT = os.getenv( "HOME" )
    BASE = '%s/Dropbox/PainNarrativesLab' % ROOT
    sys.path.append( "%s/TwitterDataAnalysis" % ROOT )

    import environment
    # /Users/adam/Dropbox/PainNarrativesLab/TwitterDataAnalysis/
    import Servers.ServerControlCommander as Commander
    import Servers.DatabaseServerGrumble as DSG
    from Executables import process_user_descriptions_into_words2 as Runner

    def run1():

        loop = asyncio.get_event_loop()
        DSG.main()
        future = asyncio.Future()
        # wraps as a task (i.e., with a future)
        print( 'go' )
        asyncio.ensure_future( Runner.run( future ) )
        future.add_done_callback( Commander.flush_and_shutdown_server )
        result = loop.run_until_complete( future )
        print( future.result() )

        loop.close()

    run1()

    def chunked_http_client(num_chunks):
        semaphore = asyncio.Semaphore(num_chunks)

        @asyncio.coroutine
        def send(payload): #
            nonlocal semaphore
            with (yield from semaphore):
                response = yield from aiohttp.request('POST', data=payload)
                body = yield from response.content.read()
                yield from response.wait_for_close()
                return body
        return send
    #
    # def run_experiment(base_url, num_iter=500):
    #     http_client = chunked_http_client(100)
    #     tasks = [http_client(url) for url in urls] # responses_sum = 0
    #     for future in asyncio.as_completed(tasks): # data = yield from future
    #     responses_sum += len(data) return responses_sum



    # rc = ipp.Client()
    # print(rc.ids)
    #
    # dview1 = rc[:]
    # dview2 = rc[:]
    # dview1.block = False
    # dview2.block = False

    # dview1.apply_async(DSG.main())

    # dview2.apply_async(run)

    # DSG.main()

    # async def run0():
    #     semaphore = asyncio.Semaphore(1)
    #
    #     @asyncio.coroutine
    #     def start():
    #         DSG.main()
    #     await asyncio.ensure_future()


#
# dview1.targets = [0]
# dview1.targets = [1]
#
# # dview.execute('run')
# dview1.apply(run)

# dview1.apply_async(DSG.main())

# dview2.apply_async(run)

# dview.execute('DSG.main()')



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
