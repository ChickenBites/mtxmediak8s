def mediamtx_deployment(name, namespace, image="bluenviron/mediamtx:latest"):
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": name,
            "namespace": namespace,
            "labels": {"app": name},
        },
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [
                        {
                            "name": "mediamtx",
                            "image": image,
                            # Correct command: no --config flag
                            "command": ["mediamtx", "/etc/mediamtx/mediamtx.yml"],
                            "ports": [{"containerPort": 8888, "name": "hls"}],
                            "volumeMounts": [
                                {
                                    "name": "mediamtx-config",
                                    "mountPath": "/etc/mediamtx/mediamtx.yml",
                                    "subPath": "mediamtx.yml",
                                }
                            ],
                        }
                    ],
                    "volumes": [
                        {
                            "name": "mediamtx-config",
                            "configMap": {"name": "mediamtx-config"},
                        }
                    ],
                },
            },
        },
    }
