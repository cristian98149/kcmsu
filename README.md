# kcmsu
K8s ConfigMaps and Secrets Usage it's a cronjob that allows you to monitor the usage of ConfigMaps and Secrets on your Kubernetes Cluster.

By checking all configmaps and secrets against PODs, it will help you to identify:
- unused ConfigMaps and Secrets
- which resource is using ConfigMaps and Secrets

# Installation
## Helm
Before installing it, check default chart values.

Also, check available chart versions [here](https://github.com/cristian98149/kcmsu/pkgs/container/kcmsu-chart).

```helm install kcmsu oci://ghcr.io/cristian98149/kcmsu-chart --version <VERSION>```

# Output
![image](https://github.com/user-attachments/assets/3ca2897f-982b-4372-ad68-50a8c27f619a)
