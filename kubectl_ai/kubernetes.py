from kubernetes import client, config
from kubernetes import config, client

# Load kubeconfig automatically
config.load_kube_config()
from kubernetes import client

apps_v1 = client.AppsV1Api()
core_v1 = client.CoreV1Api()
from kubernetes.client.exceptions import ApiException

config.load_kube_config()
v1 = client.CoreV1Api()
try:
    config.load_kube_config()
except Exception as e:
    print("Kubernetes config not found or cluster not running")

def get_pods():
    return v1.list_pod_for_all_namespaces(watch=False).items
def get_deployment(namespace, deployment_name):
    return apps_v1.read_namespaced_deployment(deployment_name, namespace)
def get_events(namespace):
    return core_v1.list_namespaced_event(namespace)
def get_all_pods():
    return v1.list_pod_for_all_namespaces(watch=False).items

def get_pod(namespace, pod_name):
    try:
        return v1.read_namespaced_pod(
            name=pod_name,
            namespace=namespace
        )
    except ApiException:
        return None


def get_pod_logs(namespace, pod_name):
    try:
        return v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=30
        )
    except ApiException:
        return "Unable to read logs."
    
def get_pod_status(namespace, pod):
    pod_info = v1.read_namespaced_pod(pod, namespace)
    return pod_info.status.phase