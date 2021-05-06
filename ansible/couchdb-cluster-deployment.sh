#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts couchdb-cluster-deployment.yaml