DNADNA Changelog
================

1.0.0rc1 (16-05-2022)
---------------------

### Enhancements

* Batch size can be customized when running `dnadna predict` (!140)

* SNP matrices are no longer forced to be unsigned 8-bit integers, but
  are allowed to be in principle any numeric data type that can converted
  to floats (!154)

* New syntax in config files for completely overriding inherited sections,
  rather than merging with them (!157)

### Bug fixes

* When running `dnadna predict` on an existing file it is appended to
  without writing a new header (!134)

* Fixed bug in resolution of relative paths in config files when they are
  inherited from another config file (!135)

* Fixed bug where custom network parameters in the network configuration
  sometimes failed validation.  Added better logging of inferred network
  params (!137)

* Fixed possible performance defect when running prediction due to acciental
  use of `np.ext()` on `Tensor` objects (!139)

* Fixed crash that could occur in `dnadna preprocess` when some replicates
  are missing from the dataset (!141)

* Fixed crash when running `dnadna train` on a purely classification task
  (!147)

* Fixed support for PyTorch 1.10+ (!153)

### Misc

* The `dnadna init` command now *requires* a model name argument, and does
  not take a default name from the dataset name (!136)

* Added new dependency on `jsonschema-pyref` which allowed removing some of
  the more complicated and bug-prone code for validation of complex
  schemas (!144)

* Installation of tensorboard is now optional (!149)

* Various documentation improvements.
