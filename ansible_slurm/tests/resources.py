import os
import yaml

from ansible_slurm import tests


class TestResources(object):

    def __init__(self):
        # full path of the test module
        test_file_location = tests.__file__

        test_dir = os.path.dirname(test_file_location)
        self.resources_directory = os.path.join(test_dir, tests.RESOURCES_DIR)

    @property
    def resources_dir(self):
        return self.resources_directory

    @property
    def input_simple_text(self):
        input_simple = None
        input_simple_file = os.path.join(self.resources_dir, 'input-simple.txt')
        with open(input_simple_file, 'r') as f:
            input_simple = f.read()
        return input_simple

    @property
    def expected_simple(self):
        expected_filename = os.path.join(self.resources_dir, 'expected-simple.yml')
        self.expected_dict = None
        with open(expected_filename, 'r') as ef:
            expected_dict = yaml.load(ef)
        return expected_dict


if __name__ == '__main__':
    tr = TestResources()
    print(tr.resources_dir)
    print(tr.input_simple_text)
    print(tr.expected_simple)
