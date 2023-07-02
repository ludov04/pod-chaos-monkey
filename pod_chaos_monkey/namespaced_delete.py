import random
from kubernetes import client, config

def delete_random_pod(namespace, label_selector=None, dry_run=False):
  config.load_config()
  v1 = client.CoreV1Api()

  # Get the list of pods in the specified namespace
  pods = v1.list_namespaced_pod(namespace, label_selector=label_selector).items
  print(f"{len(pods)} pod(s) found in namespace {namespace}. Using {label_selector} selector")

  if not pods:
    print(f"No pods found in the namespace '{namespace}'.")
    return

  # Select a random pod
  random_pod = random.choice(pods)

  print(f"Selected pod '{random_pod.metadata.name}' for deletion")
  if not dry_run:
    try:
      # Delete the pod
      v1.delete_namespaced_pod(random_pod.metadata.name, namespace)
      print(f"Pod '{random_pod.metadata.name}' in namespace '{namespace}' deleted successfully.")
    except client.rest.ApiException as e:
      print(f"Error deleting pod: {e.reason}")
  else:
    print(f"dry_run flag set, would have deleted '{random_pod.metadata.name}' in namespace '{namespace}'")
