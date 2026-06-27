"""
===============================================================================
AWS IAM Access Review Automation
Author: Danielle Koppel

Purpose
-------
This project will become an automated AWS IAM access review tool.

Instead of manually clicking through the AWS Console, this program will collect
IAM evidence using AWS APIs and produce an audit-ready report.

Version 1 Goal
--------------
Verify that the Python environment is working correctly before I begin
communicating with AWS.
===============================================================================
"""
# -----------------------------------------------------------------------------
# Import the AWS SDK for Python.
#
# boto3 is Amazon's Software Development Kit (SDK) for Python.
# It allows our program to communicate with AWS services such as:
#
#   • IAM (Identity and Access Management)
#   • STS (Security Token Service)
#   • S3
#   • Lambda
#
# Think of boto3 as the translator between our Python code and AWS.
# -----------------------------------------------------------------------------

import boto3
#Import ClientError so I can handle AWS errors.
#Instead of the program crashing, it can display a helpful message.
from botocore.exceptions import ClientError

def list_iam_users():
    """
    Retrieve and display all IAM users.

    This is the first step of an access review because it establishes the
    inventory of identities that exist in the AWS account.
    """

    #Create a client that allows Python to communicate with AWS IAM service
    iam = boto3.client("iam")

    #Request a list of all IAM users in the AWS account
    response = iam.list_users()

    print("\nIAM Users:")

    #Loop through each IAM user returned by AWS
    for user in response["Users"]:

        #Display only the username instead of the entire response object
        print(f"- {user['UserName']}")

def main():
    """
    Main entry point for the program.

    Every Python application needs a place to begin. 
    By putting the starting logic inside a function mained 'main',
    the code stays organized and becomes easier to maintain as the project grows.
    """

    # ============================================================
    # Step 1: Create a connection to AWS Security Token Service (STS).
    #
    # STS provides information about the identity currently authenticated
    # with AWS.
    #
    # This is the same information I previously retrieved using:
    #
    #     aws sts get-caller-identity
    #
    # The difference is that now my Python program is making the API call.
    # ============================================================
    try:
        sts_client = boto3.client("sts")

        #Ask AWS who I am
        identity = sts_client.get_caller_identity()

        print("=" * 60)
        print("AWS CONNECTION SUCCESSFUL")
        print("=" * 60)

        print(f"Account : {identity['Account']}")
        print(f"ARN :{identity['Arn']}")
        print(f"User ID: {identity['UserId']}")

        # ============================================================
        # STEP 2: Retrieve all IAM users for the access review
        # ============================================================
        list_iam_users() 

    except ClientError as error:
        print("Unable to connect to AWS.")
        print(error)

if __name__ == "__main__":
    main()

iam = boto3.client("iam")

response = iam.list_users()

print("\nIAM Users:")
for user in response["Users"]:
    print(f"- {user['UserName']}")