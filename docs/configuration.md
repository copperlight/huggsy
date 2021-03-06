## Introduction

This provides an overview of the configuration steps necessary to get the chatbot working.

## Chatbot Configuration Overview

* Create a Slack App.
* Create an AWS Lambda function.
* Attach an AWS API gateway to the function.
* Validate the Slack API challenge.

## Create a Slack App

* Slack API > Your Apps > Create New App > From Scratch
* App Name: Huggsy > Pick a workspace: $WORKSPACE > Create App
* Settings > Display Information > Basic Information
  * Display Information
    * App name: Huggsy
    * Short description: Your penguin pal!
    * App icon & Preview: <upload image from docs>
    * Background color: #2c2d30
  * Save Changes

## Configure Slack App Details, Tabs, OAuth Scopes and Event Subscriptions

* OAuth Scopes
    * Slack API > $BOT > Features > OAuth & Permissions > Scopes > Bot Token Scopes
        * app_mentions:read
        * channels:join
        * chat:write
        * commands
        * files:read
        * files:write
        * im:history
        * im:read
        * im:write
        * links:read
        * links:write
        * reactions:read
        * reactions:write
* OAuth Tokens for Your Workspace
  * Install to Workspace > Allow
  * Bot User OAuth Token > Copy
* Tabs
    * Slack API > $BOT > Features > App Home
      * Your App's Presence in Slack
        * Always Show My Bot as Online
      * Show Tabs
          * Messages Tab: Enabled
          * Allow users to send Slash commands and messages from the messages tab: Enabled
          * Requires Slack client restart.
* Slack API > $BOT > Features > Event Subscriptions
  * Enable Events: Enabled
     * Request URL: <AWS API Gateway URL>
     * With the challenge response handling built-in, the URL will verify immediately.
  * Subscribe to bot events
    * app_mention
    * message.im
  * Save Changes
* Reinstall App
  * Slack API > $BOT > Settings > Install App > Reinstall to Workspace

## Configure AWS Lambda Handler for Relative Imports

From [Lambda function handler in Python](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html):

> A function handler can be any name; however, the default name in the Lambda console is
`lambda_function.lambda_handler`. This function handler name reflects the function name
(`lambda_handler`) and the file where the handler code is stored (`lambda_function.py`).

To allow relative imports to be used in the Lambda function, we need to make it a module and adjust
the Handler name.

* AWS Lambda > $FUNCTION_NAME > Code > Runtime settings > Edit
    * Runtime settings > Handler > app.lambda_function.lambda_handler

## Configure AWS Deployment Credentials

* Create a new IAM user for deploying this Lambda function.
    * IAM > Add users
    * Set user details > User name: $USERNAME
    * Select AWS credential type: Access key - Programmatic access
    * Set permissions > Add user to group > Do not select a group
    * Next: Tags > Next: Review > Warning: This user has no permissions
    * Create user > Save the AWS access keys
* Grant the IAM user permission to deploy the function.
    * IAM > Users > $USERNAME > Add inline policy

            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "VisualEditor0",
                        "Effect": "Allow",
                        "Action": "lambda:UpdateFunctionCode",
                        "Resource": "arn:aws:lambda:$REGION:$ACCOUNT_ID:function:$FUNCTION_NAME"
                    }
                ]
            }

* On GitHub, add repository secrets which contain the AWS access keys.
    * Settings > Secrets > Actions > New repository secret
    * Also add a secret to set the region used for deployment.

## Configure Slack OAuth Token as Lambda Environment Variable

* Get the token
    * Slack API > $BOT > OAuth & Permissions > OAuth Tokens for Your Workspace > Bot User OAuth Token
* Store the token
    * AWS Lambda > $FUNCTION_NAME > Configuration > Environment variables > Edit > Add environment variable

This value is encrypted at rest.

## View AWS Lambda Logs

* AWS Lambda > $FUNCTION_NAME > Monitor > Logs > View logs in CloudWatch
