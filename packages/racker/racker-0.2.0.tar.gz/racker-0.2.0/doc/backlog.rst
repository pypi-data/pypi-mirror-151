##############
Racker backlog
##############

.. note::

    Those are just random notes about ideas and more.


***********
Iteration 2
***********

- [x] Check if software tests can be invoked on CI/GHA.
- [x] Improve software tests.
- [x] Split functionality between ``racker`` and ``postroj``.

  - ``racker {run,ps,pull,logs}``
  - ``postroj {list-images,pkgprobe,selftest}``
  - ``pronto opensuse/tumbleweed hostnamectl`` (``pronto.hexagon`` (hx), ``pronto.kaxon`` (kx))

- [x] Continue renaming to ``racker``.
- [x] Improve error messages, see "Compatibility" section
  Compare with ``docker run --rm -it debian:bullseye-slim foo``.

  - ``racker run -it --rm debian-stretch hostnamectl``
  - ``racker run -it --rm debian-stretch /bin/hostnamectl``
  - ``racker run -it --rm debian-stretch /usr/bin/hostnamectl``

- [x] Provide more advanced and generic image (label) resolution.
  From docker.io, ghcr.io, registry.access.redhat.com, etc.
- [x] Improve documentation
- [x] Is it possible to run RHEL and SLES?

  - registry.access.redhat.com/rhel7/rhel
  - registry.suse.com/bci/bci-base
  - https://registry.suse.com/


***********
Iteration 3
***********

- [o] Tests: Wait for container to properly shut down before moving on.

  - Q: When running ``postroj selftest``, why is there more output from
    containers shutting down, while the program is finished already?
  - Q: Why are the tests failing when trying to subsequently spin up / tear down
    the same container?

- [o] Address issues in ``bugs.rst``

- [o] Invoke arbitrary Docker containers, even when they don't contain an OS root directory.

  - Directory ``/var/lib/postroj/archive/hello-world.img/rootfs`` doesn't look like an OS root directory (os-release file is missing). Refusing.
  - Directory ``/var/lib/postroj/archive/hello-world.img/rootfs`` doesn't look like it has an OS root directory. Refusing.
  - ``unshare --fork --pid --mount-proc --root=/var/lib/postroj/images/hello-world ./hello``

- [o] Use/integrate with ``mkosi``.

  - https://github.com/systemd/mkosi
  - http://0pointer.net/blog/mkosi-a-tool-for-generating-os-images.html
  - https://lwn.net/Articles/726655/
  - https://github.com/asiffer/netspot/search?q=mkosi

- [o] Improve timeout behaviors across the board,
  using ``with stopit.ThreadingTimeout(timeout) as to_ctx_mgr``.
- [o] Tests: ``racker pull foo``. Also remove ``/var/lib/postroj/archive/foo`` again.
- [o] No ``--boot`` / No ``umoci``?
- [o] Introduce ``postroj pull-dkr``
- [o] ``racker --verbose run -it --rm https://cloud-images.ubuntu.com/minimal/daily/focal/current/focal-minimal-cloudimg-amd64-root.tar.xz /bin/bash``
- [o] TODO: Introduce appropriate exception classes.
- [o] Maybe use ``ubi8/ubi-init`` instead of ``ubi8/ubi``?


***********
Iteration 4
***********

- [o] Test case currently does not tear down container?
- [o] Check using btrfs as container root.
- [o] Improve textual/logging output of probe details. Colors?
- [o] Check non-x64 architectures, maybe using Qemu and/or ``binfmt_misc``/``systemd-binfmt``.

  - https://en.wikipedia.org/wiki/Binfmt_misc
  - https://www.freedesktop.org/software/systemd/man/binfmt.d.html
  - https://www.freedesktop.org/software/systemd/man/systemd-binfmt.service.html
  - https://forums.raspberrypi.com/viewtopic.php?t=232417&start=100
  - https://github.com/sakaki-/raspbian-nspawn-64
  - https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-generic-arm64.tar.xz
  - ``podman run --arch arm64 'docker.io/alpine:latest' arch``
    https://wiki.archlinux.org/title/Podman

- [o] Improve README:

  - Point out some specific features and their use cases
  - ``racker pull`` as a successor to ``machinectl pull-dkr``.

- [o] Maybe don't *always* use the ``--pipe`` option, e.g. when installing packages.

    Console mode 'pipe' selected, but standard input/output are connected to an interactive TTY.
    Most likely you want to use 'interactive' console mode for proper interactivity and shell job
    control. Proceeding anyway.

- [o] Optionally force downloading and rebuilding rootfs images by using
  ``postroj pull --force``, re-triggering the ``skopeo`` and ``umoci`` steps.
- [o] Implement ``postroj logs``.
- [o] Accept packages from filesystem by using ``copy-to``.
  https://www.freedesktop.org/software/systemd/man/machinectl.html#copy-to%20NAME%20PATH%20%5BPATH%5D
- [o] Generalize package installation (is_debian vs. is_redhat vs. is_suse)
- [o] Implement ``racker compose``.

  - What about network isolation, host name assignment and resolution?
    - https://wiki.gnome.org/LubomirRintel/NMContainers
  - What about filesystem mounting?
    - https://fntlnz.wtf/post/systemd-nspawn/
  - Test on common Docker Compose configurations
    - https://github.com/bcremer/docker-telegraf-influx-grafana-stack

- [o] Improve HTTP probe request/response handling and verification.
  Q: Would it be possible to implement it completely in Python?
  E: Grafana responds with ``302 Found``, ``Location: /login``.


*************
Compatibility
*************

CLI interfaces
==============
- ``docker {run,ps,pull,logs}`` (implemented by ``racker``)
- ``docker compose`` (implemented by ``racker``)
- ``docker-py`` Python package (``import racker as docker; client = docker.from_env()``)
- Xen CLI ``xm``/``xl`` (implemented by ``hx`` or ``kx``)

Docker
======
Behaviour on error conditions.
::

    $ docker run --rm -it foo bash
    Unable to find image 'foo:latest' locally
    docker: Error response from daemon: pull access denied for foo, repository does not exist or may require 'docker login': denied: requested access to the resource is denied.
    See 'docker run --help'.

::

    $ docker run --rm -it debian:bullseye-slim foo
    docker: Error response from daemon: dial unix /Users/amo/Library/Containers/com.docker.docker/Data/docker.raw.sock: connect: connection refused.
    See 'docker run --help'.

::

    $ docker run --rm -it debian:bullseye-slim foo
    docker: Error response from daemon: failed to create shim: OCI runtime create failed: container_linux.go:380: starting container process caused: exec: "foo": executable file not found in $PATH: unknown.

::

    $ docker rmi debian:bullseye-slim
    bullseye-slim: Pulling from library/debian
    Status: Downloaded newer image for debian:bullseye-slim
    docker.io/library/debian:bullseye-slim

::

    $ docker pull debian:bullseye-slim
    bullseye-slim: Pulling from library/debian
    Digest: sha256:f75d8a3ac10acdaa9be6052ea5f28bcfa56015ff02298831994bd3e6d66f7e57
    Status: Image is up to date for debian:bullseye-slim
    docker.io/library/debian:bullseye-slim


Podman
======
- https://wiki.archlinux.org/title/Podman
- https://github.com/containers/podman
- https://podman.io/
- Podman + Buildah => systemd-nspawn + mkosi, controlled by racker

    Podman uses Buildah(1) internally to create container images. Both tools share
    image (not container) storage, hence each can use or manipulate images (but not
    containers) created by the other.

    -- https://docs.podman.io/en/latest/markdown/podman.1.html
    -- https://github.com/containers/buildah/blob/main/docs/buildah.1.md


API
===
- https://pypi.org/project/docker-compose/
- https://pypi.org/project/docker-pycreds/
- https://pypi.org/project/docker-py/
- https://pypi.org/project/docker/
- https://github.com/docker/docker-py/blob/master/tests/unit/client_test.py


*****
Ideas
*****

- [o] Look at Nspawn console
  - https://wiki.archlinux.org/title/getty#Nspawn_console
  - https://wiki.archlinux.org/title/Systemd#Change_default_target_to_boot_into

- [o] Look at systemd-firstboot

  - https://wiki.archlinux.org/title/Systemd-firstboot

- Currently, ``systemd-nspawn`` needs to be invoked as user ``root``.

  - Investigate *systemd-nspawn unprivileged mode* if that can improve the situation.
    https://www.reddit.com/r/archlinux/comments/ug1fwy/systemdnspawn_unprivileged_mode/
  - Check options ``--user`` / ``-U``.

- Make sure ``resolved`` is enabled on both the host and the guest.
  ``systemctl enable systemd-resolved``.
  Maybe this can get rid of bind-mounting the ``resolv.conf``, see
  ``--bind-ro=/etc/resolv.conf:/etc/resolv.conf``.

- Optionally install more software into machine image by default.
  ``apt-get install --yes procps iputils-ping netcat telnet iproute2 openssh-client wget curl``

- Use ``CacheDirectory=`` directive to cache download artefacts
- Build ``RootImage=``-compatible images, with GPT
- Integrate ``fpm``-based packaging code from Kotori
- Proposal: ``postroj create image`` vs. ``postroj create package``
- Check if "login prompt" unit can be deactivated when running with ``--boot``
- Check ``systemd-dissect``
- Boot ``.iso``
- Boot Xen guest, using either Hexagon, with ``hx``, or ``pronto``
- Add logging to journald
- Run system provisioning with Ansible
- How to crate and ship portable services?
  - https://github.com/asiffer/netspot/blob/v2.1.2/.github/workflows/systemd.yaml
  - https://github.com/asiffer/netspot/blob/v2.1.2/Makefile#L193-L203
- Provide web-based log tail like GHA and others, or even full access to the system.
  - wtee -- https://github.com/gvalkov/wtee
  - frontail -- https://github.com/mthenw/frontail
  - GoTTY -- https://github.com/yudai/gotty; https://jpmens.net/2022/05/03/one-gotty-per-user/
- Rebundle multiple microservice containers into groups, which are hosted on
  single OS containers.
