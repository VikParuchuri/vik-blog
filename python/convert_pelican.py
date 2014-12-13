import os
import html2text
import codecs

BASE_DIR = os.path.dirname(__file__)
POSTS_PATH = os.path.join(BASE_DIR, "_posts")

for filename in os.listdir(POSTS_PATH):
    if not filename.endswith(".md"):
        continue
    first_char = filename[0]
    f = codecs.open(os.path.join(POSTS_PATH, filename), "r", "utf-8")
    data = f.read()
    f.close()
    if first_char == "2":
        f = codecs.open(os.path.join(POSTS_PATH, "processed", filename), 'w+', 'utf-8')
        f.write(data)
        f.close()
        continue

    lines = data.split("\n")
    info = {
        "layout": "post"
    }
    post_start = ""
    content = []
    for line in lines:
        line_split = line.split(": ")
        if len(line_split) >= 2:
            try:
                tag, end = line_split
            except:
                tag = line_split[0]
                end = ": ".join(line_split[1:])
            if line.startswith("Title:"):
                info["title"] = end
            elif line.startswith("Date:"):
                info["date"] = end
                post_start = end.split(" ")[0]
            elif line.startswith("Slug:"):
                info["slug"] = end
            elif line.startswith("Modified:"):
                info["modified"] = end
            elif line.startswith("Status:"):
                info["status"] = end
            elif line.startswith("Tags:"):
                info["categories"] = end
            elif line.startswith("Category:"):
                continue
            elif len(line.strip()) > 1:
                content.append(line)
        else:
            content.append(line)
    content_flat = "\n".join(content)
    content_flat = content_flat.strip()
    h = html2text.HTML2Text()
    if content_flat.startswith("<div"):
        content_flat = content_flat.replace("<div class='post'>", '')
        content_flat = content_flat[:-6]
        content_flat = h.handle(content_flat)
    new_filename = "{0}-{1}".format(post_start, filename)
    f = codecs.open(os.path.join(POSTS_PATH, "processed", new_filename), 'w+', 'utf-8')
    write_lines = ["---"]
    for k in ["layout", "title", "date", "slug", "modified", "status", "categories"]:
        line = "{0}: {1}".format(k, info[k])
        write_lines.append(line)
    write_lines.append("---")
    write_lines.append("")
    write_lines.append(content_flat.strip())

    write_data = "\n".join(write_lines)
    f.write(write_data)
    f.close()