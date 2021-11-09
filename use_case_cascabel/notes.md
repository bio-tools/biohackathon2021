# About 

Cascabel (https://doi.org/10.3389/fgene.2020.489357) is a variable pipeline for amplicon sequence data analysis. 

It makes an interesting use case for workflow work with bio.tools/EDAM and APE, as it already foresees several variants of the main workflow, and potentially more can be found when taking to account the full content of bio.tools.

Here we document the work on bringing it all together. 

# Tools

The tools used in Cascabel are listed in the figure/table at https://www.frontiersin.org/files/Articles/489357/fgene-11-489357-HTML/image_m/fgene-11-489357-t001.jpg

Custom scripts are obviously not available in bio.tools (here's the shim discussion again!), first assessment of the other tools listed: 

| **Tool**  | **in bio.tools?**  | **bio.tools ID**  | **functional annotation?**  |
|-----------|--------------------|-------------------|-----------------------------|
| FastQC | yes | biotools:fastqc | yes |
| PEAR | yes | biotools:pear | no |
| QIIME | yes | biotools:qiime | no |
| QIIME | yes | biotools:qiime2 | no |
| Mothur | no | - | - |
| usearch61 | no | - | - |
| VSEARCH | yes | biotools:vsearch | yes | 
| Cutadapt | yes | biotools:cutadapt | yes | 
| Cutadapt 1.12 | yes | biotools:cutadapt_1.12 | no |
| CD-HIT | yes | biotools:cd-hit | yes |
| SUMACLUST | no | - | - |
| Swarm | yes | biotools:swarm | yes |
| UCLUST | no | - | - | 
| trie | no | - | - |
| SortMeRna | yes | biotools:sortmerna | no |
| DADA2 | yes | biotools:dada2 | no | 
| BLAST | yes | biotools:blast | no |
| pynast | no | - | - |
| MAFFT | yes | biotools:MAFFT | yes | 
| Infernal | yes | biotools:infernal | yes | 
| ClustalW | yes | biotools:clustalw | yes | 
| MUSCLE | yes | biotools:muscle | yes | 
| RAxML | yes | biotools:raxml | no | 
| FastTree | yes | biotools:fasttree | no | 
| Krona | yes | biotools:krona | no | 

Next steps: 
* add the missing tools to bio.tools
* check and if necessary improve the functional annotations
* ...
* try to (re-)create the pipeline with APE (probably more steps needed before this works)









