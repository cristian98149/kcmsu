# kcmsu
K8s ConfigMaps and Secrets Usage it's a cronjob that allows you to monitor the usage of ConfigMaps and Secrets on your Kubernetes Cluster.

By checking all configmaps and secrets against PODs, it will help you to identify:
- unused ConfigMaps and Secrets
- which resource is using ConfigMaps and Secrets
- how ConfigMaps and Secrets are used (volume, env, envFrom)

# Installation
## Helm
Before installing it, check default chart values.

Also, check available chart versions [here](https://github.com/cristian98149/kcmsu/pkgs/container/kcmsu-chart).

```helm install kcmsu oci://ghcr.io/cristian98149/kcmsu-chart --version <VERSION>```

# Output
![image](https://github.com/user-attachments/assets/d26176d1-78b3-4b4e-84d3-484a9e60909f)

