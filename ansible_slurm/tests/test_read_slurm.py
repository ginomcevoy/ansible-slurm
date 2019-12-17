import unittest

from ansible_slurm import read_slurm

from . import resources as test_resources


class TestCreateHostDetails(unittest.TestCase):

    def setUp(self):
        resources = test_resources.TestResources()
        self.input_simple = resources.input_simple_text

    def test_first_node_present(self):
        host_details = read_slurm.sinfo_output_to_host_details(self.input_simple)
        self.assertTrue('pm-nod009' in host_details)

    def test_two_nodes_present(self):
        host_details = read_slurm.sinfo_output_to_host_details(self.input_simple)
        self.assertTrue('pm-nod009' in host_details and 'pm-nod010' in host_details)

    def test_state_present_without_star(self):
        host_details = read_slurm.sinfo_output_to_host_details(self.input_simple)

        self.assertTrue('state' in host_details['pm-nod009'])
        self.assertEqual(host_details['pm-nod009']['state'], 'mixed')

        self.assertTrue('state' in host_details['pm-nod052'])
        self.assertEqual(host_details['pm-nod052']['state'], 'idle')

    def test_partition_present(self):
        host_details = read_slurm.sinfo_output_to_host_details(self.input_simple)
        self.assertTrue('partition' in host_details['pm-nod009'])
        self.assertEqual(host_details['pm-nod009']['partition'], 'production')
