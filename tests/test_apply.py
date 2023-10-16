import os
import subprocess
import tempfile
import uuid
from typing import Dict
import boto3

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(THIS_PATH, "..")
PULUMILOCAL_BIN = os.path.join(ROOT_PATH, "bin", "pulumilocal")
LOCALSTACK_ENDPOINT = "http://localhost:4566"


def test_successful_provisioning():
    # create bucket
    bucket_name = short_uid()
    create_test_bucket(bucket_name)
    s3_bucket_names = get_bucket_names()

    # Pulumi adds suffix to the bucket's name so not enough simply checking for the name in the list
    assert any(s3_bucket.startswith(bucket_name) for s3_bucket in s3_bucket_names)


def test_service_endpoints():
    # create bucket
    bucket_name = short_uid()
    error_message = "Invalid or unknown key. Check `pulumi config get aws:endpoints`."

    assert error_message not in create_test_bucket(bucket_name), \
        "Endpoints list is not up-to-date."

###
# UTIL FUNCTIONS
###


def deploy_pulumi_script(script: str, env_vars: Dict[str, str] = None) -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        kwargs = {"cwd": temp_dir}
        env_vars.update({
            "PULUMI_BACKEND_URL": f"file://{temp_dir}"
        })
        kwargs["env"] = {**os.environ, **(env_vars or {})}

        run([PULUMILOCAL_BIN, "new", "typescript", "-y", "-s", "test", "--cwd", temp_dir], **kwargs)
        run(["npm", "install", "@pulumi/aws", "--prefix", temp_dir], **kwargs)
        with open(os.path.join(temp_dir, "index.ts"), "w") as f:
            f.write(script)
        run([PULUMILOCAL_BIN, "stack", "select", "-c", "test", "--cwd", temp_dir], **kwargs)
        out = run([PULUMILOCAL_BIN, "up", "--cwd", temp_dir, "-y"], **kwargs)
        return out


def create_test_bucket(bucket_name: str) -> str:
    config = """import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("%s");

export const bucketName = bucket.id;
""" % (bucket_name)
    return deploy_pulumi_script(
        config,
        env_vars={"PULUMI_CONFIG_PASSPHRASE": "localstack"}
    )


def get_bucket_names(**kwargs: dict) -> list:
    s3 = client("s3", region_name="eu-west-1", **kwargs)
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


def run(cmd, **kwargs) -> str:
    try:
        kwargs["stderr"] = subprocess.PIPE
        return subprocess.check_output(cmd, **kwargs).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")
