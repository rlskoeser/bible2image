# run with python 3
import os
import argparse
import subprocess
import shutil

# simple slugify for bible books
def slugify(title):
    return title.lower().replace(" " , "-")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("verse")
    parser.add_argument("slug")
    args = parser.parse_args()

    print(args)

    # path is based on verse + slug
    # split from the right to get the verse number
    rest, verse_num = args.verse.rsplit(':', 1)
    # then split again to get chapter and book
    book, chapter = rest.rsplit(maxsplit=1)
    # slugify book for use in directory / url
    book_slug = slugify(book)
    # generate path to markdown file
    newpath = os.path.join("content", book_slug, chapter, verse_num, "%s.md" % args.slug)
    print("Creating new content page at %s" % newpath)
    # make sure containing directory exists
    # ... create _index.md if new directory (archetypes or type for book/verse?)
    # TODO: create hugo archetype for image page
    # run hugo new with correct path and title

    # determine image extension before renaming
    _, image_ext = os.path.splitext(args.image)

    # run hugo new with correct archetype and generated path; set env vars for title and image
    # use environment variables to pass in options for the template
    import_env = os.environ.copy()
    import_env["HUGO_POST_TITLE"] = args.verse
    # generate a name for the file to match the slug of the page
    image_filename = "%s%s" % (args.slug, image_ext)  # ext includes .
    import_env["HUGO_POST_IMG"] = image_filename
    #cmd = "hugo new --kind verse-image %s/%s/%s/%s.md" % (book, chapter, verse_num, args.slug)
    cmd = "hugo new --kind verse-image %s" % newpath
    print(cmd)
    # run the hugo command
    subprocess.run(cmd.split(), env=import_env)
    # move the image into the new directory
    target_dir = os.path.dirname(newpath)
    imagepath = os.path.join(target_dir, image_filename)
    print("Copying image from %s to %s" % (args.image, imagepath))
    shutil.copyfile(args.image, imagepath)

    # make sure the section index pages exist and have correct contents
    verse_index = os.path.join(target_dir, "_index.md")
    if not os.path.exists(verse_index):
        print("Creating index page for verse at %s" % verse_index)
        # title is the full verse reference
        with open(verse_index, "w") as indexfile:
            indexfile.write("---\ntitle: %s\n---" % args.verse)
    # check for chapter
    chapter_index = os.path.join(os.path.dirname(target_dir), "_index.md")
    if not os.path.exists(chapter_index):
        print("Creating index page for chapter at %s" % chapter_index)
        # title is the full book + chapter
        with open(chapter_index, "w") as indexfile:
            indexfile.write("---\ntitle: %s %s\n---" % (book, chapter))
    # check for book
    book_index = os.path.join(os.path.dirname(os.path.dirname(target_dir)), "_index.md")
    if not os.path.exists(book_index):
        print("Creating index page for book at %s" % book_index)
        # title is the book title
        with open(book_index, "w") as indexfile:
            indexfile.write("---\ntitle: %s\n---" % book)
    #  - bible api call to get the full verse text for the verse page?
    # https://labs.bible.org/api/?passage=John%203:16
    # remind to fill in other metadata?
    print("Remember to add verse content to verse index page %s" % verse_index)
