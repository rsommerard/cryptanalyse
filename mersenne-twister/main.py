import client
from marsenne import MersenneTwister

BASE_URL = "http://pac.bouillaguet.info/TP2/"

def reverse_number(nb):
  # reverse y ^= y >> 18
  last14 = nb >> 18
  part1 = nb ^ last14

  # reverse y ^= (y << 15) & 4022730752
  first17 = part1 << 15
  part2 = part1 ^ (first17 & 4022730752)

  # reverse y ^= (y << 7) & 2636928640
  part3a = part2 << 7
  part3b = part2 ^ (part3a & 2636928640)
  part3c = part3b << 7
  part3d = part2 ^ (part3c & 2636928640)
  part3e = part3d << 7
  part3f = part2 ^ (part3e & 2636928640)
  part3g = part3f << 7
  part3h = part2 ^ (part3g & 2636928640)
  part3i = part3h << 7
  part3 = part2 ^ (part3i & 2636928640)

  # reverse y ^= y >> 11
  part4a = part3 >> 11
  part4b = part3 ^ part4a
  part4c = part4b >> 11;
  part4 = part3 ^ part4c;

  return part4

if __name__ == "__main__":
  server = client.Server(BASE_URL)

  response = server.query('mersenne-twister/challenge/sommerard')
  challenge = response['challenge']

  mt = MersenneTwister()

  for i in range(624):
    mt.MT[i] = reverse_number(challenge[i])

  for i in range(1000):
    mt.rand()

  generation_1001 = mt.rand()
  print('1001ème génération:', generation_1001)

  response = server.query('mersenne-twister/prediction/sommerard/' + str(generation_1001))
  print(response)
