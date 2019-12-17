import unittest
import yaml

from ansible_slurm import create_yaml
from ansible_slurm import ALL, CHILDREN, HOSTS

from . import resources as test_resources


class TestCreateYAML(unittest.TestCase):

    def setUp(self):
        resources = test_resources.TestResources()
        self.expected_simple = resources.expected_simple
        self.maxDiff = None

    def test_hosts(self):
        created = create_yaml.create_ansible_inventory_dict(self.host_details_testing())
        expected = self.expected_simple
        self.assertEqual(created[ALL][HOSTS], expected[ALL][HOSTS])

    def test_production_present(self):
        created = create_yaml.create_ansible_inventory_dict(self.host_details_testing())

        self.assertTrue(CHILDREN in created[ALL].keys())
        self.assertTrue('production' in created[ALL][CHILDREN].keys())

    def test_production_contents(self):
        created = create_yaml.create_ansible_inventory_dict(self.host_details_testing())
        expected = self.expected_simple

        self.assertEqual(created[ALL][CHILDREN]['production'],
                         expected[ALL][CHILDREN]['production'])

    def test_complete_output(self):
        created = create_yaml.create_ansible_inventory_dict(self.host_details_testing())
        expected = self.expected_simple

        self.assertEqual(created, expected)

    def test_yaml_output(self):
        output_filename = '/tmp/ansible_slurm_output-simple.yml'
        output_dict = create_yaml.create_ansible_inventory_dict(self.host_details_testing())
        create_yaml.to_yaml(output_dict, output_filename)

        with open(output_filename, 'r') as of:
            actual_output = yaml.load(of)

        self.assertEqual(actual_output, self.expected_simple)

    def host_details_testing(self):
        example_host_details = {
            'pm-nod009': {'partition': 'production', 'state': 'mixed'},
            'pm-nod010': {'partition': 'production', 'state': 'mixed'},
            'pm-nod052': {'partition': 'production', 'state': 'idle'},
            'pm-nod146': {'partition': 'python3', 'state': 'mixed'},
            'pm-nod147': {'partition': 'production', 'state': 'down'},
        }
        return example_host_details
