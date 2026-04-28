from typing import Optional

import smtplib
from email.message import EmailMessage
from email.utils import format_datetime

import balder

from balderhub.email.lib.utils import EmailDataMessage
from .. import scenario_features
from ..scenario_features import SmtpServerConfig


class SmtplibClientFeature(scenario_features.SmtpClientFeature):
    """SMTP client setup feature implemented on top of the standard :mod:`smtplib` module.

    The feature requires a connected ``SmtpServer`` :class:`balder.VDevice` exposing a
    :class:`SmtpServerConfig`, which provides the host/port the client should connect to.
    """

    class SmtpServer(balder.VDevice):
        """VDevice representing the SMTP server the client connects to."""
        config = SmtpServerConfig()

    def send_mail(
            self,
            message: EmailDataMessage,
            mail_from: Optional[str] = None,
            mail_to: Optional[list[str]] = None
    ):
        msg = EmailMessage()
        msg["Date"] = format_datetime(message.date)
        msg["From"] = message.from_address.to_string()

        for cur_header in message.additional_headers:
            msg[cur_header.key] = cur_header.value
        msg.set_content(message.body_text)

        with smtplib.SMTP(self.SmtpServer.config.host, self.SmtpServer.config.port) as server:
            server.send_message(msg, from_addr=mail_from, to_addrs=mail_to)
