from chess import Chess
from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from pawn import Pawn
from rook import Rook

a: set = {1,2,3,4,5}
b: set = set()

print(a&b)


a = Pawn('w')
b = Knight('w')
c = Bishop('w')
d = Rook('w')
e = Queen('w')
f = King('w')

print(str(a)[1:3])
print(str(b)[1:3])
print(str(c)[1:3])
print(str(d)[1:3])
print(str(e)[1:3])
print(str(f)[1:3])

print(type(a))
print(type(b))
print(type(c))
print(type(d))
print(type(e))
print(type(f))

