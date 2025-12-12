# scripts/post_install.py
import os
from pathlib import Path

import certifi


def add_custom_certs(azturite_cert_path: Path | None = None, docker_cert_path: Path | None = None) -> None:
    certifi_bundle = Path(certifi.where())

    azturite_cert_path = azturite_cert_path or Path.home() / "Github/dev-certs/azurite-local/azurite-local.crt"
    docker_cert_path = docker_cert_path or Path.home() / "Github/dev-certs/docker-local/docker-local.crt"

    # Define custom cert paths using home directory
    home = Path.home()
    cert_paths = [
        azturite_cert_path,
        docker_cert_path,
    ]

    # Read existing bundle
    existing_certs = certifi_bundle.read_text()

    # Append custom certs if not already present
    for cert_path in cert_paths:
        if not cert_path.exists():
            print(f"Warning: Certificate not found at {cert_path}")
            continue

        cert_content = cert_path.read_text().strip()
        cert_name = cert_path.stem

        # Check if the actual certificate content is already in the bundle
        if cert_content in existing_certs:
            print(f"✓ {cert_name} already in certifi bundle")
        else:
            with certifi_bundle.open("a") as f:
                f.write(f"\n\n# Custom certificate: {cert_name}\n")
                f.write(cert_content)
                f.write("\n")
            print(f"✓ Added {cert_name} to certifi bundle")


if __name__ == "__main__":
    add_custom_certs(
        azturite_cert_path=Path(str(os.environ.get("AZTURITE_CERT_PATH"))) if os.environ.get("AZTURITE_CERT_PATH") else None,
        docker_cert_path=Path(str(os.environ.get("DOCKER_LOCAL_CERT_PATH"))) if os.environ.get("DOCKER_LOCAL_CERT_PATH") else None,
    )
