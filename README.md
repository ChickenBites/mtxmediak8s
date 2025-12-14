# MediaMTX Auto-Scaling Operator (K3s)

## Overview
A Kubernetes operator that automatically provisions MediaMTX instances based on the number of HLS inputs. It assigns up to 10 streams per instance and rebalances on updates.

## Repo layout
- deploy/: CRD, RBAC, Deployment, Namespace
- operator/: Python operator (kopf), Dockerfile, requirements.txt
- examples/: Sample StreamSet CR

## Build & push (Docker Hub)
Update the version (patch) and build/push the image:
