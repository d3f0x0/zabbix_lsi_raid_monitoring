import argparse
from raid_zabbix import discover_controller, discover_physical_disk, info_physical_disk, status_raid

parser = argparse.ArgumentParser(description='process some integers')
parser.add_argument('--discover_controller', nargs='*', metavar='', help='Discover raid controller')
parser.add_argument('--discover_physical_disk', nargs=1, metavar='',
                    help='discover physical disk, input: index raid controller')
parser.add_argument('--info_physical_disk', nargs=3, metavar='',
                    help='return status disk, input:index_raid_controller,enclosure,slot')
parser.add_argument('--status_raid', nargs=1, metavar='', help='return raid status')
args = parser.parse_args()

if args.discover_controller:
    print(discover_controller())
elif args.discover_physical_disk:
    print(discover_physical_disk(args.discover_physical_disk[0]))
elif args.info_physical_disk:
    print(info_physical_disk(args.info_physical_disk[0], args.info_physical_disk[1], args.info_physical_disk[2]))
elif args.status_raid:
    print(status_raid(args.status_raid[0]))
