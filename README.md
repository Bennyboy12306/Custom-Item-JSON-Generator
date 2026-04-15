# Custom Item JSON Generator

A Python script that automatically generates JSON files for adding data driven custom items to Minecraft via a resource pack.

## Installation

1. Clone or download this script to your project root folder
2. Ensure your texture files are in the following directory (or within a folder contained within this directory):
   `assets/<namespace>/textures/item/`

## Usage

- Please note that some of the generated item json files will be contained all within the one folder.
- This means that despite subfolders being supported, all textures **MUST** have unique names.

Run the script from your project root folder with:

```
python json_generator.py
```

When prompted, enter your pack's namespace.

The required json files will be generated for you.

To get the item run the following command in game:

```
/give @s <item>[item_model="<namespace>:<custom_item_name>"]
```

Replacing `<item>`, `<namespace>` and `<custom_item_name>` with your desired values.

### Options

| Flag | Full Name | Description |
|------|-----------|-------------|
| -v | --verbose | Enable detailed output logging |


## Directory Structure

Here is an example of a valid project structure:

```
project-root/
├── assets/
│   └── <namespace>/
│       ├── textures/
│       │   └── item/
│       │       ├── optional_subfolder/
│       │       │   └── optional_subfolder_within_subfolder/
│       │       │       └── texture.png
│       │       └── another_optional_subfolder/
│       │           └── texture2.png
└── json_generator.py
```

As a minimum you need 1 texture anywhere inside of the `assets/<namespace>/textures/item/` directory
