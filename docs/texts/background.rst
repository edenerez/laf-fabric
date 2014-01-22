Background
##########

What is LAF/GrAF
================
LAF/GrAF is a framework for representing linguistic source material plus associated annotations.
LAF, Linguistic Annotation Framework is an
ISO standard (`24612:2012 <http://www.iso.org/iso/catalogue_detail.htm?csnumber=37326>`_)
that describes the organization of the data.
GrAF, Graph Annotation Framework, is a set of
`schemas <http://www.xces.org/ns/GrAF/1.0/>`_ for the XML-annotations in a LAF resource.

Despite the L of linguistics, there is nothing particularly linguistic to LAF.
LAF describes data that comes as a linearly ordered *primary data* stream
(audio, video, text, or anything that has a one dimensional order), in which *regions* can be defined.
*Annotations* are key=value pairs or *feature structures* in general,
which conform to the joint definition of
`TEI Feature Structures <http://www.tei-c.org/release/doc/tei-p5-doc/en/html/FS.html>`_
and `ISO 24610 <http://www.iso.org/iso/catalogue_detail.htm?csnumber=37324>`_).
Between the primary data and the annotations is a *graph* of *nodes* and *edges*.
Some nodes are linked to regions of primary data.
Some nodes are linked to other nodes by means of edges.
An annotation may refer to a node or to an edge, but not both. 

So, features target the primary data through annotations.
Annotations can be labeled and they can be organized in *annotation spaces*.

.. _data:

Data
====
Although this tool is written to deal with LAF resources in general, it has been developed with a particular
LAF resource in mind:
the `Text database of the Hebrew Bible <http://www.dans.knaw.nl/en/content/categorieen/projecten/text-database-hebrew-old-testament>`_.
This data set is available (by request) from the national research data archive in the Netherlands, DANS,
by following this persistent identifier:
`urn:nbn:nl:ui:13-ukhm-eb <http://www.persistent-identifier.nl/?identifier=urn%3Anbn%3Anl%3Aui%3A13-ukhm-eb>`_.
This data is not yet in LAF format.
The `SHEBANQ <http://www.slideshare.net/dirkroorda/shebanq-gniezno>`_ project has
converted the database into LAF (the conversion code is in `GitHub project wivu2laf <https://github.com/dirkroorda/wivu2laf>`_),
and the resulting LAF resource is a file set of 2.27 GB, being predominantly linguistic annotations.
It is this LAF resource that is the reference context for LAF-Fabric.
It is to be deposited into the DANS archive shortly, under an Open Access licence, with the
restriction that it may not be used commercially. 

Existing tools for LAF/GrAF resources
=====================================
There is an interesting Python module
(`POIO, Graf-python <http://media.cidles.eu/poio/graf-python/>`_)
that can read generic GrAF resources.
It exposes an API to work with the graph and annotations of such resources.
However, when feeding it a resource with 430 k words and 2 GB of annotation material,
the performance is such that the graph does not fit into memory of a laptop.
Clearly, the tool has been developed for bunches of smaller GrAF documents,
and not for single documents with a half million words words and gigabytes of annotation material.

LAF-Fabric
==========
This program seeks to remedy that situation.
Its aim is to provide a framework on top of which you can write small Python scripts that
perform analytic tasks on big GrAF resources.
It achieves this goal by compiling xml into compact binary data, both on disk and in RAM and by
selective loading of features. The binary data loads very fast. Only selected features will be loaded,
and after loading they will be blown up into data structures that facilitate fast lookup of values.

With LAF-Fabric you can add an additional annotation package to the basic resource.
You can also switch easily between additional packages without any need for recompiling the basic resource.
The annotations in the extra package may define new annotation spaces, but they can
also declare themselves in the spaces that exist in the basic source.
Features in the extra annotation package that coincide with existent features, override the existent ones,
in the sense that for targets where they define a different value,
the one of the added annotation package is taken. Where the additional package does not provide values,
the original values are used.

With this device it becomes possible for you to include a set of corrections to the original features.
Or alternatively, you can include the results of your own work, whether manual or algorithmic or both,
with the original data. You can then do *what-if* research on the combination.

There are two example tasks that demonstrate this workflow.
With the :mod:`annox_create` task you can produce spreadsheets customized to the annotations that you
want to make. The same task can then transform your input into valid LAF annotations,
targeted at the pieces of primary data that you have specified in the spreadsheet.
The :mod:`annox_use` task shows you how you can use your annotations in analysis. 

Interactive notebooks
=====================
LAF-Fabric is designed to work within `iPython notebooks <http://ipython.org>`_.
That is a great environment to run tasks interactively, exploring the data as you go, and visualizing
your intermediate results at the moment they become available.
Last but not least, you can add documentation to notebooks and share them with your colleagues.
As an example, look at the
`gender notebook <http://nbviewer.ipython.org/github/dirkroorda/laf-fabric/blob/master/notebooks/gender.ipynb>`_
notebook by which you can draw a graph of the percentage of masculine and feminine
words in each chapter of the Hebrew Bible.

Rationale
=========
The paradigms for biblical research are becoming *data-driven*.
If you work in that field, you need increasingly sophisticated ways
to get qualitative and quantitative data out of your texts.
You, as a researcher, are in the best position to define what you need.
You can even fulfill those needs if you or someone else in your group
has basic programming experience.

LAF-Fabric is a stepping stone for teams in digital humanities to the wonderful world of computing.
With it you extract data from your resources of interest and feed it into your other tools.

See for example the notebook :mod:`cooccurrences`, also available as example
`notebook <http://nbviewer.ipython.org/github/dirkroorda/laf-fabric/blob/master/notebooks/cooccurrences.ipynb>`_,
which codes in less than a page an extraction of **data tables** relevant to the
study of linguistic variation in the Hebrew Bible.
These tables are suitable for subsequent data analysis
by means of the open source `statistics toolkit R <http://www.r-project.org>`_.

An other example is the task :mod:`proper`, which outputs a **visualization** of the text of the Hebrew Bible
in which the syntactic structure of the text is visible plus the the genders of all the proper nouns.
With this visualization it becomes possible to discern genealogies from other genres with the unaided eye,
even without being able to read a letter of Hebrew.

The code of LAF-Fabric is on
`github <https://github.com/dirkroorda/laf-fabric>`_,
including example notebooks, tasks and extra annotation packages.
You are invited to develop your own notebooks and share them,
either through data archives or directly through github,
or the `notebook viewer <http://nbviewer.ipython.org>`_.
In doing so, you (together) will create a truly state-of-the-art research tool,
adapted to your scholarly needs of analysis, review and publication.

Implementation highlights
=========================
There are several ideas involved in compiling a LAF resource into something
that is compact, fast loadable, and amenable to efficient computing.

#. Replace nodes and edges and regions by integers.
#. Store relationships between integers in *arrays*, that is, Python arrays.
#. Store relationships between integers and sets of integers also in *arrays*.
#. Keep individual features separate.
#. Compress data when writing it to disk.

**Everything is integer**
In LAF the pieces of data are heavily connected, and the expression of the connections are XML identifiers.
Besides that, absolutely everything gets an identifier, whether or not those identifiers are targeted or not.
In the compiled version we get rid of all XML identifiers.
We will represent everything that comes in great quantities by integers: regions, nodes, edges, feature values.
But feature names, annotation labels and annotation spaces will be kept as is.

**Relationships between integers as Python arrays**
In Python, an array is a C-like structure of memory slots of fixed size.
You do not have arrays of arrays, nor arrays with mixed types.
This makes array handling very efficient, especially loading data from disk and saving it to disk.
Moreover, the amount of space in memory needed is like in C, without the overhead a scripting language usually adds to its data types.

There is an other advantage:
a mapping normally consists of two columns of numbers, and numbers in the left column map to numbers in the right column.
In the case of arrays of integers, we can leave out the left column: it is the array index, and does not have to be stored.

**Relationships between integers as Python arrays**
If we want to map numbers to sets of numbers,
we need to be more tricky, because we cannot store sets of numbers as integers.
What we do instead is: we build two arrays, the first array points to data records in the second array.
A data record in the second array consists of a number giving the length of the record,
followed by that number of integers.
The function :func:`arrayify() <laf.model.arrayify>` takes a list of items and turns it in a double array. 

**Keep individual features separate**
A feature is a mapping from either nodes or edges to string values. Features are organized by the annotations
they occur in, since these annotations have a *label* and occur in an *annotation space*. 
We let features inherit the label and the space of their annotations. Within space and label, features are distinguished by name.
And the part of a feature that addresses edges is kept separate from the part that addresses nodes.

So an individual feature is identified by *annotation space*, *annotation label*, *feature name*, and *kind* (node or edge).
For example, in the Hebrew Bible data, we have the feature::

    shebanq:ft.suffix (node)

with annotation space ``shebanq``, annotation label ``ft``, feature name ``suffix``, and kind ``node``.
The data of this feature is a mapping that assigns a string value to each of more than 400,000 nodes.
So this individual feature represents a significant chunk of data.

The individual features together take up the bulk of the space.
In our example, they take 145 MB on disk, and the rest takes only 55 MB.
Most tasks require only a limited set of individual features.
So when we run tasks and switch between them, we want to swap feature data in
and out.
The design of LAF-fabric is such that feature data is neatly chunked per individual feature.

.. note::
    Here is the reason that we do not have an overall table for feature values, identified by integers.
    We miss some compression here, but with a global feature value mapping, we would burden every task with a significant
    amount of memory.
    Moreover, the functionality of extra annotation packages is easier to implement
    when individual features are cleanly separable.

.. note::
    Features coming from the source and features coming from the extra annotation package will be merged
    before the you can touch them in tasks.
    This merging occurs late in the process, even after the loading of features by LAF-fabric.
    Only at the point in time when a task declares the names of the API methods
    (see :meth:`API <laf.task.LafTask.API>`)
    the features will be assembled into objects.
    At this point the source features and annox features finally get merged.
    When a task no longer uses a merged feature, or want to merge with a different package,
    the feature data involved will be cleared, so that a fresh merger can take place.

.. _author:

Author
======
This work has been undertaken first in November 2013 by Dirk Roorda, working for
`Data Archiving and Networked Services (DANS) <http://www.dans.knaw.nl/en>`_ and
`The Language Archive (TLA) <http://tla.mpi.nl>`_.
The work has been triggered by the execution of the
`SHEBANQ <http://www.slideshare.net/dirkroorda/shebanq-gniezno>`_ project
(see `results <http://wivu2laf.readthedocs.org/en/latest/>`_)
together with the researchers Wido van Peursen, Oliver Glanz and Janet Dyk at the
`Eep Talstra Centre for Bible and Computing (ETCBC), VU University
<http://www.godgeleerdheid.vu.nl/nl/onderzoek/instituten-en-centra/eep-talstra-centre-for-bible-and-computer/index.asp>`_.

Thanks to Martijn Naaijer and Gino Kalkman for first experiments with LAF-Fabric.

History
=======

**2014-01-17**
Joint presentation with Martijn Naaijer at `CLIN <http://clin24.inl.nl>`_ (Computational Linguistics In the Netherlands).

**2013-12-18**
Demonstration on the `StandOff Markup and GrAF workshop (CLARIN-D) <http://cceh.uni-koeln.de/node/531>`_ in Köln.

**2013-12-12**
Demonstration for the `ETCBC <http://www.godgeleerdheid.vu.nl/etcbc>`_ team Amsterdam. Updated the 
`slides <http://www.slideshare.net/dirkroorda/work-28611072>`_.

**2013-12-09**
Abstract sent to `CLIN <http://clin24.inl.nl>`_ (Computational Linguistics In the Netherlands) accepted.
To be delivered 2014-01-17. 

**2013-11-26**
Vitamin Talk to the `TLA team Nijmegen <http://tla.mpi.nl>`_. Here are the
`slides <http://www.slideshare.net/dirkroorda/work-28611072>`_.
