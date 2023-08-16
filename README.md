# Pulumi CLI for LocalStack

This package provides the `pulumilocal` command, which is a thin wrapper around the `pulumi`
command line interface to use [`Pulumi`](https://github.com/pulumi/pulumi) with [LocalStack](https://github.com/localstack/localstack).

## Version Notices
### v1.0
1. Removed PULUMI_STACK_NAME and no longer default to a Pulumi Stack name of `localstack`. The `pulumi` cmd and env determines the Stack name.


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
### Create a new Pulumi Project with Stack name lsdev
```shell
mkdir myproj
export PULUMI_CONFIG_PASSPHRASE=lsdevtest
export PULUMI_BACKEND_URL=file://`pwd`/myproj
pulumilocal new typescript -y -s lsdev --cwd myproj
```

### Select and Create the lsdev Pulumi Stack
This is unnecessary if you just did the `new typescript` command above as it will already be selected.
```shell
pulumilocal stack select -c lsdev --cwd myproj
```

### Deploy the stack to LocalStack
```shell
pulumilocal up --cwd myproj
```

## How it works

When running a deployment command like `pulumilocal up`, the wrapper script creates a `Pulumi.localstack.yaml` config file with local endpoint definitions, and then deploys a Pulumi stack called `localstack` to your LocalStack instance on `localhost`.

## Configurations

You can configure the following environment variables:

* `LOCALSTACK_HOSTNAME`: Target host to use for connecting to LocalStack (default: `localhost`)
* `EDGE_PORT`: Target port to use for connecting to LocalStack (default: `4566`)
* `PULUMI_CMD`: Name of the executable Pulumi command on the system PATH (default: `pulumi`)

## Deploying to AWS
Use your preferred Pulumi backend. https://www.pulumi.com/docs/concepts/state/#deciding-on-a-state-backend
Change the `pulumilocal` command in the instructions above to `pulumi`.

## License

This software library is released under the Apache License, Version 2.0 (see `LICENSE`).

[pypi-version]: https://img.shields.io/pypi/v/pulumi-local.svg
[pypi]: https://pypi.org/project/pulumi-local/
