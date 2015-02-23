import json
import urllib.request
import urllib.parse
import urllib.error
from base64 import b16decode
from base64 import b16encode

BASE_URL = "http://pac.bouillaguet.info/TP2/"
ENCODING = 'utf-8'

class ServerError(Exception):
    def __init__(self, code=None, msg=None):
        self.code = code
        self.msg = None

class Server:
    def __init__(self, base_url):
        self.base = base_url

    def query(self, url, parameters=None ):
         url = self.base + url
         try:
            request = urllib.request.Request(url)
            data = None
            if parameters is not None:
                data = json.dumps(parameters).encode()
                request.add_header('Content-type', 'application/json')
            with urllib.request.urlopen(request, data) as connexion:
                result = connexion.read().decode()
                if connexion.info()['Content-Type'] == "application/json":
                    result = json.loads(result)
            return result
         except urllib.error.HTTPError as e:
             raise ServerError(e.code, e.read().decode()) from None

def xor(a, b):
  c = bytearray()
  for x,y in zip(a,b):
    c.append(x ^ y)
  return c

if __name__ == "__main__":
  server = Server(BASE_URL)
  seed = '1234'

  response = server.query('two-time-pad/question/sommerard/' + seed)
  print(response)

  response = server.query('two-time-pad/challenge/sommerard/' + seed)

  A = response['A']
  B = response['B']

  A_byte = b16decode(A, casefold=True)
  B_byte = b16decode(B, casefold=True)

  A_byte_xor_B_byte = xor(A_byte, B_byte)

  C = ""
  text = ""
  for i in A_byte_xor_B_byte:
    C = chr(i ^ ord('0'))
    if((C.isalpha() == False) and (C != "\n") and (C != " ")):
      C = chr(i ^ ord('1'))
    text += str(C)

  print(text)

  word2send = ""
  cpt_line = 0
  cpt_word = 0
  for i in text:
    if(i == "\n"):
      cpt_line += 1
      cpt_word = 0
    if(i == " "):
      cpt_word += 1
    if((cpt_line == 4) and (cpt_word == 3)):
      break
    if((cpt_line == 4) and (cpt_word == 2)):
      if(i != " "):
        word2send += i

  print("Word: ", word2send)

  parameters = { 'word': 'Parthénon' }
  response = server.query('two-time-pad/answer/sommerard/' + seed, parameters)
  print(response)
