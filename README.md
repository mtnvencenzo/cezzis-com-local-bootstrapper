
# Cezzis.com Bootstrapper

This repository provides a bootstrapper for Cezzis.com, designed to facilitate the setup, configuration, and management of local development environments for Cezzis.com services. The bootstrapper automates the provisioning of essential infrastructure components, messaging systems, and storage solutions, enabling developers to quickly start and test Cezzis.com applications locally.

## Features

- **Automated Infrastructure Setup:**
	- Kafka
	- RabbitMQ
	- Azure Blob Storage
- **Modular Architecture:**
	- Organized by domain, infrastructure, and application layers
	- Extensible command structure for provisioning and configuration
- **Exception Handling & Observability:**
	- Global exception handler
	- OpenTelemetry integration for tracing
- **Configuration Management:**
	- Centralized options for each service
	- Easy customization for local development

## Usage

The bootstrapper provides a runtime process to create and configure instances of Kafka, RabbitMQ, and Azure Blob Storage. Each command is modular and can be extended or customized for additional services.

## ArgoCD Installation

Install the ArgoCD Application and ImageUpdater CR:

### K8s Cloud Sync (prod)
```shell
# Install the ArgoCD Application
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/cezzis-com-local-bootstrapper-cloudsync.yaml

# Install the ImageUpdater CR (manages automatic image updates)
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/image-updater-cloudsync.yaml

# Delete the ArgoCD Application
kubectl delete -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/cezzis-com-local-bootstrapper-cloudsync.yaml

# Delete the ImageUpdater CR (manages automatic image updates)
kubectl delete -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/image-updater-cloudsync.yaml

```

### K8s Loc
```shell
# Install the ArgoCD Application
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/cezzis-com-local-bootstrapper-loc.yaml

# Install the ImageUpdater CR (manages automatic image updates)
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/image-updater-loc.yaml

# Delete the ArgoCD Application
kubectl delete -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/cezzis-com-local-bootstrapper-loc.yaml

# Delete the ImageUpdater CR (manages automatic image updates)
kubectl delete -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/image-updater-loc.yaml

```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
