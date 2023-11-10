# This is the base directory for this repo
BASE_DIR:=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: all
all: fmt compile test

.PHONY: compile
compile:
	tk env list --json | jq > lib/imported/environments.json
	@# we need to add a flag for `--merge-deleted-envs` for each env which is no longer present
	@# for now we're mashing this up in bash; but if this gets much more complex we may wrap
	@# this whole thing in a python script
	tk export -V 'rootDir=$(shell pwd)' releases environments/ --recursive --format '{{env.metadata.labels.cluster}}/{{if .metadata.namespace}}{{.metadata.namespace}}{{ else }}{{ if eq .kind "Namespace"}}{{.metadata.name}}{{ else }}global{{end}}{{end}}/{{.kind}}-{{.metadata.name}}' -c .cache --merge-strategy replace-envs $(shell ./scripts/missing_envs.py | sed 's/^/--merge-deleted-envs /')
	@# prune empty directories if we created any
	find releases/ -type d -empty -delete

.PHONY: vendor
vendor:
	@# re-run vendoring for helm-chars (ensure no local modifications)
	tk tool charts vendor --prune
	@# re-run vendoring for jsonnet bundler (ensure no local modifications)
	jb install

.PHONY: fmt
fmt:
	tk fmt .

.PHONY: test
test:
	@# Run our local python tests for ensuring policy has been met
	./scripts/test.py
	@# run kubeconform tests to ensure the manifests we have are valid
	kubeconform -schema-location default  -skip CustomResourceDefinition -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' releases/*/*

.PHONY: clean
clean:
	@# clean out the releases directory of any extraneous files
	git clean -dfx -- releases/
	@# reset any releases files to their upstream state
	git checkout releases/
	@# ensure that environments.json is *also* reset (since it is also generated)
	git checkout lib/imported/environments.json

.PHONY: clean-all
clean-all:
	git clean -dfx
	git checkout .

.PHONY: policy
policy:
	./scripts/policy_generate.py | tee .policy.yml
