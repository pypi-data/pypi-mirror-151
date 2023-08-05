from glob import glob
import os
import pkg_resources

from .__about__ import __version__

templates = pkg_resources.resource_filename(
    "keyterms", "templates"
)

config = {
    "add": {
        "DOCKER_REGISTRY": "589371489025.dkr.ecr.us-east-2.amazonaws.com/",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ KEYTERMS_DOCKER_REGISTRY }}edx_key_terms_api:latest",
        "HOST": "keyterms.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "edx_key_terms_api",
        "MYSQL_USERNAME": "keyterms",
    }
}

hooks = {
    "init": ["lms", "mysql", "keyterms"],
    "build-image": {"keyterms": "{{ KEYTERMS_DOCKER_IMAGE }}"},
    "remote-image": {"keyterms": "{{ KEYTERMS_DOCKER_IMAGE }}"},
}


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename(
        "keyterms", "patches"
    )
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
