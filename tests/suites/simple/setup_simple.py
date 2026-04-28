import balder
from balder import connections as cnn
from balderhub.smtp.lib.setup_features import SmtplibClientFeature

from tests.lib.setup_features.aiosmtpd_server_feature import AiosmtpdServerFeature
from tests.lib.setup_features.local_smtp_config import LocalSmtpConfig


class SetupSimple(balder.Setup):

    class Server(balder.Device):
        config = LocalSmtpConfig()
        server = AiosmtpdServerFeature()

    @balder.connect(Server, over_connection=cnn.SmtpConnection)
    class Client(balder.Device):
        client = SmtplibClientFeature(SmtpServer="Server")
