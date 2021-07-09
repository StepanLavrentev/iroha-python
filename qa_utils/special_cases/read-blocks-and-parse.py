from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
from collections import defaultdict
import datetime

IROHA_HOST_ADDR = '127.0.0.1'
IROHA_PORT = '3456'
ADMIN_ACCOUNT_ID = 'alice@test'
ADMIN_PRIVATE_KEY = '4985f7499aa8e9841100fe41499a4e8f44c501b20afcf29be62ef5053ed89a1c'

'''
 BLOCK_STORE_HEIGHT - the first block to begin parse
 BLOCK_STORE_LOW - end of the block store parse.
 diference beetween BLOCK_STORE_HEIGHT and BLOCK_STORE_LOW shouldn't be more
 speed of parsing is ~5 block/sec
'''
BLOCK_STORE_HEIGHT = 630
BLOCK_STORE_LOW = 0

iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))


def get_block():

    block_store_height = BLOCK_STORE_HEIGHT
    command_list = []

    while block_store_height > BLOCK_STORE_LOW:
        query = iroha.query('GetBlock', height=block_store_height)
        IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

        response = net.send_query(query)
        data = response.block_response.block.block_v1.payload.transactions
        for transaction in data:
            for command in transaction.payload.reduced_payload.commands:
                field_list = command.ListFields()
                command_list.append(field_list[0][0].camelcase_name)
        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Block %s was parsed' % block_store_height)
        block_store_height-=1


    compare_dict = defaultdict(list)

    for i in command_list:
        compare_dict[i].append(i)

    for key in compare_dict:
        print("Iroha command: %s, count: %s" % (key, len(compare_dict[key])))


get_block()