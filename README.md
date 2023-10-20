# Pulumi CLI for LocalStack

**<u>DISCLAIMER</u>: pulumi-local currently does not support the _aws-native_ package. ([pulumi/pulumi-aws-native #108](https://github.com/pulumi/pulumi-aws-native/issues/108))**
**<u>DISCLAIMER</u>: due to the degraded performance of _pulumi-aws@6.x_ with local endpoints, we highly recommend to all our users to pin their package version _<=5.42.0_. ([pulumi/pulumi-aws #2880](https://github.com/pulumi/pulumi-aws/issues/2880))**

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

When running any pulumi deployment command like `pulumilocal ["up", "destroy", "preview", "cancel"]`,
the wrapper script runs the `pulumi config` command to augment the pulumi config with LocalStack AWS configuration,
and then runs the original pulumi command. 

## Configurations

You can configure the following environment variables:

* `LOCALSTACK_HOSTNAME`: Target host to use for connecting to LocalStack (default: `localhost`)
* `EDGE_PORT`: Target port to use for connecting to LocalStack (default: `4566`)
* `PULUMI_CMD`: Name of the executable Pulumi command on the system PATH (default: `pulumi`)

## Deploying to AWS
Use your preferred Pulumi backend. https://www.pulumi.com/docs/concepts/state/#deciding-on-a-state-backend
Change the `pulumilocal` command in the instructions above to `pulumi`.

## Change Log

* v1.2.0: Added dynamic endpoint generation and tests
* v1.1: Added README to long description and update twine publish.
* v1.0: Using `pulumi config set-all` to set all the AWS provider configurating instead of modifying
  the Stack file directly. Removed defaulting the stack name to `localstack`. Added argparse. 
  Removed pyyaml dependency. Removed python2 package classifiers. 
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
