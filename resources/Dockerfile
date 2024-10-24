FROM registry.redhat.io/amq-streams/kafka-37-rhel9:2.7.0-19
USER root:root
RUN dnf --setopt=tsflags=nodocs --setopt=install_weak_deps=0 upgrade -y \
    && dnf autoremove -y \
    && dnf clean all \
    && rm -rf /var/cache/yum
COPY ./connect-plugins/ /opt/kafka/plugins/
USER 1001
