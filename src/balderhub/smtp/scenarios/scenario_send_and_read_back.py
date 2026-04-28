import logging
import datetime

import balder
from balder import connections as cnn
from balderhub.smtp.lib.scenario_features import SmtpClientFeature, SmtpReadableServerFeature
from balderhub.email.lib.utils import EmailDataMessage, EmailAddress



logger = logging.getLogger(__name__)


class ScenarioSendAndReadBack(balder.Scenario):
    """Scenario that sends a mail through an SMTP client and verifies it was received by the server.

    The scenario consists of a :class:`Server` device exposing a :class:`SmtpReadableServerFeature` and a
    :class:`Client` device exposing an :class:`SmtpClientFeature`. Both devices are connected via an
    SMTP connection. Each test case starts with a freshly rebooted server and an empty outbox.
    """

    class Server(balder.Device):
        """Device representing the SMTP server."""
        server = SmtpReadableServerFeature()

    @balder.connect(Server, over_connection=cnn.SmtpConnection)  # pylint: disable=undefined-variable
    class Client(balder.Device):
        """Device representing the SMTP client used to send mails to :class:`Server`."""
        client = SmtpClientFeature()

    @balder.fixture('testcase')
    def restart_smtp_server(self):
        """Test-case fixture that restarts the SMTP server and clears its outbox before each test."""
        yield from self.Server.server.fixt_reboot_and_clear_outbox()

    def test_send_mail_and_read_back(self):
        """Send a single email from the client and assert that the server receives an equivalent message."""
        mail_to_send = EmailDataMessage(
            from_address=EmailAddress(name="Mr Example", mail_address="example@example.com"),
            date=datetime.datetime.now().replace(microsecond=0),
        )
        mail_to_send.add_to_addresses(EmailAddress(name='Receiver', mail_address="receiver@example.com"))
        mail_to_send.add_subject("Hello World")
        mail_to_send.body_text = "Hello My Friend\r\nThis text is from Body.\r\nBye\r\n"

        logger.info("make sure that there are no messages received yet")
        outbox = self.Server.server.get_outbox()
        assert not outbox, f"saw some messages before mail was sent: {outbox}"

        logger.info("send new message")
        self.Client.client.send_mail(mail_to_send)
        logger.info("- message sent")

        logger.info("make sure that new message has been received")
        outbox = self.Server.server.get_outbox()
        assert len(outbox) == 1, f"detect unexpected state of outbox: {outbox}"
        assert mail_to_send.compare(outbox[0].mail, ignore_added_headers=True), \
            (f"different mail received than the one that was sent "
             f"- sent mail was `{mail_to_send}`, but received mail `{outbox[0].mail}`")
