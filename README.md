
# Cezzis.com Bootstrapper

This repository provides a bootstrapper for Cezzis.com, designed to facilitate the setup, configuration, and management of local development environments for Cezzis.com services. The bootstrapper automates the provisioning of essential infrastructure components, messaging systems, and storage solutions, enabling developers to quickly start and test Cezzis.com applications locally.

## Features

- **Automated Infrastructure Setup:**
	- CosmosDB
	- Qdrant
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

The bootstrapper provides a runtime process to create and configure instances of CosmosDB, Qdrant, Kafka, RabbitMQ, and Azure Blob Storage. Each command is modular and can be extended or customized for additional services.

## ArgoCD Installation

Install the ArgoCD Application and ImageUpdater CR:

```shell
# Install the ArgoCD Application
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/cezzis-com-local-boostrapper.yaml

# Install the ImageUpdater CR (manages automatic image updates)
kubectl apply -f https://raw.githubusercontent.com/mtnvencenzo/cezzis-com-local-bootstrapper/refs/heads/main/.iac/argocd/image-updater.yaml
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
