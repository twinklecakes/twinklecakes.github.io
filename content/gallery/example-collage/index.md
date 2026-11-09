---
title: "Example collage"
date: 2026-11-08
cover: "cover.jpg"     # this image goes in the jar on the gallery shelf
draft: true            # drafts only show with `hugo server -D`; delete this folder when you add real work
---

A few lines about the piece, if you want them. You can skip writing completely.

{{< collage >}}
![first detail](detail-1.jpg)
![second detail](detail-2.jpg)
{{< /collage >}}

A video works the same way. Put `clip.mp4` in this folder and write:

    {{</* video src="clip.mp4" */>}}

For YouTube or Vimeo: `{{</* youtube VIDEO_ID */>}}` or `{{</* vimeo VIDEO_ID */>}}`.
