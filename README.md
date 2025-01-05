# AWS Token Refresh Automation Guide (in terminal)

A practical guide for managing AWS CLI token refresh, both manually and programmatically.

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [The Token Refresh Challenge](#the-token-refresh-challenge)
4. [Manual Token Refresh Process](#manual-token-refresh-process)
   - [Check Token Status](#1-check-token-status)
   - [Refresh Process](#2-refresh-process)
   - [Token Location](#3-token-location)
5. [Best Practices](#best-practices)
6. [Automation](#automation)
7. [Author](#author)

## Introduction
I needed to write this because it is so annoying to each time refresh my CLI aws tokens manually. Also, I struggled hours to get the right steps by myself.

This small tutorial explains how to manually but also programmatically refresh your CLI aws tokens when needed, as long as you remember your profile name (we get this after configuring the sso profile aka: aws configure sso).

I hope this could be helpful. It is up to date and I will be maintaining it at least for my own sake so you can trust that. If there is an issue do not hesitate to create an issue or contribute!

## Prerequisites
- AWS account setup (root and IAM/IAM identity)
- Basic AWS CLI configuration
- AWS SSO access

## The Token Refresh Challenge
When using AWS with GitHub Actions or other services, access tokens expire (typically after 1 hour), requiring manual refresh (At least that is what I was doing). Here is a simple solution I came with.

## Manual Token Refresh Process

### 1. Check Token Status
To verify if your session has expired:
```bash
aws sts get-caller-identity --profile <profile-name>
```
If expired, you'll see:
```
... The security token included in the request is expired
```
Or close to that...

### 2. Refresh Process
1. Run the SSO configuration:
   ```bash
   aws configure sso
   ```
2. Follow the prompts and provide:
   - Start url (if you have your IAM identity account, you can easily get it)
   - Key ID
   - Access key
   - Session token

3. Click the provided authentication link to approve the connection

4. Use the profile:
   ```bash
   aws s3 ls --profile your-profile-name
   ```
This command will basically create a new json file in your local machine with the new credentials, so REALLY IMPORTANT to type it!

### 3. Token Location
- For Ubuntu users: `~/.aws/cli/` (I am an Ubuntu user sorry the others, look for your own path...)
- Look for the most recent JSON configuration file
- Extract and update the required credentials

## Best Practices

Keep basic configuration information easily accessible. (I do that by storing them in a flash drive or env_variable but I still put it somewhere)

## Automation
I have written a python script that does just what I explained here. You just have to type in terminal:
```bash
script.py --profile <profile-name>
```
Replace `<profile-name>` with the last profile name you used to perform the previous aws configure sso. Leave a Star if it helped you :-)

## Author
anvix9
