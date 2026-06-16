from parser import *
import os
import shutil

def static_to_public(src: str, dest: str, delete: bool = False):
    # Delete the current public directory and create an empty one
    # Only if this is the first iteration
    if delete:
        shutil.rmtree(dest)
        os.mkdir(dest)
    # Iterate through files in the source directory
    for f in os.listdir(src):
        src_path = f"{src}/{f}"
        dest_path = f"{dest}/{f}"
        # Check to see the file really exists in the directory
        if os.path.exists(src_path):
            # If it's a regular file, copy it
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
                print(f"Copied {src_path} to {dest_path}")
            # If it's a directory, recursively roll through it
            elif os.path.isdir(src_path):
                os.mkdir(dest_path)
                static_to_public(src_path, dest_path)


def generate_page(src_path, dest_path, template_path):
    print(f"Generating  page from {src_path} to {dest_path} using {template_path}")
    # Take in the markdown and template files
    with open(src_path, "r") as src_text, open(template_path, "r") as template:
        source = src_text.read()
        out_doc = template.read()
        # Generate html from the markdown
        html = markdown_to_html(source).to_html()
        header = extract_title(source)
        # Fill in the template
        out_doc = out_doc.replace("{{ Title }}", header)
        out_doc = out_doc.replace("{{ Content }}", html)
    # Write out to the proper file
    with open(dest_path, "w") as file:
        file.write(out_doc)


def generate_pages(src: str, dest: str, template: str):
    # Iterate through files in the source directory
    for f in os.listdir(src):
        src_path = f"{src}/{f}"
        dest_path = f"{dest}/{f}"
        # Check to see the file really exists in the directory
        if os.path.exists(src_path):
            # If it's a regular file, copy it
            if os.path.isfile(src_path) and src_path[-3:] == ".md":
                dest_path =  dest_path[:-3] + ".html"
                generate_page(src_path, dest_path, template)
            # If it's a directory, recursively roll through it
            elif os.path.isdir(src_path):
                os.mkdir(dest_path)
                generate_pages(src_path, dest_path, template)

def main():
    static_to_public("./static", "./public", True)
    generate_pages("./content", "./public", "./template.html")

main()
