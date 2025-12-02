FROM fedora:latest

RUN dnf install -y mock rpmdevtools dnf-plugins-core createrepo_c git && dnf clean all

RUN useradd -u 1000 -m -G mock builder

WORKDIR /src

USER builder
