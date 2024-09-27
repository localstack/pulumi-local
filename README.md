# Pulumi CLI for LocalStack

**<u>DISCLAIMER</u>: pulumi-local currently does not support the _aws-native_ package. ([pulumi/pulumi-aws-native #108](https://github.com/pulumi/pulumi-aws-native/issues/108))**  

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

### Add environment variables to store state on local backend (optional)
```shell
export PULUMI_CONFIG_PASSPHRASE=lsdevtest
export PULUMI_BACKEND_URL=file://`pwd`/myproj
```
_Note: For further options please consult the official documentation on available [environment variables][env_vars] and [local backend][local_backend]._

[env_vars]: https://www.pulumi.com/docs/cli/environment-variables/
[local_backend]: https://www.pulumi.com/docs/concepts/state/#local-filesystem

### Create a new Pulumi project with stack name lsdev
```shell
mkdir myproj
pulumilocal new typescript -y -s lsdev --cwd myproj
```
_Note: `--cwd` switch is unnecessary if commands are being run in project directory._

### Select and create the lsdev Pulumi stack
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

* `AWS_ENDPOINT_URL`: hostname and port of the target LocalStack instance
* `LOCALSTACK_HOSTNAME`: __(Deprecated)__ Target host to use for connecting to LocalStack (default: `localhost`)
* `EDGE_PORT`: __(Deprecated)__ Target port to use for connecting to LocalStack (default: `4566`)
* `PULUMI_CMD`: Name of the executable Pulumi command on the system PATH (default: `pulumi`)
* `CONFIG_STRATEGY`: the strategy to handle config merging. If stack config already exists `pulumi-local` will prompt for user input. Possible values are:
  * `overwrite` (default): pulumi-local will overwrite the stack's config and replaces it with values necessary to communicate with LocalStack. This strategy is equivalent of the legacy behaviour.
  * `override`: generates a temporary config file from the current stack config and overrides it's values, after run this file will be deleted. The name of the file is generated from the `LS_STACK_NAME` variable.
  * `separate`: creates a separate stack with the stack name set in the `LS_STACK_NAME` env variable.
> [!NOTE]
> The fall through to the default strategy with a misconfigured or missing `CONFIG_STRATEGY` environment variable will be deprecated by the next `pulumi-local` version.
* `LS_STACK_NAME`: the stack name to use when the config file generated either with the `override` and `separate` strategy.
* `DRY_RUN`: only usable with `CONFIG_STRATEGY=override`, as a result the created temporary stack config is not deleted.
* `NON_INTERACTIVE`: starts a non-interactive session where all user prompts are automatically accepted

> [!WARNING]
> Using the `DRY_RUN` and `NON_INTERACTIVE` flags together changes the stack configuration without confirmation prompt. Use with caution!

## Deploying to AWS
Use your preferred Pulumi backend. https://www.pulumi.com/docs/concepts/state/#deciding-on-a-state-backend
Change the `pulumilocal` command in the instructions above to `pulumi`.

## Change Log

* v1.3.0: Add config merging strategies, dry-run and non-interactive runs.
* v1.2.2: Fix project URL in package metadata
* v1.2.1: Add support for AWS_ENDPOINT_URL env variable
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
