TAG :=		$(shell awk '/ENV SNORT_VERSION/ { print $$3 }' Dockerfile)
IMAGE :=	jasonish/snort

all:
	docker build -t $(IMAGE) .
	docker run --rm $(IMAGE) snort -V
	docker tag $(IMAGE) $(IMAGE):latest
	docker tag $(IMAGE) $(IMAGE):$(TAG)

clean:
	rm -f *~
