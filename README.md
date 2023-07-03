# Pod Chaos Monkey

Pod Chaos Monkey is a simple Python program that randomly deletes a pod in a given namespace within a kubernetes cluster. This program is designed to help you simulate failures and test the resilience of your Kubernetes deployments.

## Prerequisites

- Python 3.x
- [Poetry](https://python-poetry.org/), to install follow [these steps](https://python-poetry.org/docs/#installation)

## Getting Started

To use Pod Chaos Monkey, follow these steps:

1. Activate the [poetry](https://python-poetry.org/) virtualenv:

   ```bash
   poetry shell
   ```
2. Install project dependencies

   ```bash
   poetry install
   ```

## Usage
Pod Chaos Monkey provides several options. Here are the available command-line arguments:

- -n, --namespace: Specifies the namespace in which to delete a random pod, optional, default is `workload`

```
python pod_chaos_monkey -n my-namespace
```

- -l, --label-selector: Restricts the selection of candidate pods using a label selector. Only pods matching the specified label selector will be eligible for deletion. Example:
```
python pod_chaos_monkey -l "app=frontend"
```

- --dry-run: Performs a dry run without deleting the pod. This can be useful for testing and validation purposes. Example:
```
python pod_chaos_monkey --dry-run
```

## Run the tests
Use the following command to run the tests
```
python -m unittest discover
```

### Examples
To delete a random pod in the my-namespace namespace, excluding pods with the app=frontend label, you can use the following command:
```
python pod_chaos_monkey -n my-namespace -l "app!=frontend"
```
## Usage with docker

You can either build your own image:
```
docker build -t pod-chaos-monkey .
```
Or use the one provided at `ghcr.io/ludov04/pod-chaos-monkey`
```
docker pull ghcr.io/ludov04/pod-chaos-monkey
```

If you are running this locally, make sure to mount your kubeconfig within the container:
```
docker run -v $HOME/.kube:/root/.kube ghcr.io/ludov04/pod-chaos-monkey -n workloads --dry-run
```

## Installation

The easiest way to use this in your cluster is to use the kustomize manifests:
```
kubectl apply -k https://github.com/ludov04/pod-chaos-monkey//deploy
```

Write a kustomization.yaml file if you need to customise the image used or some parameters
```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: pod-chaos-monkey
resources:
 - https://github.com/ludov04/pod-chaos-monkey//deploy

images:
  - name: pod-chaos-monkey
    newName: ghcr.io/ludov04/pod-chaos-monkey # Use your own image
    newTag: latest

patches:
  - patch: |
      apiVersion: batch/v1
      kind: CronJob
      metadata:
        name: pod-chaos-monkey
      spec:
        schedule: "* * * * *"
        jobTemplate:
          spec:
            template:
              spec:
                containers:
                - name: pod-chaos-monkey # Customize flags
                  args:
                  - -n
                  - workloads
                  - -l
                  - importance!=critical
                  - --dry-run
    target:
      name: pod-chaos-monkey
      kind: CronJob
```

Deploy with `kubectl apply -k .`

## Notes

- When deploying in a cluster, the python kubernetes sdk will automatically use the service account token mounted in the pod to authenticate to the kubernetes api. Make sure the service account have the correct permissions. See the role within `deploy/rbac.yaml` for an example.
- Use `Role` instead of `ClusterRole` if you'd prefered pod-chaos-monkey to be able to delete pods only within a selected namespace.
- The built image currently uses root as default user, consider using a different user.