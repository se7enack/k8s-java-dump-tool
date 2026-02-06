# k8s-java-dump-tool

A lightweight web-based utility for generating Java thread dumps and heap dumps from Java applications running inside Kubernetes pods.

This tool wraps common `kubectl exec` workflows behind a simple Python web service, making it easier to diagnose JVM issues such as deadlocks, high CPU usage, or memory leaks in Kubernetes environments.

## Features

- Generate Java thread dumps (`jstack`) from running pods
- Generate Java heap dumps (`jmap`) from running pods
- Simple web UI for selecting namespaces and pods
- Ability to download dump files locally
- Uses existing `kubectl` configuration (no cluster agents required)

## Requirements

- Python 3.7+
- `kubectl` installed locally
- Access to a Kubernetes cluster via kubeconfig
- Java applications running in Kubernetes pods
- JVM tools (`jstack`, `jmap`) available inside the target container

## Running
```
python3 /Users/${YOU}/Documents/tools/dumpv2/app.py >/dev/null 2>&1 & sleep 1 && open http://localhost:5001;fg
```

## Usage

### Web Interface

From the UI you can:

1. Select a Kubernetes namespace
2. Select a pod (and container, if applicable)
3. Trigger a thread dump
4. Trigger a heap dump
5. Download the generated dump files


<img width="715" height="449" alt="demo" src="https://github.com/user-attachments/assets/3fdf4c9c-3b1a-4293-88ab-0dfe547aefc2" />



