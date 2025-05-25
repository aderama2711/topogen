# topogen
Topology Generator for mininet and mini-ndn

## Prerequisite
```shell
pip install -r requirements.txt
```

## Usage
```shell
usage: gen.py [-h] [--nodes NODES] [--links LINKS] [--min_hop MIN_HOP] [--delay DELAY] [--std_dev STD_DEV]

Generate random network topology

options:
  -h, --help         show this help message and exit
  --nodes NODES      Number of nodes
  --links LINKS      Average number of links per node
  --min_hop MIN_HOP  Minimum hop count for non-direct connections (to determine node as producer an consumer)
  --delay DELAY      Mean delay in ms for each link
  --std_dev STD_DEV  Standard deviation for delay and link generation
```

## Results
![alt text](https://github.com/aderama2711/topogen/blob/main/topology.jpg)
topology.txt is configuration for mininet or mini-ndn
and prod-cons.txt is list of possible pair for producer and consumer placement