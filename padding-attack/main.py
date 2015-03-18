import client
import helpers

SEED = '0'

BASE_URL = 'http://pac.bouillaguet.info/TP2/'
CHALLENGE = 'padding-attack/challenge/sommerard/' + SEED
ORACLE = '/padding-attack/oracle/sommerard'

STEP_1_VALIDATION = '/padding-attack/last-byte/sommerard/' + SEED

#
# SEED = 0
#
# IV = 6721419f58d3664f6e4df5b205646e7f
#
# ciphertext = 23FD388483AF17FB54CB62F20EC13F1E5D5A7CDF572349D6605EA1D58B887E0392B7EEC13D6ADADB0B740FD149059A37B72C88E3FCE8E4407F4A093AE3D1A2EBD3BD9B84C4BB14AC8464447C8B51791B2D7C4595050D1B475FD7B6A9C568BC116B03481C09045B771D04FFA97E9D3BB7F6AC11011FCFF5F06E5498A4634A2006978D3A539D5BDD54CE0118466C8D980E8E8952BA3AE3EE5A74473D1CAF8EF1B5EB7E8A0B5AD60A380F80F4AA4573F907C98B703B9EECC4DC8DF7BAFCD015BB381F020A67F7906B44518AB6DEAE4A4EBA
#

def get_oracle_response(ciphertext, iv):
    parameters = { "ciphertext": ciphertext, 'IV': iv }
    return server.query(ORACLE, parameters)


def find_last_byte(block, before_block, iv):
    i = 0

    r = helpers.Block()

    for i in range(59, 256):
        r[15] = i
        print('i:', i, ' | ', r.hex() + block.hex())
        response = get_oracle_response(r.hex() + block.hex(), iv.hex())
        if response['status'] == 'OK':
            break

    is = helpers.Block()
    is = r ^ block
	last_byte = is ^ 1

    print(last_byte)

    return last_byte

if __name__ == '__main__':
    global server

    server = client.Server(BASE_URL)

    #response = server.query(CHALLENGE)
    response = { 'IV': '6721419f58d3664f6e4df5b205646e7f', 'ciphertext': '23FD388483AF17FB54CB62F20EC13F1E5D5A7CDF572349D6605EA1D58B887E0392B7EEC13D6ADADB0B740FD149059A37B72C88E3FCE8E4407F4A093AE3D1A2EBD3BD9B84C4BB14AC8464447C8B51791B2D7C4595050D1B475FD7B6A9C568BC116B03481C09045B771D04FFA97E9D3BB7F6AC11011FCFF5F06E5498A4634A2006978D3A539D5BDD54CE0118466C8D980E8E8952BA3AE3EE5A74473D1CAF8EF1B5EB7E8A0B5AD60A380F80F4AA4573F907C98B703B9EECC4DC8DF7BAFCD015BB381F020A67F7906B44518AB6DEAE4A4EBA' }

    iv = helpers.Block(response['IV'])
    blocks = helpers.Message(response['ciphertext'])

    find_last_byte(blocks[-1], blocks[-2], iv)
