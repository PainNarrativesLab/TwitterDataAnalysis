"""
Created by adam on 5/14/18
"""
import asyncio

__author__ = 'adam'


from Servers.ClientSide import Client


def flush_and_shutdown_server(future=None):
    c = Client()
    # Each of the listening request handlers needs its queue flushed
    # loop = asyncio.get_event_loop()
    print('starting queue flush')
    c.send_flush_command()
    c.send_shutdown_command()
    # # f = asyncio.ensure_future(c.async_send_flush_command())
    # f.add_done_callback(c.send_shutdown_command)
    # loop.run_until_complete(f)
    print('sending shutdown')

    if future is not None and not future.done():
        future.set_result('done flushing')
    # loop.close()

if __name__ == '__main__':
    flush_and_shutdown_server()