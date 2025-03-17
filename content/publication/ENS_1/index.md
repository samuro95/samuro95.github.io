---
title: 'From Denoising Score Matching to Langevin Sampling: A Fine-Grained Error Analysis in the Gaussian Setting'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin
  - Matthieu Terris
  - Thomas Moreau
  - Gabriel Peyré

# Author notes (optional)
author_notes:
  - 
  - 
date: '2025-03-14T00:00:00Z'
doi: ''

# Schedule page publish date (NOT publication's date).
publishDate: '2025-03-14T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['3']

# Publication name and optional abbreviated publication name.
publication:
publication_short:

abstract: Sampling from an unknown distribution, accessible only through discrete samples, is a fundamental problem at the core of generative AI. The current state-of-the-art methods follow a two-step process, first estimating the score function (the gradient of a smoothed log-distribution) and then applying a gradient-based sampling algorithm. The resulting distribution’s correctness can be impacted by several factors, the generalization error due to a finite number of initial samples, the error in score matching, and the diffusion error introduced by the sampling algorithm. In this paper, we analyze the sampling process in a simple yet representative setting—sampling from Gaussian distributions using a Langevin diffusion sampler. We provide a sharp analysis of the Wasserstein sampling error that arises from the multiple sources of error throughout the pipeline. This allows us to rigorously track how the anisotropy of the data distribution (encoded by its power spectrum) interacts with key parameters of the end-to-end sampling method, including the noise amplitude, the step sizes in both score matching and diffusion, and the number of initial samples. Notably, we show that the Wasserstein sampling error can be expressed as a kernel-type norm of the data power spectrum, where the specific kernel depends on the method parameters. This result provides a foundation for further analysis of the tradeoffs involved in optimizing sampling accuracy, such as adapting the noise amplitude to the choice of step sizes.


# Summary. An optional shortened abstract.
#summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere tellus ac convallis placerat. Proin tincidunt magna sed ex sollicitudin condimentum.

tags: []

# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

url_pdf: 'https://arxiv.org/pdf/2503.11615'
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
image:
  caption: ''
  focal_point: ''
  preview_only: true

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: []

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
slides: ""
---
