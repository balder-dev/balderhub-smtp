Introduction into SMTP
**********************

SMTP (Simple Mail Transfer Protocol) is a communication protocol for electronic mail transmission. As an internet
standard, SMTP is primarily used by mail servers and other message transfer agents to send and receive mail messages.
User-level client mail applications typically use SMTP only for sending messages to a mail server for relaying.

While SMTP is used for the transmission of emails, protocols like IMAP or POP3 are traditionally used to retrieve them.
If you are looking for a complete email integration that also includes IMAP or POP3 retrieval functionalities, you should also take a look at the `balderhub-mail <https://docs.balder.dev/balderhub-mail>`_ package. This package builds upon SMTP and provides comprehensive features for handling both sending and receiving of emails.

In the context of the ``balderhub-smtp`` package, the focus is entirely on providing and utilizing SMTP 
functionalities, making it ideal for testing simple mail transmission and simulating an SMTP server.

SMTP was first defined in 1982 by `RFC 821 <https://datatracker.ietf.org/doc/html/rfc821>`_, and last updated in
2008 by `RFC 5321 <https://datatracker.ietf.org/doc/html/rfc5321>`_ to Extended SMTP additions, which is the protocol
variety in widespread use today. Mail servers use SMTP to send, receive, and relay outgoing mail between email
senders and receivers.

.. note::
    Coming more soon.

