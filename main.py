from PIL import Image
import os
import random
import json
from tqdm import tqdm

# Set the paths of the directories containing the images
image_dirs = ["background", "tail", "ears", "body", "eyes"]
optional_dirs = ["glasses", "hat"]

# Set the paths of the directories to save the new images and metadata
image_save_dir = "./NewNFTs"
metadata_save_dir = "./Metadata"

# Get a list of the image filenames in each directory
image_filenames = []
for dir in image_dirs:
    dir_path = os.path.join("./", dir)
    filenames = os.listdir(dir_path)
    random.shuffle(filenames) # Shuffle the filenames
    image_filenames.append([os.path.join(dir_path, f) for f in filenames])

# Calculate the total number of possible combinations
num_combinations = 1
for filenames in image_filenames:
    num_combinations *= len(filenames)
num_optional_combinations = 2 ** len(optional_dirs)
total_combinations = num_combinations * num_optional_combinations

# Print the total number of possible combinations
print(f"There are {total_combinations} possible combinations.")

# Ask the user how many images they want to create
num_images = int(input("How many images do you want to create? "))

# Loop through the number of images and create each one
for i in tqdm(range(num_images)):
    # Load the first image to get the dimensions
    first_image = Image.open(image_filenames[0][0])
    width, height = first_image.size

    # Create a new image with the combined height
    combined_image = Image.new('RGB', (width, height))

    # Keep track of the images that have already been used
    used_images = set()

    # Initialize a list to hold the filenames of the images used to create the NFT
    image_filenames_used = []

    # Loop through the images in each directory and paste them vertically
    for filenames in image_filenames:
        # Loop until a unique image is found
        while True:
            layer_filename = random.choice(filenames)
            if layer_filename not in used_images:
                used_images.add(layer_filename)
                break

        layer = Image.open(layer_filename)
        combined_image.paste(layer, (0, 0), layer)

        # Add the filename of the image to the list of used images
        image_filenames_used.append(layer_filename)

    # Randomly decide whether or not to include the optional directories
    for dir in optional_dirs:
        if random.random() < 0.5:
            dir_path = os.path.join("./", dir)
            filenames = os.listdir(dir_path)
            random.shuffle(filenames) # Shuffle the filenames
            layer_filename = os.path.join(dir_path, filenames[0])
            layer = Image.open(layer_filename)
            combined_image.paste(layer, (0, 0), layer)

            # Add the filename of the image to the list of used images
            image_filenames_used.append(layer_filename)

    # Save the combined image as an NFT with a filename based on the image index
    filename = f"my_nft_{i+1}.png"
    filepath = os.path.join(image_save_dir, filename)
    combined_image.save(filepath)

    # Generate the metadata for the image
    metadata = {
        "name": f"My NFT {i+1}",
        "description": "This is a unique NFT created by combining multiple images.",
        "image": filename,
        "image_filenames_used": image_filenames_used
    }

    # Save the metadata as a JSON file with a filename based on the image index
    metadata_filename = f"my_nft_{i+1}_metadata.json"
    metadata_filepath = os.path.join(metadata_save_dir, metadata_filename)
    with open(metadata_filepath, "w") as f:
        json.dump(metadata, f, indent=4)

# Print a message when all images and metadata have been created
print(f"{num_images} images and metadata have been created")