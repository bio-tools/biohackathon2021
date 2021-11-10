---
title: 'Making bio.tools fit for workflows'
title_short: 'Making bio.tools fit for workflows'
tags:
  - scientific workflows
  - computational pipelines
  - bio.tools
  - EDAM
  - APE
authors:
  - name: Anna-Lena Lamprecht
    orcid: 0000-0003-1953-5606
    affiliation: 1
  - name: another author
    orcid: 0000-0000-0000-0000
    affiliation: 2
affiliations:
  - name: Dept. of Information and Computing Sciences, Utrecht University, Netherlands
    index: 1
  - name: another affiliation
    index: 2
date: 9 November 2021
bibliography: paper.bib
event: BioHackathon Europe 2021
biohackathon_name: "BioHackathon Europe 2021"
biohackathon_url:   "https://biohackathon-europe.org/"
biohackathon_location: "Barcelona, Spain, 2021"
group: 22
# URL to project git repo --- should contain paper.md
git_url: https://github.com/bio-tools/biohackathon2021/
# This is the short authors description that is used at the
# bottom of the generated paper.
authors_short: TBD \emph{et al.}
---

<!--

The paper.md, bibtex and figure file can be found in this repo:

  https://github.com/journal-of-research-objects/Example-BioHackrXiv-Paper

To modify, please clone the repo. You can generate PDF of the paper by
pasting above link (or yours) in

  http://biohackrxiv.genenetwork.org/

-->

# Introduction

With 20.000+ entries, bio.tools is a major registry of computational tools in the life sciences. During the [2020 European BioHackathon](https://biohackathon-europe.org/), the project "Making bio.tools fit for workflows" was run to  address two urgent needs of the platform:

1. Slicing the bio.tools content through specialisation and categorisation, to improve exposure to communities and to present useful content for the users. The main challenge is to summarise relevant information from the wealth of annotation categories in bio.tools and metrics from external sources. Therefore we aim to enrich tools, communities and collections with statistics and metrics that summarise functionality, impact and annotation quality. These metrics and statistics are valuable resources for tool-building communities, scientific domains, individual scientific tool repositories and groups specialising in technical features. With that information, we can identify, calculate and integrate metrics relevant for the bio.tools registry. In addition we will devise a mock-up / alpha version summary stats page within bio.tools.

2. Improving the quality of functional tool annotations, to enable automated composition of individual tools into multi-step computational pipelines or workflows. Currently, tool annotations are often incomplete or imprecise, hampering plug&play workflow composition. We will develop a protocol for improving functional tool annotations in bio.tools. It will be based on 1) selecting reference workflows from workflow repositories and literature, 2) trying to recreate them using bio.tools and the Automated Pipeline Explorer, 3) comparing automatically created and reference workflows, and 4) if necessary revising the tool annotations until recreation succeeds. Workshop participants will perform this process and concurrently develop the tooling and documentation to enable its application to additional workflows after the hackathon.

The outcomes of this project will make software more findable and provide a solid basis for iteratively improving the quality of functional annotations in bio.tools, making it an increasingly powerful source of new fit-for-purpose workflows.

In this document we document the progress towards these goals that was made during the BioHackathon 

# Hacking Activities and Outcomes

## bio.tools Stats and Figures

(please add content here)

## bio.tools Annotation Quality

(please add content here)

## ...

## Use Case: The Cascabel Pipeline

Based on [@cascabel], content to be added


# Discussion

...

## Acknowledgements

We thank the organizers of the BioHackathon Europe 2021 for travel support for some of the authors.

## References
