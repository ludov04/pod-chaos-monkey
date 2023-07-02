import random
from kubernetes import client, config
def delete_random_pod(namespace):
  config.load_config()
  v1 = client.CoreV1Api()

  # Get the list of pods in the specified namespace
  pods = v1.list_namespaced_pod(namespace).items

  if not pods:
    print(f"No pods found in the namespace '{namespace}'.")
    return

  # Select a random pod
  random_pod = random.choice(pods)

  # Delete the selected pod
  v1.delete_namespaced_pod(random_pod.metadata.name, namespace)

  print(f"Deleted pod: {random_pod.metadata.name}")
def main():
  parser = argparse.ArgumentParser(description='Pod Chaos Monkey')
  parser.add_argument('-n', '--namespace',
                      type=str, 
                      default=os.getenv('NAMESPACE', 'workloads'), 
                      help='Namespace in which delete a random pod (default is \'workloads\')'
                      )
  args = parser.parse_args()
  namespace = args.namespace

  delete_random_pod(namespace, exclude_label, dry_run)

if __name__ == '__main__':
  main()