import os
import shutil
import re

from htmlnode import markdown_to_html_node
from markdownblock import extract_title

def generate_site(static, src, template, dst, site_root="/"):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    copy_path(static, dst)

    generate_pages(src, template, dst, site_root)



def copy_path(src, dst):
    if os.path.exists(src):
        if not os.path.exists(dst):
            os.mkdir(dst)
        for file in os.listdir(src):
            filepath = f"{src}/{file}"
            if os.path.isdir(filepath):
                copy_path(f"{src}/{file}", f"{dst}/{file}")
            else:
                shutil.copy(filepath, dst)

def generate_pages(src, template, dst, site_root):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for file in os.listdir(src):
        file_path = f"{src}/{file}"
        if os.path.isdir(file_path):
            dst_path = f"{dst}/{file}"
            generate_pages(file_path, template, dst_path, site_root)
        else:
            filename_matches = re.findall(r"^(.*)(\.md)$", file)
            if len(filename_matches) == 1:
                filename_parts = filename_matches[0]
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
        dest_file.write(final_content)


