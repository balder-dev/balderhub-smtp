import datetime
from email.utils import parseaddr, parsedate_to_datetime
from email.message import Message as Em_Message
from typing import Optional, Union

from aiosmtpd.controller import Controller
import aiosmtpd.handlers

from balderhub.email.lib.utils import EmailDataMessage, EmailAddress, EmailHeader
from ..scenario_features.smtp_readable_server_feature import SmtpReadableServerFeature


class AiosmtpdServerFeature(SmtpReadableServerFeature):
    """SMTP server setup feature backed by the :mod:`aiosmtpd` library.

    The feature spins up a local :class:`aiosmtpd.controller.Controller` that listens on the
    host/port provided through :class:`SmtpServerConfig`. Every received message is parsed into an
    :class:`EmailDataMessage` and stored in an in-memory outbox that can be inspected from tests.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._controller: Union[Controller, None] = None

        self._msgs: list[SmtpReadableServerFeature.Message] = []

    @property
    def hostname(self) -> str:
        """
        :return: configured host name within the aiosmtpd server controller
        """
        return '0.0.0.0'

    @property
    def port(self) -> int:
        """
        :return: configured port within the aiosmtpd server controller
        """
        return 25

    @property
    def ready_timeout_sec(self):
        """
        :return: configured timeout within the aiosmtpd server controller
        """
        return 5

    def start(self):
        if self._controller is not None:
            raise ValueError('server is still active')

        this_obj = self

        class LogMessage(aiosmtpd.handlers.Message):
            """
            Internal :mod:`aiosmtpd` handler that converts received
            messages into :class:`EmailDataMessage` instances.
            """

            def handle_message(self, message: Em_Message) -> None:
                """Parse the incoming :class:`email.message.Message` and append it to the outbox."""
                from_name, from_addr = parseaddr(message.get('From', ''))
                from_address = EmailAddress(name=from_name, mail_address=from_addr)

                date_header = message.get('Date')
                if not date_header:
                    raise ValueError('did not receive date header')
                msg_date = parsedate_to_datetime(date_header)

                email_data_message = EmailDataMessage(from_address=from_address, date=msg_date)

                for key, val in message.items():
                    if key.lower() not in ('from', 'date'):
                        email_data_message.add_header(EmailHeader(key=key, value=val), allow_multiple=True)

                if message.is_multipart():
                    parts = []
                    for part in message.walk():
                        if part.get_content_type() == 'text/plain':
                            payload = part.get_payload(decode=True)
                            if payload:
                                parts.append(payload.decode(errors='replace'))
                    email_data_message.body_text = "\n".join(parts)
                else:
                    payload = message.get_payload(decode=True)
                    if payload:
                        email_data_message.body_text = payload.decode(errors='replace')
                    else:
                        email_data_message.body_text = str(message.get_payload())

                msg_obj = this_obj.Message(
                    mail=email_data_message,
                    received_timestamp=datetime.datetime.now(datetime.timezone.utc)
                )

                this_obj._msgs.append(msg_obj)  # pylint: disable=protected-access

        self._controller = Controller(
            LogMessage(),
            hostname=self.hostname,
            port=self.port,
            ready_timeout=self.ready_timeout_sec
        )
        self._controller.start()

    def shutdown(self):
        if self._controller is None:
            raise ValueError('server was already shut down')
        self._controller.stop()
        self._controller = None

    def is_running(self) -> bool:
        if self._controller is None:
            return False
        if self._controller.server is None:
            return False
        return hasattr(self._controller.server, "is_serving") and self._controller.server.is_serving()

    def get_outbox(self, for_mail_address: Optional[str] = None) -> list[SmtpReadableServerFeature.Message]:
        if for_mail_address is None:
            return self._msgs

        filtered = []
        for msg in self._msgs:
            if msg.mail.additional_headers is None:
                continue
            for header in msg.mail.additional_headers:
                if header.key.lower() == 'to' and for_mail_address in header.value:
                    filtered.append(msg)
                    break
        return filtered

    def clear_outbox(self):
        self._msgs = []
