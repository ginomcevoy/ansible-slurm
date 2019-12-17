# ansible-slurm
Create Ansible inventory based on Slurm sinfo.
This module does not create/configure a new Slurm cluster, instead it can be used to manage an existing one.

It will use a configured Slurm cluster (proper /etc/slurm/slurm.conf) to query sinfo and compute the state of the nodes, grouping the nodes according to their state. In addition to the default Slurm states (idle, alloc, mixed, down, etc), it creates the additional "online" group, comprising the nodes that are not down/drained.

To create the inventory, run:

PYTHONPATH=. python -m ansible_slurm.inventory output_file

or run the convenience script

bin/inventory output_file

The inventory file will be created at the specified output_file, or at "/tmp/slurm_inventory.yml" if not provided.
