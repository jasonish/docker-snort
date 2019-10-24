TAG :=		$(shell awk '/ENV SNORT_VERSION/ { print $$3 }' Dockerfile)
NAME ?=		jasonish/snort

all:
	docker build -t $(NAME) .
	docker run --rm $(NAME) snort -V
	docker tag $(NAME) $(NAME):latest
	docker tag $(NAME) $(NAME):$(TAG)

push:
	docker push $(NAME):latest
	docker push $(NAME):$(TAG)

clean:
	rm -f *~
