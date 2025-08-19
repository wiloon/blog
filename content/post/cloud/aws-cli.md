---
title: aws-cli
author: "-"
date: 2014-02-24T06:44:56+00:00
url: aws-cli
categories:
  - Cloud
tags:
  - aws

---
## aws-cli

## install

```bash
# archlinux
pacman -Sy aws-cli

# macos
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```

aws console> iam> user> w10n_ec2>create access key> cli>

## commands

```bash
aws configure

# default region name: ap-southeast-1
# default output format: json

cat ~/.aws/credentials
cat ~/.aws/config

aws ec2 describe-instances --instance-ids i-xxxxxxxxxxxxxxxxx --query 'Reservations[*].Instances[*].{ID:InstanceId,State:State.Name}' --output table
```
