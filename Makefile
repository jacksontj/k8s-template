.PHONY: all
all: fmt compile

.PHONY: compile
compile:
	python3 compile.py

test:
	#python3 test.py
	find ./releases/*/release/ | grep json | xargs kubeval --exit-on-error --strict --kubernetes-version=1.16.3 --skip-kinds=CustomResourceDefinition,ClusterIssuer,Certificate,VolumeSnapshotClass

fmt:
	find . -name '*.jsonnet' | xargs jsonnetfmt -i
	find . -name '*.libsonnet' | xargs jsonnetfmt -i

fmt-test:
	find . -name '*.jsonnet' | xargs jsonnetfmt --test
	find . -name '*.libsonnet' | xargs jsonnetfmt --test

.PHONY: upload
upload:
	gsutil -m rsync -d -r ./releases/ gs://k8s-release-channels/
