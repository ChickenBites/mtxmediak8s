import time
from kubernetes import client, config

NAMESPACE = "mediamtx"
CR_NAME = "fatbunny"

def apply_streamset(urls):
    """Apply a StreamSet CR with the given URLs."""
    crd_api = client.CustomObjectsApi()
    body = {
        "apiVersion": "media.example.com/v1alpha1",
        "kind": "StreamSet",
        "metadata": {"name": CR_NAME, "namespace": NAMESPACE},
        "spec": {
            "hlsEnabled": True,
            "instanceSize": 10,
            "mediamtxImage": "bluenviron/mediamtx:latest",
            "loaderImage": "jrottenberg/ffmpeg:5.1-alpine",
            "urls": urls,
        },
    }
    crd_api.patch_namespaced_custom_object(
        group="media.example.com",
        version="v1alpha1",
        namespace=NAMESPACE,
        plural="streamsets",
        name=CR_NAME,
        body=body,
    )

def count_instances():
    """Count how many MediaMTX deployments exist for this StreamSet."""
    apps = client.AppsV1Api()
    deps = apps.list_namespaced_deployment(namespace=NAMESPACE).items
    return len([d for d in deps if d.metadata.name.startswith(CR_NAME + "-mtx-")])

def test_scaling():
    config.load_kube_config()

    # Case 1: more than 10 streams
    urls = [f"https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8" for _ in range(12)]
    apply_streamset(urls)
    time.sleep(30)  # wait for reconcile
    instances = count_instances()
    assert instances == 2, f"Expected 2 instances, got {instances}"
    print("Scaling up test passed: 12 streams -> 2 instances")

    # Case 2: fewer than 10 streams
    urls = [f"https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8" for _ in range(8)]
    apply_streamset(urls)
    time.sleep(30)  # wait for reconcile
    instances = count_instances()
    assert instances == 1, f"Expected 1 instance, got {instances}"
    print("Scaling down test passed: 8 streams -> 1 instance")

if __name__ == "__main__":
    test_scaling()
