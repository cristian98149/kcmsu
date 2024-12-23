import pandas as pd
from kubernetes import client, config
from tabulate import tabulate

from utils.utils import list_cm, list_ns, list_secret, usage

if __name__ == "__main__":
    config.load_kube_config()
    api = client.CoreV1Api()

    selected_ns = list_ns(api).items

    df = pd.DataFrame(
        columns=['Namespace', 'Kind', 'Name', 'UsedCount', 'UsedAs', 'UsedBy'])

    for ns in selected_ns:
        ns_name = ns.metadata.name
        cm_list = list_cm(api, ns_name)
        secret_list = list_secret(api, ns_name)
        for cm in cm_list.items:
            cm_name = cm.metadata.name
            count, used_as, used_by = usage(api, ns_name, "config_map", cm_name)
            df.loc[len(df)] = {
                "Namespace": ns_name,
                "Kind": "config-map",
                "Name": cm_name,
                "UsedCount": count,
                "UsedAs": used_as,
                "UsedBy": used_by
            }
        for secret in secret_list.items:
            secret_name = secret.metadata.name
            count, used_as, used_by = usage(api, ns_name, "secret", secret_name)
            df.loc[len(df)] = {
                "Namespace": ns_name,
                "Kind": "secret",
                "Name": secret_name,
                "UsedCount": count,
                "UsedAs": used_as,
                "UsedBy": used_by
            }

    selected_ns_name = []

    if selected_ns_name:
        print(
            tabulate(df[df['Namespace'].isin(selected_ns_name)].sort_values(
                'UsedCount'),
                     headers='keys',
                     tablefmt='psql',
                     showindex=False))
    else:
        print(
            tabulate(df.sort_values('UsedCount'),
                     headers='keys',
                     tablefmt='psql',
                     showindex=False))
