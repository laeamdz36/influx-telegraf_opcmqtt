FROM telegraf:1.36.3

# Set file capability on the binary so non-root user can use raw ICMP sockets
# This avoids running the container as root at runtime
RUN setcap cap_net_raw=eip /usr/bin/telegraf

USER 1000
