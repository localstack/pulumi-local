import os
import subprocess
import tempfile
import uuid
from typing import Dict

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(THIS_PATH, "..")
PULUMILOCAL_BIN = os.path.join(ROOT_PATH, "bin", "pulumilocal")


def test_service_endpoints():
    # create bucket
    bucket_name = short_uid()

    assert "Invalid or unknown key. Check `pulumi config get aws:endpoints`." not in create_test_bucket(bucket_name), \
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


def short_uid() -> str:
    return str(uuid.uuid4())[0:8]


def run(cmd, **kwargs) -> str:
    try:
        kwargs["stderr"] = subprocess.PIPE
        return subprocess.check_output(cmd, **kwargs).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")
