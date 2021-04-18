#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts create-configure-instances.yaml