import sys

from generatesite import generate_site

def main():

    site_root = "/"
    dst = "public"

    if len(sys.argv) >= 2:
        site_root = sys.argv[1]
    if len(sys.argv) >= 3:
        dst = sys.argv[2]

    if len(sys.argv) > 3:
        print("Usage: {sys.argv[0]} [<site root> [<destination directory>]")
        exit(1)

    if site_root[0] != "/":
        print("Error: site root must start with '/'")
        exit(1)

    print(f"Site root is '{site_root}'")
    print(f"Destination directory is '{dst}'")

    static = "static"
    content = "content"
    template = "template.html"

    generate_site(static, content, template, dst, site_root)

if __name__ == "__main__":
    main()

