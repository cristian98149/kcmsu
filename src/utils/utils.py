from kubernetes.client.rest import ApiException

def list_ns(api):
    try:
        api_response = api.list_namespace(pretty=True)
        return api_response
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespace: %s\n" % e)
    
def list_cm(api, ns):
    try:
        api_response = api.list_namespaced_config_map(namespace=ns, pretty=True)
        return api_response
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_config_map: %s\n" % e)

def list_secret(api, ns):
    try:
        api_response = api.list_namespaced_secret(namespace=ns, pretty=True)
        return api_response
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_secret: %s\n" % e)

def check_cm_usage(api, ns, cm):
    try:
        api_response = api.list_namespaced_pod(namespace=ns, pretty=True)

        count = 0
        env_from_count = 0
        volume_count = 0
        env_count = 0

        used_as = []
        used_by = []

        for pod in api_response.items:
            for c in pod.spec.containers:
                if c.env:
                    for env in c.env:
                        if env.value_from:
                            if env.value_from.config_map_key_ref:
                                if cm == env.value_from.config_map_key_ref.name:
                                    env_from_count += 1
        
        if env_from_count > 0:
            used_as.append("EnvFrom")
        
        count = env_from_count + volume_count + env_count
                            
        return count, used_as, used_by
    except ApiException as e:
        if "404" in str(e):
            print("No POD found in ns %s\n" % ns)
        else:
            print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)