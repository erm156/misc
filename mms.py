import os
import sys
from argparse import ArgumentParser

from twilio.rest import Client


def main():
    try:
        TWILIO_SID = os.environ['TWILIO_SID']
        TWILIO_AUTH = os.environ['TWILIO_AUTH']
        TWILIO_NUM = os.environ['TWILIO_NUM']
    except KeyError:
        print('Twilio API access not configured! Exiting...')
        sys.exit()

    parser = ArgumentParser()
    parser.add_argument('--url', type=str, required=True, help='multimedia url')
    parser.add_argument('--num', type=str, required=True, help='recipient number')
    parser.add_argument('--txt', type=str, help='optional body text')
    args = parser.parse_args()

    client = Client(TWILIO_SID, TWILIO_AUTH)
    client.api.account.messages.create(to=args.num,
                                    from_=TWILIO_NUM,
                                    body= args.txt or 'MMS via Python!',
                                    media_url=args.url)

if __name__ == '__main__':
    main()
