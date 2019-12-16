import subprocess
import unittest


SENTINEL = 'NODELIST'
PARTITION = 'partition'
STATE = 'state'

SINFO_COMMAND = 'sinfo -N']


def call_sinfo():
    return subprocess.check_output(SINFO_COMMAND, shell=True)


def sinfo_output_to_host_details(sinfo_output):
    '''
    Reads this string (output of sinfo -N)

    NODELIST   NODES   PARTITION STATE
    pm-nod009      1 production* mixed
    pm-nod010      1 production* mixed
    pm-nod052      1 production* idle*
    pm-nod146      1     python3 idle

    and creates the host details dictionary:

    example_host_details = {
        'pm-nod009': {'partition': 'production', 'state': 'mixed'},
        'pm-nod010': {'partition': 'production', 'state': 'mixed'},
        'pm-nod052': {'partition': 'production', 'state': 'idle'},
        'pm-nod146': {'partition': 'python3', 'state': 'mixed'},
        'pm-nod147': {'partition': 'production', 'state': 'down'},
    }

    Mind the '*'!
    '''

    host_details = {}

    for output_line in sinfo_output.split('\n'):
        if SENTINEL in output_line or not output_line:
            continue

        # get the node, partition and state
        (node_name, _, partition_unclean, state_unclean) = output_line.split()

        # clean partition and state (remove possible stars)
        partition = partition_unclean.replace('*', '')
        state = state_unclean.replace('*', '')

        host_details[node_name] = {'partition': partition, 'state': state}

    return host_details


class TestCreateHostDetails(unittest.TestCase):

    def setUp(self):
        self.input_simple = self.read_input_simple()

    def read_input_simple(self):
        input_simple = None
        with open('input-simple.txt', 'r') as f:
            input_simple = f.read()
        return input_simple

    def test_first_node_present(self):
        host_details = sinfo_output_to_host_details(self.read_input_simple())
        self.assertTrue('pm-nod009' in host_details)

    def test_two_nodes_present(self):
        host_details = sinfo_output_to_host_details(self.read_input_simple())
        self.assertTrue('pm-nod009' in host_details and 'pm-nod010' in host_details)

    def test_state_present_without_star(self):
        host_details = sinfo_output_to_host_details(self.read_input_simple())

        self.assertTrue('state' in host_details['pm-nod009'])
        self.assertEqual(host_details['pm-nod009']['state'], 'mixed')

        self.assertTrue('state' in host_details['pm-nod052'])
        self.assertEqual(host_details['pm-nod052']['state'], 'idle')

    def test_partition_present(self):
        host_details = sinfo_output_to_host_details(self.read_input_simple())
        self.assertTrue('partition' in host_details['pm-nod009'])
        self.assertEqual(host_details['pm-nod009']['partition'], 'production')


if __name__ == '__main__':
    unittest.main()
