import random
from kubernetes import client, config
def delete_random_pod(namespace):
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
