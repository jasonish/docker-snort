VERSION :=	2.9.8.3
TAG :=		jasonish/snort

all:
	docker build -t $(TAG) .
