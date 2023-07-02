import unittest
from unittest.mock import patch, MagicMock
from pod_chaos_monkey.namespaced_delete import delete_random_pod

class TestPodChaosMonkey(unittest.TestCase):

  @patch('pod_chaos_monkey.namespaced_delete.client.CoreV1Api')
  @patch('pod_chaos_monkey.namespaced_delete.config.load_config')
  def test_delete_random_pod(self, mock_load_config, mock_core_v1_api):
    namespace = "target-namespace"

    # Mock a pod
    mock_pod = MagicMock()
    mock_pod.metadata.name = "mock-pod"
    # Mock the returned list of pods
    mock_core_v1_api.return_value.list_namespaced_pod.return_value.items = [mock_pod]

    delete_random_pod(namespace)
    mock_load_config.assert_called()
    # Verify that the delete_namespaced_pod method is called
    mock_core_v1_api.return_value.delete_namespaced_pod.assert_called_with("mock-pod", namespace)

  #TODO: Test if list is empty

if __name__ == '__main__':
  unittest.main()
