from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

config.load_kube_config()
v1 = client.CoreV1Api()


def get_pods():
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