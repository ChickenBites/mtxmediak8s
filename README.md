Overview:

A Kubernetes operator that automatically provisions and scales MediaMTX instances based on HLS input streams.

Streams per instance: Default 10.

Sidecar loader: ffmpeg ingests HLS URLs and republishes via RTMP.

Outputs: MediaMTX serves HLS, RTMP, RTSP.

Auto‑scaling: Operator spins up/down instances as streams are added or removed.

Setup:
Install K3s or k3d
    Linux: curl -sfL https://get.k3s.io | sh -
    Docker Desktop: k3d cluster create mediamtx

Deploy operator:

kubectl apply -f deploy/namespace.yaml
kubectl apply -f deploy/crd-streamset.yaml
kubectl apply -f deploy/rbac.yaml
kubectl apply -f deploy/operator-deployment.yaml

Create a StreamSet:

kubectl apply -f examples/streamset-sample.yaml

Usage:

Check operator logs

kubectl -n mediamtx logs deploy/mediamtx-operator

List resources

kubectl -n mediamtx get sset,deploy,svc

Access HLS output

kubectl -n mediamtx port-forward svc/sports-aggregator-mtx-0 8888:8888


Then Open: http://localhost:8888/live/stream-0000.m3u8


Config Options:

    urls: List of HLS input URLs.
    instanceSize: Max streams per instance (default 10).
    mediamtxImage: Override MediaMTX image.
    loaderImage: Override ffmpeg image.
    hlsEnabled: Enable/disable HLS output.

Example CR

apiVersion: media.example.com/v1alpha1
kind: StreamSet
metadata:
  name: fatbunny
  namespace: mediamtx
spec:
  instanceSize: 10
  urls:
    - https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8  
    - https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8 

Cleanup

kubectl -n mediamtx delete sset sports-aggregator