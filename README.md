# Pulumi CLI for LocalStack

This package provides the `pulumilocal` command, which is a thin wrapper around the `pulumi`
command line interface to use [`Pulumi`](https://github.com/pulumi/pulumi) with [LocalStack](https://github.com/localstack/localstack).

## Installation

You can install the `pulumilocal` command via `pip`:

```
pip install pulumi-local
```

## Prerequisites

Please make sure you have a LocalStack instance running on your local machine.

## Usage

The `pulumilocal` command has the same usage as the `pulumi` command. For detailed usage,
please refer to the man pages of `pulumi -h`.

For example:
### Create a new Pulumi Project
```shell
export PULUMI_STACK_NAME=lsdev
export PULUMI_CONFIG_PASSPHRASE=lsdevtest
export PULUMI_BACKEND_URL=file://~/local-pulumi-state
mkdir ~/local-pulumi-state
mkdir mylsapp
cd mylsapp
pulumilocal new typescript -y -s $PULUMI_STACK_NAME
```

### Select the lsdev Pulumi Stack (it's already selected if doing all of this in order)
```shell
pulumilocal stack select lsdev
```

### Deploy the stack to LocalStack
```shell
pulumilocal up
```

## How it works

When running a deployment command like `pulumilocal up`, the wrapper script creates a `Pulumi.localstack.yaml` config file with local endpoint definitions, and then deploys a Pulumi stack called `localstack` to your LocalStack instance on `localhost`.

## Configurations

You can configure the following environment variables:

* `LOCALSTACK_HOSTNAME`: Target host to use for connecting to LocalStack (default: `localhost`)
* `EDGE_PORT`: Target port to use for connecting to LocalStack (default: `4566`)
* `PULUMI_CMD`: Name of the executable Pulumi command on the system PATH (default: `pulumi`)
* `PULUMI_STACK_NAME`: Name of the Pulumi stack used to configure local endpoints (default: `localstack`)

## Deploying to AWS
Use your preferred Pulumi backend. https://www.pulumi.com/docs/concepts/state/#deciding-on-a-state-backend
Change the `pulumilocal` command in the instructions above to `pulumi`.

## Change Log

* v0.6: Replace deprecated `s3ForcePathStyle` with `s3UsePathStyle` in default config
* v0.5: Remove deprecated `mobileanalytics` service config to fix invalid key error
* v0.4: Point pulumilocal.bat to the correct script
* v0.3: Add apigatewayv2 service endpoint
* v0.2: Add init command and add aws:region key by default
* v0.1: Initial release

## License

This software library is released under the Apache License, Version 2.0 (see `LICENSE`).

[pypi-version]: https://img.shields.io/pypi/v/pulumi-local.svg
[pypi]: https://pypi.org/project/pulumi-local/
