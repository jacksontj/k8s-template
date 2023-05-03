# k8s-template

This repository is aspiring to be a template for enterprise managment of k8s resources.


## Build/Usage/Compilation Notes

- (1) Each cluster in `clusters/*.jsonnet` is built to determine the full set of clusters to build
- (2) for each cluster; all the apps (as linked in `ctx.Namespaces`) are compiled into a release directory (`releases/CLUSTERNAME/release`) with a kustomization.yaml
- (3) a set of tests are run against the output manifests

## Example topology

3 distinct accounts (dev, stage, prod) with 1 cluster per account.

## Design Principles

- All templating is done *prior* to the releases/ directory
	-- NOTE: this is a specific design choice to have the releases/ directory be exactly what is applied on a cluster
- This repository isn't opinionated about *how* the releases/ directory is applied (flux, argo, etc.)

## requirements
- jsonnet
- python-jsonnet
- python-yaml
- [kubeconform](https://github.com/yannh/kubeconform)
- [helm](https://helm.sh/docs/helm/helm_install/)
