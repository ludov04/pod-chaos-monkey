import argparse
import os
from namespaced_delete import delete_random_pod

parser = argparse.ArgumentParser(description='Pod Chaos Monkey')
parser.add_argument('-n', '--namespace',
                      type=str,
                      default=os.getenv('NAMESPACE', 'workloads'),
                      help='Namespace in which delete a random pod (default is \'workloads\')')
parser.add_argument('--exclude-label', type=str, default=None,
                      help='Exclude pods with the specified label')
parser.add_argument('--dry-run', type=bool, default=False, help='Perform a dry run without deleting the pod')

args = parser.parse_args()
namespace = args.namespace
exclude_label = args.exclude_label
dry_run = args.dry_run

delete_random_pod(namespace, exclude_label, dry_run)
