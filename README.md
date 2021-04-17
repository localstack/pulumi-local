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

For example, to deploy a Pulumi application to LocalStack:
```
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

## Change Log

* v0.1: Initial release

## License

This software library is released under the Apache License, Version 2.0 (see `LICENSE`).

[pypi-version]: https://img.shields.io/pypi/v/pulumi-local.svg
[pypi]: https://pypi.org/project/pulumi-local/
