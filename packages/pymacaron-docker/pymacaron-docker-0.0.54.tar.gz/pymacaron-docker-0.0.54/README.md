# pymacaron-docker

Tools for packaging a PyMacaron microservice as a Docker image.

See more at [pymacaron.com](http://pymacaron.com/deploy.html)


## Generating a new pymacaron/base image

To generate a new pymacaron/base image, run:

```
./bin/pymdockerbase --push
```

By default, the generated new base image gets tagged with a version number
generated from today's date and the commit number.

You can see available [pymacaron base images here](https://hub.docker.com/repository/docker/pymacaron/base).

To give the most recent image the 'stable' tag, do:

* First make sure the image is indeed stable by using it as the base image to various pymacaron services for a while

* Then give it the stable tag and push back to docker.io:

```
docker pull pymacaron/base:<LATEST_VERSION>
docker tag pymacaron/base:<LATEST_VERSION> pymacaron/base:stable
# Optionally: do 'docker login'
docker push pymacaron/base:stable
```

## bin/pymdocker

Build a pymacaron docker image and/or push it to a docker repository. For
details:

```
pymdocker --help
```


## Author

Erwan Lemonnier<br/>
[github.com/pymacaron](https://github.com/pymacaron)</br>
[github.com/erwan-lemonnier](https://github.com/erwan-lemonnier)<br/>
[www.linkedin.com/in/erwan-lemonnier/](https://www.linkedin.com/in/erwan-lemonnier/)