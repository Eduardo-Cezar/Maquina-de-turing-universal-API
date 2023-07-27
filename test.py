import json

json_data = '''
{
    "requests": [
        {
            "input": "00000000111111111",
            "states": ["q0", "q1", "q2", "q3", "q4"],
            "input_symbols": ["0", "1"],
            "tape_symbols": ["0", "1", "x", "y", "."],
            "initial_state": "q0",
            "blank_symbol": ".",
            "final_states": ["q4"],
            "transitions": {
                "q0": {
                    "0": ["q1", "x", "R"],
                    "y": ["q3", "y", "R"]
                },
                "q1": {
                    "0": ["q1", "0", "R"],
                    "1": ["q2", "y", "L"],
                    "y": ["q1", "y", "R"]
                },
                "q2": {
                    "0": ["q2", "0", "L"],
                    "x": ["q0", "x", "R"],
                    "y": ["q2", "y", "L"]
                },
                "q3": {
                    "y": ["q3", "y", "R"],
                    ".": ["q4", ".", "R"]
                }
            }
        },
        {
            "input": "001111111111",
            "states": ["q0", "q1", "q2", "q3", "q4"],
            "input_symbols": ["0", "1"],
            "tape_symbols": ["0", "1", "x", "y", "."],
            "initial_state": "q0",
            "blank_symbol": ".",
            "final_states": ["q4"],
            "transitions": {
                "q0": {
                    "0": ["q1", "x", "R"],
                    "y": ["q3", "y", "R"]
                },
                "q1": {
                    "0": ["q1", "0", "R"],
                    "1": ["q2", "y", "L"],
                    "y": ["q1", "y", "R"]
                },
                "q2": {
                    "0": ["q2", "0", "L"],
                    "x": ["q0", "x", "R"],
                    "y": ["q2", "y", "L"]
                },
                "q3": {
                    "y": ["q3", "y", "R"],
                    ".": ["q4", ".", "R"]
                }
            }
        }
    ]
}
'''

# Carregar o JSON em uma estrutura de dados Python
data = json.loads(json_data)

# Acessar a lista de solicitações
requests_list = data["requests"]

# Agora 'requests_list' é uma lista contendo os objetos de cada solicitação
# Você pode iterar sobre ela ou acessar as solicitações individualmente

# Por exemplo, para acessar a primeira solicitação:
#first_request = requests_list[0]
#print(first_request)

# Ou para iterar sobre todas as solicitações:
print (type(json_data))
for request in requests_list:
    print(request)
    print("\n---------------------------------------------------------------------------\n")