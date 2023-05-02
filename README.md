# k8s-template

This repository is aspiring to be a template for enterprise managment of k8s resources.


## Example topology

3 distinct accounts (dev, stage, prod) with 1 cluster per account.

## Design Principles

- All templating is done *prior* to the releases/ directory
	-- NOTE: this is a specific design choice to have the releases/ directory be exactly what is applied on a cluster
- This repository isn't opinionated about *how* the releases/ directory is applied (flux, argo, etc.)
