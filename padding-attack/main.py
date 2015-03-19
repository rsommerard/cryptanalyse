import client
import helpers
import random

SEED = '14'

BASE_URL = 'http://pac.bouillaguet.info/TP2/'
CHALLENGE = 'padding-attack/challenge/sommerard/' + SEED
ORACLE = '/padding-attack/oracle/sommerard'

STEP_1_VALIDATION = '/padding-attack/last-byte/sommerard/' + SEED
STEP_2_VALIDATION = '/padding-attack/last-block/sommerard/' + SEED
STEP_3_VALIDATION = '/padding-attack/validation/sommerard/' + SEED

def get_oracle_response(ciphertext, iv):
    parameters = { "ciphertext": ciphertext, 'IV': iv }
    response = server.query(ORACLE, parameters)
    return response['status']

def find_block(c1, c2):
    c1b = helpers.Block().random()
    i2 = helpers.Block()
    p2b = helpers.Block()
    p2 = helpers.Block()

    tab_values = [i for i in range(256)]

    for index_byte in range(15, -1, -1):
        padding = (16 - index_byte)

        for i in range(15, index_byte - 1, -1):
            p2b[i] = padding
            c1b[i] = p2b[i] ^ i2[i]

        #print('p2b:', p2b)
        #print('c1b:', c1b)

        #print('> Searching for byte index', index_byte)

        random.shuffle(tab_values)
        tested_values = 0
        for i in tab_values:
            tested_values += 1
            print('\r<' + str(tested_values) + '>\t', end='')
            c1b[index_byte] = i
            #print(c1b)
            if get_oracle_response(c1b.hex() + c2.hex(), iv.hex()) == 'OK':
                break

        #print('>> Byte found:', hex(c1b[index_byte]))

        i2[index_byte] = c1b[index_byte] ^ p2b[index_byte]
        #print(hex(i2[index_byte]) + ' = ' + hex(c1b[index_byte]) + ' ^ ' + hex(p2b[index_byte]))

        p2[index_byte] = c1[index_byte] ^ i2[index_byte]
        #print(hex(p2[index_byte]) + ' = ' + hex(c1[index_byte]) + ' ^ ' + hex(i2[index_byte]))

        print('<' + p2.hex() + '>')

        #byte = hex(p2[index_byte])[2:].upper()

        #if(len(byte) != 2):
        #    byte = '0' + byte

        #if(index_byte == 15):
        #    parameters = { 'value': byte }
        #    response = server.query('/padding-attack/last-byte/sommerard/' + SEED + '/1', parameters)
        #    print(response)
        #if(index_byte == 14):
        #    parameters = { 'value': byte }
        #    response = server.query('/padding-attack/last-byte/sommerard/' + SEED + '/2', parameters)
        #    print(response)

    return p2

if __name__ == '__main__':
    global server

    server = client.Server(BASE_URL)

    response = server.query(CHALLENGE)

    iv = helpers.Block(response['IV'])
    blocks = helpers.Message(response['ciphertext'])

    ciphertext_dec = ''

    nb_block = 13
    for i in range(-1, -(len(blocks) + 1), -1):
        if(i == (-(len(blocks) + 1) + 1)):
            block = find_block(iv, blocks[i])
        else:
            block = find_block(blocks[i-1], blocks[i])

        print('Block ' + str(nb_block) + ': ' + block.hex())

        ciphertext_dec = block.hex() + ciphertext_dec

        print('ciphertext_dec: ' + ciphertext_dec)

        nb_block -= 1

    # SEED 14 block 13 = 62653766306235630808080808080808
    # SEED 14 block 12 = 63313637303433306466613364623663
    # SEED 14 block 11 = 6F6F0A6D61633A203435373237356333
    # SEED 14 block 10 = 756E6B3A20666F6F6F6F6F6F6F6F6F6F
    # SEED 14 block 9 = 0A70736575646F2D72616E646F6D206A
    # SEED 14 block 8 = 7333727633720A0A736565643A203134
    # SEED 14 block 7 = 2D2D2D2D2D2D2D0A5468652050344320
    # SEED 14 block 6 = 206C652070616464696E672E0A2D2D2D
    # SEED 14 block 5 = 6F64652065740A6427656E6C65766572
    # SEED 14 block 4 = 657222206365636920656E20756E6963
    # SEED 14 block 3 = 6520706173206465202264C3A9636F64
    # SEED 14 block 2 = C3A9757373692021204E276F75626C69
    # SEED 14 block 1 = 0A0A427261766F2C2074752061732072
    # SEED 14 block 0 = 53616C757420736F6D6D65726172642C

    print('Final ciphertext_dec: ' + ciphertext_dec)

    parameters = { 'plaintext': ciphertext_dec }
    response = server.query(STEP_3_VALIDATION, parameters)
    print(response)
