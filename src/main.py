from kubernetes import client, config
from prettytable import PrettyTable

from utils.utils import list_cm, list_ns, list_secret, usage

if __name__ == "__main__":
    config.load_kube_config()
    api = client.CoreV1Api()

    selected_ns = list_ns(api).items

    table = PrettyTable(
        ['Namespace', 'Kind', 'Name', 'UsedCount', 'UsedAs', 'UsedBy'])
    table.align = "l"
    table.sortby = "UsedCount"

    for ns in selected_ns:
        ns_name = ns.metadata.name
        cm_list = list_cm(api, ns_name)
        secret_list = list_secret(api, ns_name)
        for cm in cm_list.items:
            cm_name = cm.metadata.name
            count, used_as, used_by = usage(api, ns_name, "config_map", cm_name)
            table.add_row(
                [ns_name, 'config-map', cm_name, count, used_as, used_by])
        for secret in secret_list.items:
            secret_name = secret.metadata.name
            count, used_as, used_by = usage(api, ns_name, "secret", secret_name)
            table.add_row(
                [ns_name, 'secret', secret_name, count, used_as, used_by])

    print(table)
