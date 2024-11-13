---
title: Applied Inverse Problems Conference (2023)

event: 11th Applied Inverse Problems Conference (2023)
event_url: http://www.aip2023.com/

location: Göttingen, Germany

summary: Constributed talk *Gradient Step and Proximal denoisers for convergent plug-and-play image restoration*

abstract: Plug-and-Play (PnP) methods constitute a class of iterative algorithms for imaging problems where regularization is performed by an off-the-shelf denoiser. Specifically, given an image dataset, optimizing a function (e.g. a neural network) to remove Gaussian noise is equivalent to approximating the gradient or the proximal operator of the log prior of the training dataset. Therefore, any off-the-shelf denoiser can be used as an implicit prior and inserted into an optimization scheme to restore images. The PnP and Regularization by Denoising (RED) frameworks provide a basis for this approach, for which various convergence analyses have been proposed in the literature. However, most existing results require either unverifiable or suboptimal hypotheses on the denoiser, or assume restrictive conditions on the parameters of the inverse problem. We will introduce the Gradient Step and Proximal denoisers, and their variants, recently proposed to restore RED and PnP algorithms to their original form as (nonconvex) real proximal splitting algorithms. These new algorithms are shown to converge towards stationary points of an explicit functional and to perform state-of-the-art image restoration, both quantitatively and qualitatively.

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: '2023-09-07'
#date_end: '2030-06-01T15:00:00Z'
all_day: true

# Schedule page publish date (NOT talk date).
# publishDate: '2017-01-01T00:00:00Z'

authors: []
tags: []

# Is this a featured talk? (true/false)
featured: false

links:
url_code: ''
url_pdf: ''
url_slides: ''
url_video: ''

# Markdown Slides (optional).
#   Associate this talk with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides: ""

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects:
---

<!-- {{% callout note %}}
Click on the **Slides** button above to view the built-in slides feature.
{{% /callout %}}

Slides can be added in a few ways:

- **Create** slides using Wowchemy's [_Slides_](https://wowchemy.com/docs/managing-content/#create-slides) feature and link using `slides` parameter in the front matter of the talk file
- **Upload** an existing slide deck to `static/` and link using `url_slides` parameter in the front matter of the talk file
- **Embed** your slides (e.g. Google Slides) or presentation video on this page using [shortcodes](https://wowchemy.com/docs/writing-markdown-latex/).

Further event details, including [page elements](https://wowchemy.com/docs/writing-markdown-latex/) such as image galleries, can be added to the body of this page. -->
