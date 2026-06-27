def pod_failure_prompt(status, logs):

    return f"""
You are a Senior Kubernetes DevOps Engineer.

Analyze the following Kubernetes pod.

Pod Status:
{status}

Logs:
{logs}

Explain:

1. Root Cause

2. Why it happened

3. Severity

4. Exact kubectl commands to fix it

5. Best Practices

Keep the answer beginner friendly.
"""

def deployment_prompt(deployment, events):
    return f"""
You are a Kubernetes DevOps expert.

Analyze this deployment:

Deployment:
{deployment}

Events:
{events}

Give:
1. Problem summary
2. Root cause
3. Fix steps
4. kubectl commands to resolve
"""
def cluster_prompt(pods):
    return f"""
You are a Kubernetes DevOps expert.

Analyze this cluster:

Pods:
{pods}

Task:
1. Identify failing pods
2. Identify risk patterns
3. Suggest fixes
4. Provide kubectl commands
5. Give cluster health summary (Good / Warning / Critical)
"""