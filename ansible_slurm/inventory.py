import sys

from ansible_slurm import read_slurm, create_yaml, DEFAULT_OUTPUT


def main(output_file):
    print('Using output file %s' % output_file)
    sinfo_output = read_slurm.call_sinfo()
    host_details = read_slurm.sinfo_output_to_host_details(sinfo_output)
    inventory_dict = create_yaml.create_ansible_inventory_dict(host_details)
    create_yaml.to_yaml(inventory_dict, output_file)
    print('Created inventory at %s' % output_file)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = DEFAULT_OUTPUT
    main(output_file)
