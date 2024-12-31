# Download Arxiv Papers
Python scripts to list or download papers or references from arXiv by author and/or title to the working directory. Search "Examples"
in the source code for usage. For example,

`python xdownload_papers_arxiv.py "Richardson" 5 "fortran"`

gives

```
=== arXiv PDF Downloader ===

Author Filter    : Richardson
Title Filter     : fortran
Number of PDFs   : 5

Searching arXiv with query: au:"Richardson" AND ti:"fortran"

Found 2 paper(s). Starting download...

[1] Downloading: The State of Fortran
    from: http://arxiv.org/pdf/2203.15110v2
    Saved as: richardson_the_state_of_fortran.pdf

[2] Downloading: Toward Modern Fortran Tooling and a Thriving Developer Community
    from: http://arxiv.org/pdf/2109.07382v1
    Saved as: richardson_toward_modern_fortran_tooling_and_a_thriving_developer_community.pdf

Download process completed.
```

`python xdownload_papers_arxiv.py "" 1000 "fortran"`

gives output starting with

```
=== arXiv PDF Downloader ===

Author Filter    : None
Title Filter     : fortran
Number of PDFs   : 1000

Searching arXiv with query: ti:"fortran"

Found 104 paper(s). Starting download...

[1] Downloading: Fortran2CPP: Automating Fortran-to-C++ Migration using LLMs via
  Multi-Turn Dialogue and Dual-Agent Integration
    from: http://arxiv.org/pdf/2412.19770v1
    Saved as: fortran2cpp__automating_fortran-to-c++_migration_using_llms_via_multi-turn_dialogue_and_dual-agent_integration.pdf

[2] Downloading: Portability of Fortran's `do concurrent' on GPUs
    from: http://arxiv.org/pdf/2408.07843v2
    Saved as: portability_of_fortran's_`do_concurrent'_on_gpus.pdf

[3] Downloading: Fully integrating the Flang Fortran compiler with standard MLIR
    from: http://arxiv.org/pdf/2409.18824v1
    Saved as: fully_integrating_the_flang_fortran_compiler_with_standard_mlir.pdf
...
```
The `xarxiv.py` script is more advanced and lets you find papers written by any or all of a list of authors, and it also prints abstracts with the `--abstract` flag.
The output of `python xarxiv.py "OR Kedward, Aradi, Certik, Curcic" 100 "fortran" --list --abstract` is

```
=== arXiv PDF Downloader and Formatter ===

Author Query     : OR Kedward, Aradi, Certik, Curcic
Title Filter     : fortran
Year Range       : None
Number of PDFs   : 100
Action           : List only with Abstracts

Searching arXiv with query: au:"Kedward" OR au:"Aradi" OR au:"Certik" OR au:"Curcic"
Title Filter: fortran

Found 4 paper(s) matching the criteria:

[1]  Title    : The State of Fortran
    Authors   : Laurence Kedward, Balint Aradi, Ondrej Certik, Milan Curcic, Sebastian Ehlert, Philipp Engel, Rohit Goswami, Michael Hirsch, Asdrubal Lozada-Blanco, Vincent Magnin, Arjen Markus, Emanuele Pagone, Ivan Pribec, Brad Richardson, Harris Snyder, John Urban, Jeremie Vandenplas
    Year      : 2022
    PDF Link  : http://arxiv.org/pdf/2203.15110v2
    Abstract  : A community of developers has formed to modernize the Fortran
                ecosystem. In this article, we describe the high-level features
                of Fortran that continue to make it a good choice for scientists
                and engineers in the 21st century. Ongoing efforts include the
                development of a Fortran standard library and package manager,
                the fostering of a friendly and welcoming online community,
                improved compiler support, and language feature development. The
                lessons learned are common across contemporary programming
                languages and help reduce the learning curve and increase
                adoption of Fortran.

[2]  Title    : Toward Modern Fortran Tooling and a Thriving Developer Community
    Authors   : Milan Curcic, Ondřej Čertík, Brad Richardson, Sebastian Ehlert, Laurence Kedward, Arjen Markus, Ivan Pribec, Jérémie Vandenplas
    Year      : 2021
    PDF Link  : http://arxiv.org/pdf/2109.07382v1
    Abstract  : Fortran is the oldest high-level programming language that
                remains in use today and is one of the dominant languages used
                for compute-intensive scientific and engineering applications.
                However, Fortran has not kept up with the modern software
                development practices and tooling in the internet era. As a
                consequence, the Fortran developer experience has diminished.
                Specifically, lack of a rich general-purpose library ecosystem,
                modern tools for building and packaging Fortran libraries and
                applications, and online learning resources, has made it
                difficult for Fortran to attract and retain new users. To
                address this problem, an open source community has formed on
                GitHub in 2019 and began to work on the initial set of core
                tools: a standard library, a build system and package manager,
                and a community-curated website for Fortran. In this paper we
                report on the progress to date and outline the next steps.

[3]  Title    : A Fortran-Keras Deep Learning Bridge for Scientific Computing
    Authors   : Jordan Ott, Mike Pritchard, Natalie Best, Erik Linstead, Milan Curcic, Pierre Baldi
    Year      : 2020
    PDF Link  : http://arxiv.org/pdf/2004.10652v2
    Abstract  : Implementing artificial neural networks is commonly achieved via
                high-level programming languages like Python and easy-to-use
                deep learning libraries like Keras. These software libraries
                come pre-loaded with a variety of network architectures, provide
                autodifferentiation, and support GPUs for fast and efficient
                computation. As a result, a deep learning practitioner will
                favor training a neural network model in Python, where these
                tools are readily available. However, many large-scale
                scientific computation projects are written in Fortran, making
                it difficult to integrate with modern deep learning methods. To
                alleviate this problem, we introduce a software library, the
                Fortran-Keras Bridge (FKB). This two-way bridge connects
                environments where deep learning resources are plentiful, with
                those where they are scarce. The paper describes several unique
                features offered by FKB, such as customizable layers, loss
                functions, and network ensembles. The paper concludes with a
                case study that applies FKB to address open questions about the
                robustness of an experimental approach to global climate
                simulation, in which subgrid physics are outsourced to deep
                neural network emulators. In this context, FKB enables a
                hyperparameter search of one hundred plus candidate models of
                subgrid cloud and radiation physics, initially implemented in
                Keras, to be transferred and used in Fortran. Such a process
                allows the model's emergent behavior to be assessed, i.e. when
                fit imperfections are coupled to explicit planetary-scale fluid
                dynamics. The results reveal a previously unrecognized strong
                relationship between offline validation error and online
                performance, in which the choice of optimizer proves
                unexpectedly critical. This reveals many neural network
                architectures that produce considerable improvements in
                stability including some with reduced error, for an especially
                challenging training dataset.

[4]  Title    : A parallel Fortran framework for neural networks and deep
                learning
    Authors   : Milan Curcic
    Year      : 2019
    PDF Link  : http://arxiv.org/pdf/1902.06714v2
    Abstract  : This paper describes neural-fortran, a parallel Fortran
                framework for neural networks and deep learning. It features a
                simple interface to construct feed-forward neural networks of
                arbitrary structure and size, several activation functions, and
                stochastic gradient descent as the default optimization
                algorithm. Neural-fortran also leverages the Fortran 2018
                standard collective subroutines to achieve data-based
                parallelism on shared- or distributed-memory machines. First, I
                describe the implementation of neural networks with Fortran
                derived types, whole-array arithmetic, and collective sum and
                broadcast operations to achieve parallelism. Second, I
                demonstrate the use of neural-fortran in an example of
                recognizing hand-written digits from images. Finally, I evaluate
                the computational performance in both serial and parallel modes.
                Ease of use and computational performance are similar to an
                existing popular machine learning framework, making neural-
                fortran a viable candidate for further development and use in
                production.

Process completed.
```
