#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts frontend-deployment.yaml