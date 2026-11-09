# avelynb.com

My personal site, built with [Hugo](https://gohugo.io) and Claude Code, and then published by GitHub Pages (pushed to my hosted domain name). 

## Preview it on your computer

Install Hugo once (`brew install hugo` on a Mac), then run this from this folder:

    hugo server -D

Then open http://localhost:1313. The page reloads every time you save a file.
`-D` also shows drafts.

## The routine of publishing, written here until I memorize it

**Option A: no terminal at all (use GitHub's website)**
1. On github.com, open the repo, go into `content/blog/` (or `content/gallery/`), then click
   **Add file → Create new file**.
2. Name it `my-title/index.md` (typing the `/` makes the folder). Paste this at the top:

       ---
       title: "My title"
       date: 2026-11-09
       ---

   then write the post under it.
3. For a gallery piece, open the new folder, click **Add file → Upload files** and drag in
   your images (call the jar image `cover.jpg`).
4. Commit to `main`. The site rebuilds itself in about a minute.

**Option B: on your laptop (lets you preview before it goes live)**
1. In Terminal, inside this folder: `hugo new content blog/my-title/index.md`
   (or `gallery/my-piece/index.md`). This only creates a folder with a starter text file.
2. Write in that file; drop images or videos into the same folder.
3. `hugo server` and look at http://localhost:1313.
4. Commit and push with GitHub Desktop. You push the whole repo; git only sends what changed.

**Option C: ask Claude** to "add a gallery entry called X" and attach the images.

New entries show up on the shelf by themselves; nothing else needs editing. Shelves fill from
the bottom-right (oldest) and a new shelf starts on top when one is full, so the newest entry
is always top-left.

Note: an entry dated in the future stays hidden until that date.

## Add a blog post (anotha book on ze shelf)

    hugo new content blog/my-post-title/index.md

Write in that file using Markdown. To pick the spine colour, add for example `spine: lagoon` to the
front matter at the top. Colour names live in `data/palette.yaml` (from the moodboard);
without one, each book gets a colour picked from its title.

## Add a gallery piece (a jar on the shelf)

    hugo new content gallery/my-piece/index.md

Put your images and videos in that `gallery/my-piece/` folder. Name the jar image
`cover.jpg`, or set `cover:` in the front matter. `lid: moss` picks the lid colour. In the text you can use:

- `![caption](photo.jpg)` for one image
- `{{< collage >}} ...images... {{< /collage >}}` for a grid
- `{{< video src="clip.mp4" >}}` for a video file
- `{{< youtube ID >}}` / `{{< vimeo ID >}}` for embedded videos

Keep videos small (under ~50 MB). For anything bigger, use YouTube or Vimeo.

## Where things live

| What | File |
|---|---|
| Home page note | `content/_index.md` |
| CV | `content/cv.md` (italic heading, then one `year – thing \` line per item) |
| Links, email, Instagram | `hugo.toml` |
| Home collage | `layouts/partials/collage.html`, images in `static/stickers/` |
| Look and feel | `assets/style.css` |
| Jar warping effect | `assets/jar.js` |
| Book / lid colours | `data/palette.yaml` |
| Shelf, dust, cloth textures | `static/textures/` (made by `tools/make_textures.py`) |
| Page templates | `layouts/` |

## Publishing

Pushing to `main` runs `.github/workflows/hugo.yml`, which builds the site and deploys it.
One-time setup: in the repo go to **Settings → Pages → Source** and choose **GitHub Actions**.

## Placeholders

Entries with `placeholder: true` in their front matter are dummy books and jars for seeing the
layout. Delete those folders before launch:

    grep -rl "placeholder: true" content | xargs -n1 dirname | xargs rm -rf
