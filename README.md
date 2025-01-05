# AWS Token Refresh Automation Guide (in terminal) 

I needed to write this because it is so annoying to each time refreshing my CLI aws tokens manually. Also I struggled hours in order to get the right steps by myself.
This small tuto explains how to manually but also programmatically refresh your cli aws tokens when needed as long as you remember your profile name (we get this after configuring the sso profile aka: aws configure sso).

I hope this could be helpful. It is up to date and I will be maintaing it at least for my own sake so you can trust that. If there is an issue do not hesitate to create an issue or contribute !


## Prerequisites
- AWS account setup (root and IAM/IAM identity)
- Basic AWS CLI configuration
- AWS SSO access

## The Token Refresh Challenge

When using AWS with GitHub Actions or other services, access tokens expire (typically after 1 hour), requiring manual refresh (At least that is what 
I was doing). Here is a simple solution I came with.

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
   - Start url (if you have you IAM identity account, you can easily get it)
   - Key ID
   - Access key
   - Session token

3. Click the provided authentication link to approve the connection

4. Use the profile:
   ```bash
   aws s3 ls --profile your-profile-name
   ```
This command will basically create a new json file in your local machine with the new credentials, so REALLLY IMPORTANT to type it!

### 3. Token Location
- For Ubuntu users: `~/.aws/cli/` (I am an Ubuntu user sorry the others, look for your own path...)
- Look for the most recent JSON configuration file
- Extract and update the required credentials

## Best Practices

1. Store credentials securely (preferably offline or in environment variables)
2. Keep basic configuration information easily accessible

## Automation

I have written a python script that does just what I explained here. you just have to type in terminal:

```bash
script.py --profile <profile-name>
```
replace <profile-name> with the last profile name you used to perform the previous the aws configure sso. Leave a Star if it helped you :-) 

## Author

anvix9 

