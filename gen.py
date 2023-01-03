#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script generates the Garden Cloche recipes for Thermal Cultivation.
It takes the thermal_cultivation-1.18.2-*.jar file as an argument.

Usage: gen.py <path to thermal_cultivation-1.18.2-*.jar> <output folder>
"""

import sys
import os
import json
import zipfile


def main():
    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        print(
            "Usage: gen.py",
            "<path to thermal_cultivation-1.18.2-*.jar>",
            "<output folder>",
            sep=" ",
        )
        sys.exit(1)

    # Path to the thermal_cultivation-1.18.2-*.jar file
    path = sys.argv[1]

    # Check if the file exists
    if not os.path.isfile(path):
        print("File does not exist")
        sys.exit(1)

    # Check if the file is a jar file
    if not path.endswith(".jar"):
        print("File is not a jar file")
        sys.exit(1)

    # Check if the file has the correct name
    if not os.path.basename(path).startswith("thermal_cultivation-1.18.2-"):
        print("File has the wrong name")
        sys.exit(1)

    # Output folder path
    output_folder = sys.argv[2]

    # Check if the output folder exists
    if not os.path.isdir(output_folder):
        print("Output folder does not exist")
        sys.exit(1)

    # Check if the output folder is empty
    if os.listdir(output_folder):
        print("Warning: Output folder is not empty")
        input("Press Enter to continue...")

    # Open the jar file as a zip file
    jar = zipfile.ZipFile(path, "r")

    # Read the files starting with "data/thermal/recipes/machines/insolator/"
    files = jar.namelist()
    files = [
        file
        for file in files
        if file.startswith("data/thermal/recipes/machines/insolator/")
        and file.endswith(".json")
    ]

    # Iterate over the files
    for file in files:
        # Read the file
        data: dict = json.loads(jar.read(file).decode("utf-8"))

        # Get the name of the item
        item_id: str = data.get("ingredient").get("item")

        # Create the output file name
        output_file_name: str = item_id.split(":")[1] + ".json"

        # Create the output file path
        output_path: str = os.path.join(output_folder, output_file_name)

        # Get the time modifier
        time_modifier: float = data.get("energy_mod", 1.0)

        # Get the results list and reform it
        results: list[dict] = []
        for result in data.get("result", []):
            results.append(
                {
                    "item": result.get("item"),
                    "count": int(result.get("chance", 1)),
                }
            )

        # Create the base output data
        output_data: dict = {
            "type": "immersiveengineering:cloche",
            "results": results,
            "input": {
                "item": item_id,
            },
            "soil": [
                {
                    "item": "minecraft:dirt",
                }
            ],
            "time": 800 * time_modifier,
            "render": {
                "type": "crop",
            },
        }

        if item_id == "thermal:frost_melon_seeds":
            # Update the render type
            output_data["render"]["type"] = "stem"

            # Get the stem block
            stem_block: str = item_id.split("_seeds")[0]

            # Update the render block
            output_data["render"]["block"] = stem_block

        elif item_id.endswith("_seeds"):
            # Get the crop block
            crop_block: str = item_id.split("_seeds")[0]

            # Update the output data
            output_data["render"]["block"] = crop_block

        elif item_id.endswith("_spores"):
            # Get the crop block
            crop_block: str = item_id.split("_spores")[0]

            # Update the output data
            output_data["render"]["block"] = crop_block

            # Change the soil list
            output_data["soil"] = [
                {
                    "item": "minecraft:mycelium",
                },
                {
                    "item": "minecraft:podzol",
                },
            ]

        # Write the output data to the output file
        output_file = open(output_path, "w")
        output_file.write(json.dumps(output_data, indent=4))
        output_file.close()

    # Close the jar file
    jar.close()


if __name__ == "__main__":
    main()
