---
sidebar_position: 3

---

# Gmail Integration for Sales Agent

Our sales agent can now send emails using Gmail. To enable this functionality, you need to set up the necessary environment variables in your system.

## Setting up Environment Variables

You need to configure two environment variables to use the Gmail integration:

1. `GMAIL_MAIL`: This should be set to the Gmail address you want to use for sending emails.
2. `GMAIL_APP_PASSWORD`: This is a special password that allows third-party applications to access your Gmail account securely.

### How to Create an App Password

To create an App Password, follow these steps:

1. Create a Google account or use an existing one.
2. Enable 2-factor authentication on your Google account. This is a prerequisite for creating an App Password.
3. Once 2-factor authentication is enabled, go to [Google App Passwords](http://myaccount.google.com/apppasswords).
4. In the App Passwords page, select the app and device you want to generate the password for and then generate the password.
5. Use the generated password as the value for `GMAIL_APP_PASSWORD` in your environment variables.

By setting these environment variables correctly, the sales agent will be able to send emails using the specified Gmail account.
![Is this setup correctly?](/img/Gmail.png)

This screenshot demonstrates the Gmail tool in action, showcasing how the sales agent can seamlessly integrate and utilize Gmail for email communications directly from the platform.


