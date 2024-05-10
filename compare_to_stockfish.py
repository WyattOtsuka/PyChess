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
my_output_map = {}

for my_string in my_output_array:
    if my_string != '':
        split_string = my_string.split("  --- ")[0]
        move_count_array = split_string.split(": ")
        my_output_map[move_count_array[0]] = move_count_array[1]

stockfish_output_arary = stockfish_output.splitlines()
stockfish_output_map = {}
for stockfish_string in stockfish_output_arary:
    if stockfish_string != '':
        move_count_array = stockfish_string.split(": ")
        stockfish_output_map[move_count_array[0]] = move_count_array[1]

key_set = set()

key_set.update(my_output_map.keys())
key_set.update(stockfish_output_map.keys())

for key in key_set:
    my_ouput = ""
    stockfish_output = ""
    if key in my_output_map:
        my_ouput = my_output_map[key]

    if key in stockfish_output_map:
        stockfish_output = stockfish_output_map[key]

    if my_ouput != stockfish_output:
        print(f"{key}: {my_ouput} -> {stockfish_output}")
