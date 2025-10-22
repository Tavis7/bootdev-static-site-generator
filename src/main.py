from textnode import TextType, TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node
from markdownblock import markdown_to_blocks, extract_title

import os
import shutil
import re

def copy_path(src, dst):
    print(f"{src} -> {dst}")
    if os.path.exists(src):
        if not os.path.exists(dst):
            print(f"making {dst}")
            os.mkdir(dst)
        for file in os.listdir(src):
            filepath = f"{src}/{file}"
            print(f"copying {file}")
            if os.path.isdir(filepath):
                print(f"{file} is directory")
                copy_path(f"{src}/{file}", f"{dst}/{file}")
            else:
                print(f"{file} is file")
                shutil.copy(filepath, dst)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    content = ""
    with open(from_path, "r") as from_file:
        content = from_file.read()
    print(content)
    template = ""
    with open(template_path, "r") as template_file:
        template = template_file.read()
    print(template)
    html_content = markdown_to_html_node(content).to_html()
    print(html_content)

    title = extract_title(content)
    print(title)

    title_parts = template.split("{{ Title }}")

    print(title_parts)

    new_title_parts = []
    for title_part in title_parts:
        content_parts = title_part.split("{{ Content }}")
        new_title_parts.append(html_content.join(content_parts))

    final_content = title.join(new_title_parts)

    with open(dest_path, "w") as dest_file:
        dest_file.write(final_content)


def main():
    path = "static"
    dst = "public"
    shutil.rmtree(dst)
    copy_path(path, dst)

    generate_page("content/index.md", "template.html", f"{dst}/index.html")


if __name__ == "__main__":
    main()

