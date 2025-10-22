from textnode import TextType, TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, markdown_to_html_node
from markdownblock import markdown_to_blocks, extract_title

import os
import shutil
import re
import sys

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

def generate_pages(src, template, dst, site_root):
    print(f"Generating pages from {src} in {dst}")
    if not os.path.exists(dst):
        print(f"Making {dst}")
        os.mkdir(dst)
    else:
        print(f"Not making {dst} {os.path.isdir(dst)}")

    for file in os.listdir(src):
        file_path = f"{src}/{file}"
        if os.path.isdir(file_path):
            dst_path = f"{dst}/{file}"
            generate_pages(file_path, template, dst_path, site_root)
        else:
            filename_matches = re.findall(r"^(.*)(\.md)$", file)
            if len(filename_matches) == 1:
                filename_parts = filename_matches[0]
                print(filename_parts)
                print(f"Found markdown file: {file_path}")
                generate_page(file_path, template, f"{dst}/{filename_parts[0]}.html", site_root)


def generate_page(from_path, template_path, dest_path, site_root):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    content = ""
    with open(from_path, "r") as from_file:
        content = from_file.read()
    template = ""
    with open(template_path, "r") as template_file:
        template = template_file.read()
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    print(title)

    title_parts = template.split("{{ Title }}")

    new_title_parts = []
    for title_part in title_parts:
        content_parts = title_part.split("{{ Content }}")
        new_title_parts.append(html_content.join(content_parts))

    final_content = title.join(new_title_parts)
    if site_root != "/":
        final_content = f'href="{site_root}/'.join(final_content.split('href="/'))
        final_content = f'src="{site_root}/'.join(final_content.split('src="/'))

    with open(dest_path, "w") as dest_file:
        print(f"Destination: {dest_file}")
        dest_file.write(final_content)


def main():

    print(sys.argv)
    site_root = "/"
    if len(sys.argv) >= 2:
        site_root = sys.argv[1]
    if len(sys.argv) > 2:
        print("Usage: {sys.argv[0]} [site root]")
        exit(1)

    print(f"Site root is '{site_root}'")

    path = "static"
    dst = "public"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    copy_path(path, dst)

    content = "content"
    template = "template.html"
    generate_pages(content, template, dst, site_root)


if __name__ == "__main__":
    main()

