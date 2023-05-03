.PHONY: all
all: fmt compile test

.PHONY: compile
compile:
	python3 compile.py

test:
	python3 test.py
	kubeconform --summary releases/*/release/*/

fmt:
	find . -name '*.jsonnet' | xargs jsonnetfmt -i
	find . -name '*.libsonnet' | xargs jsonnetfmt -i

fmt-test:
	find . -name '*.jsonnet' | xargs jsonnetfmt --test
	find . -name '*.libsonnet' | xargs jsonnetfmt --test

.PHONY: upload
upload:
	gsutil -m rsync -d -r ./releases/ gs://k8s-release-channels/
