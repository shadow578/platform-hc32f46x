# HUADA HC32F460 Series development platform for [PlatformIO](https://platformio.org)

The HC32F460 Series of MCUs is a 32-bit MCU based on the ARM Cortex-M4 processor.
It integrates up to 512 KB of Flash memory, and up to 192 KB of SRAM.

These MCUs are somewhat often found in entry level 3D printers, tho development boards are rumored to exist as well.

> [!NOTE]
> if you have a source for development boards that ships to Europe and is not absurdly expensive, please let me know by opening an issue.


## Getting Started

to get started using the HC32F460 platform, use the following in your [`platformio.ini`](https://docs.platformio.org/page/projectconf.html) file:

current *development* version:
```ini
[env:my_env]
platform = https://github.com/shadow578/platform-hc32f46x.git
framework = arduino
board = generic_hc32f460
```

latest release versions:
```ini
[env:my_env]
platform = https://github.com/shadow578/platform-hc32f46x/archive/1.0.0.zip
platform_packages =
  framework-hc32f46x-ddl @ https://github.com/shadow578/framework-hc32f46x-ddl/archive/2.2.1.zip
  framework-arduino-hc32f46x @ https://github.com/shadow578/framework-arduino-hc32f46x/archive/1.1.0.zip

framework = arduino
board = generic_hc32f460
```

> [!TIP]
> when pinning the version, check you're using the latest release(s) to benefit from the latest improvements.

> [!NOTE]
> please refer to [framework-hc32f46x-ddl](https://github.com/shadow578/framework-hc32f46x-ddl) and [framework-arduino-hc32f46x](https://github.com/shadow578/framework-arduino-hc32f46x/) for more information on the frameworks themselves.


## Configuration

the platform itself contains basically no configuration options.
everything is configured in the framework packages.

please refer to [framework-arduino-hc32f46x](https://github.com/shadow578/framework-arduino-hc32f46x) and [framework-hc32f46x-ddl](https://github.com/shadow578/framework-hc32f46x-ddl) for more information.


## Uploading & Debugging

please refer to [HOW_TO_UPLOAD](./docs/HOW_TO_UPLOAD.md) and [HOW_TO_DEBUG](./docs/HOW_TO_DEBUG.md) for information on how to upload and debug your code on the HC32F460 platform.

## License

this project is licensed under the [GPL-3.0](./LICENSE) license.
