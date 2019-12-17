import subprocess

from ansible_slurm import SINFO_COMMAND, SENTINEL


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
