import logging
import os

import pandas as pd
from kubernetes import client, config
from tabulate import tabulate

from utils.utils import list_cm, list_ns, list_secret, usage

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    config.load_incluster_config()    # when running in a POD
    # config.load_kube_config() # when running locally
    api = client.CoreV1Api()

    namespaces = os.getenv("NAMESPACES", [])
    selected_ns = []
    cluster_namespaces = {}

    for ns in list_ns(api).items:
        cluster_namespaces.update({ns.metadata.name: ns})

    if namespaces:
        for ns in namespaces.split(","):
            if ns in cluster_namespaces:
                selected_ns.append(cluster_namespaces[ns])
            else:
                logging.warning(f"Namespace {ns} not found. Skipping it.")

    if not namespaces or not selected_ns:
        logging.info("Namespace list is empty. Checking all namespaces.")
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
