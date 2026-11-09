# avelynb.com

My personal site, built with [Hugo](https://gohugo.io) and published by GitHub Pages.

## Preview it on your computer

Install Hugo once (`brew install hugo` on a Mac), then run this from this folder:

    hugo server -D

Then open http://localhost:1313. The page reloads every time you save a file.
`-D` also shows drafts.

## Add a blog post (a book on the shelf)

    hugo new content blog/my-post-title/index.md

Write in that file using Markdown. To pick the spine color, add `spine: "#1f3a5f"` to the
front matter at the top. Books are ordered by `date`, oldest on the left.

## Add a gallery piece (a jar on the shelf)

    hugo new content gallery/my-piece/index.md

Put your images and videos in that `gallery/my-piece/` folder. Name the jar image
`cover.jpg`, or set `cover:` in the front matter. In the text you can use:

- `![caption](photo.jpg)` for one image
- `{{< collage >}} ...images... {{< /collage >}}` for a grid
- `{{< video src="clip.mp4" >}}` for a video file
- `{{< youtube ID >}}` / `{{< vimeo ID >}}` for embedded videos

Keep videos small (under ~50 MB). For anything bigger, use YouTube or Vimeo.

## Where things live

| What | File |
|---|---|
| Home page note | `content/_index.md` |
| CV | `content/cv.md` (put a PDF at `static/cv.pdf`) |
| Links, email, Instagram | `hugo.toml` |
| Look and feel | `assets/style.css` |
| Jar warping effect | `assets/jar.js` |
| Page templates | `layouts/` |

## Publishing

Pushing to `main` runs `.github/workflows/hugo.yml`, which builds the site and deploys it.
One-time setup: in the repo go to **Settings → Pages → Source** and choose **GitHub Actions**.
