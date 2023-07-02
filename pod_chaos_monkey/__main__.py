import argparse
import os
from namespaced_delete import delete_random_pod

parser = argparse.ArgumentParser(description='Pod Chaos Monkey')
parser.add_argument('-n', '--namespace',
                      type=str,
                      default=os.getenv('NAMESPACE', 'workloads'),
                      help='Namespace in which to delete a random pod (default is \'workloads\')')
parser.add_argument('-l', '--label-selector', type=str, default=None,
                      help='Restrict candidate pods using a label selector')
parser.add_argument('--dry-run', action='store_true', default=False, help='Perform a dry run without deleting the pod')

args = parser.parse_args()
namespace = args.namespace
label_selector = args.label_selector
dry_run = args.dry_run

delete_random_pod(namespace, label_selector, dry_run)
