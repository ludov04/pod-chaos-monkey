import unittest
from unittest.mock import patch, MagicMock
from pod_chaos_monkey.namespaced_delete import delete_random_pod

class TestPodChaosMonkey(unittest.TestCase):
  namespace = "mock-namespace"

  @patch('pod_chaos_monkey.namespaced_delete.client.CoreV1Api')
  @patch('pod_chaos_monkey.namespaced_delete.config.load_config')
  def test_delete_random_pod(self, mock_load_config, mock_core_v1_api):
    # Mock a pod
    mock_pod = MagicMock()
    mock_pod.metadata.name = "mock-pod"
    # Mock the returned list of pods
    mock_core_v1_api.return_value.list_namespaced_pod.return_value.items = [mock_pod]

    delete_random_pod(self.namespace)
    mock_load_config.assert_called()
    # Verify that the delete_namespaced_pod method is called
    mock_core_v1_api.return_value.delete_namespaced_pod.assert_called_with("mock-pod", self.namespace)

  @patch('pod_chaos_monkey.namespaced_delete.client.CoreV1Api')
  @patch('pod_chaos_monkey.namespaced_delete.config.load_config')
  def test_delete_random_pod_empty_list(self, mock_load_config, mock_core_v1_api):
    # Mock the returned list of pods (empty)
    mock_core_v1_api.return_value.list_namespaced_pod.return_value.items = []

    delete_random_pod(self.namespace)
    # Verify that the delete_namespaced_pod method is not called
    mock_core_v1_api.return_value.delete_namespaced_pod.assert_not_called()

  @patch('pod_chaos_monkey.namespaced_delete.client.CoreV1Api')
  @patch('pod_chaos_monkey.namespaced_delete.config.load_config')
  def test_delete_random_pod_dry_run(self, mock_load_config, mock_core_v1_api):
    # Mock a pod
    mock_pod = MagicMock()
    mock_pod.metadata.name = "mock-pod"
    # Mock the returned list of pods
    mock_core_v1_api.return_value.list_namespaced_pod.return_value.items = [mock_pod]

    delete_random_pod(self.namespace, dry_run=True)
    # Verify that the delete_namespaced_pod method is not called
    mock_core_v1_api.return_value.delete_namespaced_pod.assert_not_called()


if __name__ == '__main__':
  unittest.main()
