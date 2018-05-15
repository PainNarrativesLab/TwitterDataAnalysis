"""
Created by adam on 5/14/18
"""
import asyncio

__author__ = 'adam'


from Servers.ClientSide import Client


def flush_and_shutdown_server(future=None):
    c = Client()
    # Each of the listening request handlers needs its queue flushed
    print('starting queue flush')
    c.send_flush_command()


    # c.send_shutdown_command()
    # print('sending shutdown')

    if future is not None and not future.done():
        future.set_result('done flushing')

if __name__ == '__main__':
    flush_and_shutdown_server()