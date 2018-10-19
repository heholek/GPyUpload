import yaml
import sys

LAST = False

OPTIONS=[
    'Add a file        - (a)',
    'Remove a file     - (r)',
    'Save and continue - (s)'
]

item_list = []

def make_file():
    """
    Returns the file object
    """
    pass

def add_item_to_file():
    """
    Adds an object to main.yaml
    """
    item_group_name = input("What is the name of the item group? ")
    item_name = input("What is the item name? ")
    _id = input("What is the item id? ")
    _type = input("What is the item type? ")
    item_list.append(format_as_dict(item_group_name,
                                    item_name,
                                    _id,
                                    _type
                    ))
    print("Adding " + item_name + " to main.yaml...")

def format_as_dict(item_group_name, item_name, _id, _type):
    #Template
    #[item-group]:
    #  [item-name]:
    #    id: [item-id]
    #    type: [item-type]
    return {
                    item_group_name:
                    {
                        item_name:
                        {
                            'id': _id,
                            'type': _type,
                        }
                    }
    }

def remove_item_from_file():
    """
    Removes an object from main.yaml
    """
    pass

def prompt():
    print('''Setting up configurations...''')

def response(inpt):
    finished = False
    inpt_accepted = False
    if inpt == 'a':
        print("Adding an item...")
        add_item_to_file()
        finished = False
        inpt_accepted = True
    elif inpt == 'r':
        print("Removing an item...")
        finished = False
        inpt_accepted = True
    elif inpt == 's':
        print("Writing to file...")
        with open('src/config/main.yaml', 'a+') as config_file:
            for item in item_list:
                yaml.dump(item, config_file, default_flow_style=False)
        finished = True
        inpt_accepted = True
    return finished, inpt_accepted
