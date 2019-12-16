# import pprint
import unittest
import yaml


simple_hosts = [
    'pm-nod009',
    'pm-nod010',
    'pm-nod052',
    'pm-nod146',
    'pm-nod147',
]


ALL = 'all'
CHILDREN = 'children'
HOSTS = 'hosts'
PARTITION = 'partition'
STATE = 'state'

ONLINE_STATE = 'online'
ONLINE_STATES = ['mixed', 'alloc', 'idle']

BUSY_STATE = 'busy'
BUSY_STATES = ['mixed', 'alloc']


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


class TestCreateYAML(unittest.TestCase):

    def setUp(self):
        self.expected_filename = 'expected-simple.yml'
        self.expected_dict = None
        with open(self.expected_filename, 'r') as ef:
            self.expected_dict = yaml.load(ef)
        self.maxDiff = None

    def test_hosts(self):
        created = create_ansible_inventory_dict(self.host_details_testing())
        expected = self.expected_dict
        self.assertEqual(created[ALL][HOSTS], expected[ALL][HOSTS])

    def test_production_present(self):
        created = create_ansible_inventory_dict(self.host_details_testing())

        self.assertTrue(CHILDREN in created[ALL].keys())
        self.assertTrue('production' in created[ALL][CHILDREN].keys())

    def test_production_contents(self):
        created = create_ansible_inventory_dict(self.host_details_testing())
        expected = self.expected_dict

        self.assertEqual(created[ALL][CHILDREN]['production'],
                         expected[ALL][CHILDREN]['production'])

    def test_complete_output(self):
        created = create_ansible_inventory_dict(self.host_details_testing())
        expected = self.expected_dict

        self.assertEqual(created, expected)

    def test_yaml_output(self):
        output_filename = 'output-simple.yml'
        output_dict = create_ansible_inventory_dict(self.host_details_testing())
        to_yaml(output_dict, output_filename)

        with open(output_filename, 'r') as of:
            actual_output = yaml.load(of)

        self.assertEqual(actual_output, self.expected_dict)

    def host_details_testing(self):
        example_host_details = {
            'pm-nod009': {'partition': 'production', 'state': 'mixed'},
            'pm-nod010': {'partition': 'production', 'state': 'mixed'},
            'pm-nod052': {'partition': 'production', 'state': 'idle'},
            'pm-nod146': {'partition': 'python3', 'state': 'mixed'},
            'pm-nod147': {'partition': 'production', 'state': 'down'},
        }
        return example_host_details


if __name__ == '__main__':
    unittest.main()
