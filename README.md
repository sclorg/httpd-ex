# S2I HTTPD Sample Application

This is a very basic sample application repository that can be built and deployed
on [OpenShift][https://www.openshift.com] using the [s2i httpd build image](https://github.com/sclorg/httpd-container).

The application serves a single static html page via httpd.

To build and run the application:

```
$ s2i build centos/httpd-24-centos7 https://github.com/openshift/httpd-ex myhttpdimage
$ docker run -p 8080:8080 myhttpdimage
$ curl localhost:8080
```

You can also build and deploy the application on OpenShift, assuming you have a
working `oc` command line environment connected to your cluster already:

`$ oc new-app centos/httpd-24-centos7~https://github.com/openshift/httpd-ex`

You can also deploy the sample template for the application:

`$ oc new-app -f https://raw.githubusercontent.com/openshift/httpd-ex/master/openshift/templates/httpd.json`