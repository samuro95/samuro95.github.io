---
title: 'A relaxed proximal gradient descent algorithm for convergent plug-and-play with proximal denoiser'

# Authors
# If you created a profile for a user (e.g. the default `admin` user), write the username (folder name) here
# and it will be replaced with their full name and linked to their profile.
authors:
  - admin
  - Antonin Chambolle
  - Arthur Leclaire
  - Nicolas Papadakis

# Author notes (optional)
author_notes:
  - 
  - 
date: '2024-06-12T00:00:00Z'
doi: ''

# Schedule page publish date (NOT publication's date).
publishDate: '2024-06-12T00:00:00Z'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['2']

# Publication name and optional abbreviated publication name.
publication: In * Journal of Mathematical Imaging and Vision*
publication_short: In *JMIV*

abstract: In this work, we present new proofs of convergence for plug-and-play (PnP) algorithms. PnP methods are efficient iterative algorithms for solving image inverse problems where regularization is performed by plugging a pre-trained denoiser in a proximal algorithm, such as Proximal Gradient Descent (PGD) or Douglas–Rachford splitting (DRS). Recent research has explored convergence by incorporating a denoiser that writes exactly as a proximal operator. However, in these works, the corresponding PnP algorithm has the drawback to be necessarily run with stepsize equal to 1. The stepsize condition for nonconvex convergence of the proximal algorithm in use then translates to restrictive conditions on the regularization parameter of the inverse problem. This can severely degrade the restoration capacity of the algorithm. In this paper, we present two remedies for this limitation. First, we provide a novel convergence proof for PnP-DRS that does not impose any restriction on the regularization parameter. Second, we examine a relaxed version of the PGD algorithm that converges across a broader range of regularization parameters. Our experimental study, conducted on deblurring and super-resolution experiments, demonstrate that these two solutions both enhance the accuracy of image restoration.


# Summary. An optional shortened abstract.
#summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere tellus ac convallis placerat. Proin tincidunt magna sed ex sollicitudin condimentum.

tags: []

# Display this page in the Featured widget?
featured: true

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

url_pdf: 'https://arxiv.org/pdf/2311.01216'
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
