import yaml


from ansible_slurm import ALL, CHILDREN, HOSTS, PARTITION, STATE, ONLINE_STATES, ONLINE_STATE


simple_hosts = [
    'pm-nod009',
    'pm-nod010',
    'pm-nod052',
    'pm-nod146',
    'pm-nod147',
]


def create_ansible_inventory_dict(host_details):
    '''
    Function that takes in host details dictionary with this syntax:

    example_host_details = {
        'pm-nod009': {'partition': 'production', 'state': 'mixed'},
        'pm-nod010': {'partition': 'production', 'state': 'mixed'},
        'pm-nod052': {'partition': 'production', 'state': 'idle'},
        'pm-nod146': {'partition': 'python3', 'state': 'mixed'},
        'pm-nod147': {'partition': 'production', 'state': 'down'},
    }

    and creates an Ansible inventory:

    ---

    all:
      hosts:
        pm-nod009:
        pm-nod010:
        pm-nod052:
        pm-nod146:
        pm-nod147:
      children:
        production:
          children:
            idle:
              hosts:
                pm-nod052:
            mixed:
              hosts:
                pm-nod009:
                pm-nod010:
            down:
              hosts:
                pm-nod147:
            online:
              hosts:
                pm-nod009:
                pm-nod010:
                pm-nod052:
        python3:
          children:
            mixed:
              hosts:
                pm-nod146:
            online:
              hosts:
                pm-nod146:
    '''
    d = {ALL: {HOSTS: {}, CHILDREN: {}}}
    children = d[ALL][CHILDREN]

    for node_name, node_dict in host_details.items():

        # add node to hosts
        d[ALL][HOSTS][node_name] = None

        # check for new partitions
        partition = node_dict[PARTITION]
        add_partition_if_needed(children, partition)

        # add node to correct state within partition
        state = node_dict[STATE]
        add_state_to_partition_if_needed(children, partition, state)
        add_node_to_state(children, partition, state, node_name)

        # if node is in one of 'online' states, add node to online group
        if state in ONLINE_STATES:
            add_state_to_partition_if_needed(children, partition, ONLINE_STATE)
            add_node_to_state(children, partition, ONLINE_STATE, node_name)

    return d


def add_partition_if_needed(children, partition):
    if partition not in children:
        children[partition] = {CHILDREN: {}}


def add_state_to_partition_if_needed(children, partition, state):
    '''
    Check if state is in partition. If not, add it.
    '''
    if state not in children[partition][CHILDREN]:
        # new state needed
        children[partition][CHILDREN][state] = {HOSTS: {}}


def add_node_to_state(children, partition, state, node_name):
    children[partition][CHILDREN][state][HOSTS][node_name] = None


def to_yaml(output_dict, filename):
    with open(filename, 'w') as file:
        # https://stackoverflow.com/a/47940875
        yaml.dump(output_dict, file, default_flow_style=False)

    return filename
