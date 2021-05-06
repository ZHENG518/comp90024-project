#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts backend-deployment.yaml