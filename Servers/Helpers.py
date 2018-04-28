"""
Created by adam on 3/27/18
"""
from DataTools.DataStructures import make_tweet_result, make_user_result
from Servers.Errors import BadPayloadException

__author__ = 'adam'

import tornado


# logger = FileWritingLogger(name='Client Response ERROR')


def encode_payload( result ):
    return tornado.escape.json_encode( result )


def decode_payload( payload ):
    try:
        return tornado.escape.json_decode( payload )
    except Exception as e:
        raise BadPayloadException( e )


# def handle_response(response):
#     """Client side handler of the promise"""
#     if response.error:
#         # print(response.error)
#         # logger.log(response.error)
#     else:
#         # print('success')
#         pass


@tornado.gen.coroutine
def send_result( client, url, result ):
    """Uses the client to make a request"""
    payload = encode_payload( result )
    response = yield client.fetch( url, method="POST", body=payload )
    if response.error:
        print( response.error )
        return response.error

    return response.body
    # yield client.fetch(url, handle_response, method="POST", body=payload)


def make_result_from_decoded_payload( payload ):
    sentence_index = payload[ 0 ]
    word_index = payload[ 1 ]
    text = payload[ 2 ]
    objId = payload[ 3 ]
    resultType = payload[ 4 ]

    if resultType == 'tweet':
        return make_tweet_result( sentence_index, word_index, text, objId )

    if resultType == 'user':
        return make_user_result( sentence_index, word_index, text, objId )

    raise BadPayloadException

