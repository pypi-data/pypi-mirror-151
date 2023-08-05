colors= ['Red', 'Blue', 'Green', 'Yellow']

states = ['Telangana', 'Karnataka', 'TamilNadu', 'Kerala']

neighbors = {}

neighbors['Telangana'] = ['Karnataka', 'TamilNadu']
neighbors['Karnataka'] = ['Telangana', 'TamilNadu', 'Kerala']
neighbors['TamilNadu'] = [' Telangana', 'Karnataka', 'Kerala']
neighbors['Kerala'] = ['Karnataka', 'Telangana']

colors_of_states = {}

def promising (state, color):

    for neighbor in neighbors.get(state): 
        color_of_neighbor = colors_of_states.get(neighbor) 
        if color_of_neighbor == color:
            return False
    return True

def get_color_for_state(state): 
    for color in colors:
        if promising (state, color):
            return color

def main():

    for state in states:
        colors_of_states[state] = get_color_for_state(state)
    print(colors_of_states)

if __name__ == '__main__':
    main()