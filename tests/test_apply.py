import os
import subprocess
import tempfile
import uuid
from typing import Dict, Tuple
import boto3
import pytest

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(THIS_PATH, "..")
PULUMILOCAL_BIN = os.path.join(ROOT_PATH, "bin", "pulumilocal")
LOCALSTACK_ENDPOINT = "http://localhost:4566"


# Removed latest version and pinning tests to 5.42.0 as pulumi/aws has serious performance issues
@pytest.mark.parametrize("package_version", ["5.42.0"])
@pytest.mark.parametrize("select_stack", [True, False])
@pytest.mark.parametrize("select_cwd", [True, False])
def test_provisioning(package_version: str, select_stack: bool, select_cwd: bool):
    # create bucket
    bucket_name = short_uid()
    create_test_bucket(bucket_name, package_version, select_stack, select_cwd)
    s3_bucket_names = get_bucket_names()

    # Pulumi adds suffix to the bucket's name so not enough simply checking for the name in the list
    assert any(s3_bucket.startswith(bucket_name) for s3_bucket in s3_bucket_names)


###
# UTIL FUNCTIONS
###


def deploy_pulumi_script(script: str, version: str, select_stack: bool, select_cwd: bool, env_vars: Dict[str, str] = None) -> str:
    kwargs = {}
    with tempfile.TemporaryDirectory() as temp_dir:
        if not select_cwd:
            kwargs["cwd"] = temp_dir
        env_vars.update({
            "PULUMI_BACKEND_URL": f"file://{temp_dir}"
        })
        kwargs["env"] = {**os.environ, **(env_vars or {})}

        cmd = [PULUMILOCAL_BIN, "new", "typescript", "-y", "-s", "test", "--cwd", temp_dir]
        out = run(cmd, **kwargs)
        if out[0]:
            return out[1]

        cmd = ["npm", "install", f"@pulumi/aws{'@'+ version}", "--prefix", temp_dir]
        out = run(cmd, **kwargs)
        if out[0]:
            return out[1]

        with open(os.path.join(temp_dir, "index.ts"), "w") as f:
            f.write(script)

        cmd = [PULUMILOCAL_BIN, "preview", "-y"]
        if select_stack:
            cmd.extend(["-s", "test"])
        if select_cwd:
            cmd.extend(["-C", temp_dir])
        out = run(cmd, **kwargs)

        cmd = [PULUMILOCAL_BIN, "up", "-y"]
        if select_stack:
            cmd.extend(["--stack", "test"])
        if select_cwd:
            cmd.extend(["--cwd", temp_dir])
        out = run(cmd, **kwargs)
        return out[1]


def create_test_bucket(bucket_name: str, version: str, select_stack: bool, select_cwd: bool) -> str:
    config = """import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("%s");

export const bucketName = bucket.id;
""" % (bucket_name)
    return deploy_pulumi_script(
        config,
        version=version,
        select_stack=select_stack,
        select_cwd=select_cwd,
        env_vars={"PULUMI_CONFIG_PASSPHRASE": "localstack"}
    )


def get_bucket_names(**kwargs: dict) -> list:
    s3 = client("s3", region_name="us-east-1", **kwargs)
    s3_buckets = s3.list_buckets().get("Buckets")
    return [s["Name"] for s in s3_buckets]


def short_uid() -> str:
    return str(uuid.uuid4())[0:8]


def client(service: str, **kwargs):
    # if aws access key is not set AND no profile is in the environment,
    # we want to set the access key and the secret key to test
    if "aws_access_key_id" not in kwargs and "AWS_PROFILE" not in os.environ:
        kwargs["aws_access_key_id"] = "test"
    if "aws_access_key_id" in kwargs and "aws_secret_access_key" not in kwargs:
        kwargs["aws_secret_access_key"] = "test"
    boto3.setup_default_session()
    return boto3.client(
        service,
        endpoint_url=LOCALSTACK_ENDPOINT,
        **kwargs,
    )


def run(cmd, **kwargs) -> Tuple:
    try:
        kwargs["stderr"] = subprocess.STDOUT
        kwargs["stdout"] = subprocess.PIPE
        sp = subprocess.run(cmd, **kwargs, check=True)
        return (sp.returncode, sp.stdout.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        return (e.returncode, e.stdout.decode("utf-8"))
