# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client



# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC4ccd7e15f30bc287ef5bb019cedd0c0a'
auth_token = '91b22def36f592eb2bef7c56eb62b237'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/welcome/voice/',
                        to='+16183504464',
                        from_='+5521995970551'
                    )

print(call.sid)

