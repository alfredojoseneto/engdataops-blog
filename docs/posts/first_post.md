---
date:
  created: 2026-01-26
  updated: 2026-01-26
description: "A brief description of your first blog post that will appear when shared on LinkedIn"
categories:
    - Tech
    - Lifestyle
slug: test-first-blog
tags:
  - lifestyle
authors:
  - alfredo
# readtime: 10
---

# My First Blog Post

This is the text for my firts blog post.


<!-- more -->

All the text here appears in the blog post.


### Example

```py title="scantree.py"
def scantree(path):
    for entry in os.scandir(path):
      if entry.isdir():
          yield from scantree(entry.path)
      else:
          entry
```