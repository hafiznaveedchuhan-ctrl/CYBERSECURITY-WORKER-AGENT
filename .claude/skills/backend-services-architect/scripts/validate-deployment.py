#!/usr/bin/env python3
"""
Validate Kubernetes deployment manifests for common issues
"""

import sys
import yaml
import re
from pathlib import Path
from typing import List, Tuple

class ManifestValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_file(self, filepath: str) -> bool:
        """Validate a single manifest file"""
        try:
            with open(filepath, 'r') as f:
                docs = yaml.safe_load_all(f)
                for doc in docs:
                    if doc:
                        self.validate_manifest(doc)
        except Exception as e:
            self.errors.append(f"Failed to parse {filepath}: {str(e)}")
            return False
        return True

    def validate_manifest(self, manifest: dict) -> None:
        """Validate a manifest object"""
        kind = manifest.get('kind', 'Unknown')
        name = manifest.get('metadata', {}).get('name', 'unknown')

        if kind == 'Deployment':
            self.validate_deployment(manifest, name)
        elif kind == 'Pod':
            self.validate_pod_spec(manifest.get('spec', {}), name)
        elif kind == 'Service':
            self.validate_service(manifest, name)

    def validate_deployment(self, manifest: dict, name: str) -> None:
        """Validate Deployment specific requirements"""
        spec = manifest.get('spec', {})
        template = spec.get('template', {})
        pod_spec = template.get('spec', {})
        containers = pod_spec.get('containers', [])

        # Check replicas
        replicas = spec.get('replicas', 1)
        if replicas < 3:
            self.warnings.append(f"Deployment '{name}': replicas ({replicas}) < 3 (recommended for production)")

        # Check strategy
        strategy = spec.get('strategy', {})
        if strategy.get('type') == 'RollingUpdate':
            rolling_update = strategy.get('rollingUpdate', {})
            max_unavailable = rolling_update.get('maxUnavailable')
            if max_unavailable != 0:
                self.warnings.append(f"Deployment '{name}': maxUnavailable should be 0 for zero-downtime updates")

        # Validate containers
        for i, container in enumerate(containers):
            self.validate_container(container, f"{name}[{i}]")

        # Check pod disruption budget
        # This is a warning only as PDB is defined separately

    def validate_container(self, container: dict, path: str) -> None:
        """Validate Container specification"""
        name = container.get('name', 'unknown')
        container_path = f"{path}/{name}"

        # Check resource limits
        resources = container.get('resources', {})
        if not resources.get('limits') or not resources.get('requests'):
            self.errors.append(f"Container '{container_path}': missing resource requests or limits")
        else:
            limits = resources.get('limits', {})
            requests = resources.get('requests', {})
            for resource in ['cpu', 'memory']:
                if resource not in limits:
                    self.errors.append(f"Container '{container_path}': missing resource limit for {resource}")
                if resource not in requests:
                    self.errors.append(f"Container '{container_path}': missing resource request for {resource}")

        # Check health probes
        if not container.get('livenessProbe'):
            self.warnings.append(f"Container '{container_path}': missing livenessProbe")
        if not container.get('readinessProbe'):
            self.warnings.append(f"Container '{container_path}': missing readinessProbe")

        # Check image policy
        image = container.get('image', '')
        if image.endswith(':latest'):
            self.errors.append(f"Container '{container_path}': using 'latest' tag (specify explicit version)")

        # Check security context
        if not container.get('securityContext'):
            self.warnings.append(f"Container '{container_path}': missing securityContext")
        else:
            sec_ctx = container.get('securityContext', {})
            if sec_ctx.get('runAsNonRoot') is not True:
                self.errors.append(f"Container '{container_path}': should run as non-root")

    def validate_service(self, manifest: dict, name: str) -> None:
        """Validate Service specification"""
        spec = manifest.get('spec', {})
        service_type = spec.get('type', 'ClusterIP')

        if service_type == 'LoadBalancer':
            self.warnings.append(f"Service '{name}': using LoadBalancer type (consider Ingress instead)")

    def print_report(self) -> None:
        """Print validation report"""
        if not self.errors and not self.warnings:
            print("✓ All manifests valid")
            return

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if self.errors:
            sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-deployment.py <manifest-file-or-dir>")
        sys.exit(1)

    path = Path(sys.argv[1])
    validator = ManifestValidator()

    if path.is_file():
        validator.validate_file(str(path))
    elif path.is_dir():
        for yaml_file in path.glob('**/*.yaml'):
            validator.validate_file(str(yaml_file))
        for yaml_file in path.glob('**/*.yml'):
            validator.validate_file(str(yaml_file))

    validator.print_report()

if __name__ == '__main__':
    main()
