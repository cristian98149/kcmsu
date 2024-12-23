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
        print(
            "Exception when calling CoreV1Api->list_namespaced_config_map: %s\n"
            % e)


def list_secret(api, ns):
    try:
        api_response = api.list_namespaced_secret(namespace=ns, pretty=True)
        return api_response
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_namespaced_secret: %s\n" %
              e)


def list_pod(api, ns):
    try:
        api_response = api.list_namespaced_pod(namespace=ns, pretty=True)
        return api_response
    except ApiException as e:
        if "404" in str(e):
            print("No POD found in ns %s\n" % ns)
        else:
            print(
                "Exception when calling CoreV1Api->list_namespaced_pod: %s\n" %
                e)


def cm_usage(pods, cm):
    count = 0
    env_from_count = 0
    volume_count = 0
    env_count = 0
    used_as = []
    used_by = []

    for pod in pods.items:
        cm_in_pod = False
        if pod.spec.volumes:    # checking volume
            for volume in pod.spec.volumes:
                if volume.config_map:
                    if cm == volume.config_map.name:
                        volume_count += 1
                        cm_in_pod = True
        for c in pod.spec.containers:
            if c.env:    # checking env
                for item in c.env:
                    if item.value_from:
                        if item.value_from.config_map_key_ref:
                            if cm == item.value_from.config_map_key_ref.name:
                                env_count += 1
                                cm_in_pod = True
            if c.env_from:    # checking envFrom
                for item in c.env_from:
                    if item.config_map_ref:
                        if cm == item.config_map_ref.name:
                            env_from_count += 1
                            cm_in_pod = True

        if cm_in_pod:
            used_by.append(pod.metadata.name)

    count = env_from_count + volume_count + env_count

    if env_from_count > 0 and "EnvFrom" not in used_as:
        used_as.append("EnvFrom")
    elif env_count > 0 and "Env" not in used_as:
        used_as.append("Env")
    elif volume_count > 0 and "Volume" not in used_as:
        used_as.append("Volume")

    return count, used_as, used_by


def secret_usage(pods, secret):
    count = 0
    env_from_count = 0
    volume_count = 0
    env_count = 0
    used_as = []
    used_by = []

    for pod in pods.items:
        secret_in_pod = False
        if pod.spec.volumes:    # checking volume
            for volume in pod.spec.volumes:
                if volume.secret:
                    if volume.secret.items:
                        for item in volume.secret.items:
                            if secret == item.key:
                                volume_count += 1
                                secret_in_pod = True
        for c in pod.spec.containers:
            if c.env:    # checking env
                for item in c.env:
                    if item.value_from:
                        if item.value_from.secret_key_ref:
                            if secret == item.value_from.secret_key_ref.name:
                                env_count += 1
                                secret_in_pod = True
            if c.env_from:    # checking envFrom
                for item in c.env_from:
                    if item.secret_ref:
                        if secret == item.secret_ref.name:
                            env_from_count += 1
                            secret_in_pod = True

        if secret_in_pod:
            used_by.append(pod.metadata.name)

    count = env_from_count + volume_count + env_count

    if env_from_count > 0 and "EnvFrom" not in used_as:
        used_as.append("EnvFrom")
    elif env_count > 0 and "Env" not in used_as:
        used_as.append("Env")
    elif volume_count > 0 and "Volume" not in used_as:
        used_as.append("Volume")

    return count, used_as, used_by


def usage(api, ns, resource_type, name):
    pods = list_pod(api, ns)
    if resource_type == "config_map":
        count, used_as, used_by = cm_usage(pods, name)
    elif resource_type == "secret":
        count, used_as, used_by = secret_usage(pods, name)

    return count, used_as, used_by
