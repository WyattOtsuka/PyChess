my_output = '''
b8a6: 399
b8c6: 439
g8f6: 439
g8h6: 399
a7a6: 379
a7a5: 419
b7b6: 419
b7b5: 420
c7c6: 419
c7c5: 440
d7d6: 538
d7d5: 559
e7e6: 597
e7e5: 599
f7f6: 380
f7f5: 399
g7g6: 419
g7g5: 420
h7h6: 380
h7h5: 420
'''

stockfish_output = '''
a7a6: 379
b7b6: 419
c7c6: 419
d7d6: 538
e7e6: 597
f7f6: 379
g7g6: 419
h7h6: 380
a7a5: 419
b7b5: 420
c7c5: 440
d7d5: 559
e7e5: 599
f7f5: 398
g7g5: 420
h7h5: 420
b8a6: 399
b8c6: 439
g8f6: 439
g8h6: 399
'''

my_output_array = my_output.splitlines()
stockfish_output_arary = stockfish_output.splitlines()

my_output_array.sort()
stockfish_output_arary.sort()

for my_move, stockfish_move in zip(my_output_array, stockfish_output_arary):
    if my_move != stockfish_move:
        print(f"{my_move} -> {stockfish_move}")

