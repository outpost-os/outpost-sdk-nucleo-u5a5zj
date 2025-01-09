# Outpost SDK for nucleo-u5a5zj development board

This repository is the SDK generation repository for the STM32 nucleo-u5a5zj board,
allowing to rebuild a complete SDK release of the Outpost OS for this board.

The content of the SDK is stored in the project.toml file, listing overall components part of the SDK.
SDK components configuration for the current board is set in the `configs` directory, while the current board
device tree is set in the `dts` directory.

## SDK build-dependencies

Download the python dependencies first, including the barbican Outpost project management tool:

```
pip install -r requirements.txt
```

Be sure to have the C cross-toolchain and the Rust toolchain for the Cortex-M33 target, meaning:

* the usual GCC arm-none-eabi toolchain, in a decently recent version (>=10).
* the rust thumbv8m.main-none-eabi toolchain, using rustup as usual for installation

Barbican also requires cargo-index crate in order to manipulate Rust package properly to be included as a
fully standalone, offline, SDK, please install it using cargo:

```
cargo install cargo-index
```

## Building the SDK

The SDK can now be built using the barbican outpost project tool

First download the SDK components, including, at least but not limited to, the Outpost kernel and runtime.

```
barbican download
```

Once sources are downloaded, setup the SDK build configuration:
```
barbican setup
```

To finish with, build the SDK:
```
ninja -C outpost/build
```


## Using the SDK

The effective SDK outpost, that can be stored in a tarball or any container, is generated in the `output/staging` directory.
This directory can be packaged using any container, including tarball, to be delivered, or through any artifact management tools.
The SDK is standalone, except for toolchains that are not yet a part of it.

When building a C application, the pkg_config directory is in the `usr/local/lib/pkgconfig` directory, allowing easy dependency
usage on the SDK libraries through standard pkg_config model.

For Rust, the Cargo repository that old all the Outpost crate that can be used by any library or application are stored in the
`usr/local/share/cargo/registry/outpost_sdk` directory.


This repository can be used as a template to generate a SDK for any other board that hold a Outpost-supported SoC such as
stm32l429, stm32wb55, stm32f429 and so on. Use the Sentry kernel examples configurations and device-tree for each of them as input
to initiate your board configuration and device-tree configuration.
