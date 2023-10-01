# Google Summer of Code Final Work Submission

This is a COPY of the PolyGlot repository, meant to isolate all Google Summer of Code related commits (from June 2023 to September 2023). To see the active PolyGlot repository, click here: [https://github.com/PolyPhyHub/PolyGlot](https://github.com/PolyPhyHub/PolyGlot).


In addition, I have uploaded .py files containing the code used for preprocessing Lautonomy's data. The original work was done on Google Colab, but to hide outputs and protect their original dataset, I have uploaded the code as a set of .py files. Nonetheless, seeing the code itself may be useful to others curious about Polyglot. Open the "GSoC_Lautonomy_Colab_Code" folder to access them. However, the code used in developing the timeline feature is displayed in its original notebook for anyone curious about the methodology behind the timeline feature. 

# Background
In this project, we sought to extend the Polyglot web app, as developed by [Hongwei (Henry) Zhou](https://normand-1024.github.io). For context, the web app follows this methodology:
1. Given a set of words, use an embedding model (such as Word2Vec, BERT, etc.) to generate a set of high dimensional points associated with each word.
2. Use a dimensionality reduction method (such as UMAP) to reduce the dimensionality of each word-vector point to 3 dimensions
3. Use the novel MCPM (Monte Carlo Physarum Machine) to compute the similarities between a set of anchor points and the rest of the point cloud.
4. The web app then displays the point cloud of 3-dimensional embeddings, but uses coloring to indicate the level of MCPM similarity each word has with the anchor point (e.g, if the anchor point is the word “dog”, the rest of the point cloud is colored such that words identified as similar to “dog” by the MCPM metric are brighter, whereas dissimilar words are darker.

# GSoC Results
The main results are summarized as follows:
1. New fuzzy-text search bar and “jump to point” feature for smoother navigation
[![](gsoc_images/search_feat.png)](gsoc_images/search_feat.png)
*Search feature. The point we have jumped to is highlighted in green.*

3. New annotation feature for coloring and making notes on subsections of the point cloud (+ ability to export annotations). A brush size selector is available and annotations can be deleted.
[![](gsoc_images/annotat_feat.png)](gsoc_images/annotat_feat.png)
*Annotation feature. The annotated points are in green.*

5. Novel timeline feature in which users can track the importance of certain words over time by watching the change in size of points (computes the IF-IDF metric for a word across all documents in a given year). Uses linear interpolation for years which do not have an explicit importance score.
[![](gsoc_images/timeline_feat.png)](gsoc_images/timeline_feat.png)
*Timeline feature. Yellow points are those for which timeline importance is computed. Size is relative to importance.*

3. Run time improvements, a grayscale mode
[![](gsoc_images/grascale_feat.png)](gsoc_images/grascale_feat.png)
  
4. An industrial collaboration with UK startup Lautonomy, where we have pre-processed and entered their data into Polyglot
[![](gsoc_images/lautonomy_data.png)](gsoc_images/lautonomy_data.png)
*Preview of Lautonomy’s data. Coloring is based on the 3D Euclidean metric (hence the radial coloring). Data not visible in public repo.*


# Future work
Future work will focus on automating the pre-processing pipeline (including data cleaning, computing embedding, dimensionality reduction, and  similarity metric computation), as this is quite labour intensive. In particular, we hope to automate the usage of the MCPM metric in Polyglot by adding to the PolyPhy package. We also hope to add more exploratory features relating to the word-document relationship. The collaboration with Lautonomy is ongoing and we hope to release a final output soon. Finally, we hope to expand the community around Polyglot by increasing its number of users and by seeking out others looking to contribute to its development.

## Authors

This web visualization tool was originally created by a team of researchers at University of California, Santa Cruz, Dept. of Computational Media:

- [Hongwei (Henry) Zhou](https://normand-1024.github.io/)
- [Oskar Elek](https://elek.pub/)
- [Angus G. Forbes](https://creativecoding.soe.ucsc.edu/angus/)

The original work was published as Hongwei Zhou's [M.S. thesis](https://escholarship.org/uc/item/6zj1r9ch#main).

A version of this original work was published in [2020 IEEE 5th Workshop on Visualization for the Digital Humanities (VIS4DH)](https://www.computer.org/csdl/proceedings-article/vis4dh/2020/915300a007/1pZ0Xs0EEqk)

This tool was later extended as part of Kiran Deol's 2023 Google Summer of Code project, mentored by [Oskar Elek](http://elek.pub) and [Jasmine Otto](https://jazztap.github.io).
