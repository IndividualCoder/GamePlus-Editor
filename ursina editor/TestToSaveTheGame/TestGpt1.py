from ursina import *
import pickle

game_data = {
    'objects': [],
    'player_position': (0, 0),
    'enemy_positions': [],
    'score': 0
}

def save_game():
    filename = 'game_data.pickle'
    with open(filename, 'wb') as file:
        pickle.dump(game_data, file)
    print(f"Game saved as '{filename}'.")

def export_game():
    filename = 'game_script.py'
    with open(filename, 'w') as file:
        file.write('''import ursina

game_data = {}
app = ursina.Ursina()

def create_object():
    obj = ursina.Entity(model='cube', color=ursina.color.random_color(), position=(0, 0, 0))
    game_data['objects'].append({
        'model': 'cube',
        'color': obj.color,
        'position': obj.position
    })

camera = ursina.EditorCamera()

def update():
    if ursina.held_keys['control'] and ursina.mouse.left:
        create_object()

app.run()'''.format(repr(game_data)))

    print(f"Game exported as '{filename}'.")

def create_object():
    obj = ursina.Entity(model='cube', color=ursina.color.random_color(), position=(0, 0, 0))
    game_data['objects'].append({
        'model': 'cube',
        'color': obj.color,
        'position': obj.position
    })

app = Ursina()

def input(key):
    if key == 's':
        save_game()
    elif key == 'e':
        export_game()

def update():
    if held_keys['control'] and mouse.left:
        create_object()

app.run()
