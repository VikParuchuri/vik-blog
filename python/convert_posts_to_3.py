import os

POST_DIR = os.path.abspath("../_posts")

for post in os.listdir(POST_DIR):
    full_path = os.path.join(POST_DIR, post)
    print(post)
    with open(full_path, 'r') as f:
        post_data = f.read()
    lines = post_data.split("\n")
    meta = {}
    append = False
    post_append = False
    post_lines = []
    for l in lines:
        if l.startswith("--") and not append and not post_append:
            append = True
            continue

        if l.startswith("--") and append:
            post_append = True
            append = False

        if append:
            k,v = l.split(":", 1)
            meta[k] = v.strip()

        if post_append:
            post_lines.append(l)

    if "subclass" in meta:
        continue

    meta["cover"] = "false"
    meta["tags"] = meta["categories"]
    meta["subclass"] = "post"
    meta["categories"] = "vik"


    new_post = ["---"]
    for k,v in sorted(meta.items(), key=lambda x: x[0]):
        new_post.append("{}: {}".format(k,v))
    new_post += post_lines

    write_data = "\n".join(new_post)

    with open(full_path, "w+") as f:
        f.write(write_data)



