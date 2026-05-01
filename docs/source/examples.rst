Examples
********

This package can be used to work with SMTP servers or for all kind of test that need a simple simulated SMTP server.


Simulating an SMTP Server
=========================

If you want to write test, but a smtp server is needed, that can be read by the tests, you can use the following
features.


.. code-block:: python

    import balder
    from tests.lib.setup_features import AiosmtpdServerFeature


    class SetupSimple(balder.Setup):

        ...

        class SmtpServer(balder.Device):
            server = AiosmtpdServerFeature()

        ...

Many scenarios use the :class:`balderhub.email.lib.scenario_features.EmailReaderFeature`. This package provides
implementations for this feature without the need to set up IMAP/POP3 servers. The
:class:`balderhub.smtp.lib.setup_features.LocalSmtpReader` and
:class:`balderhub.smtp.lib.setup_features.ProxySmtpReader` access the SMTP server directly and return the messages
from the outbox.

Access messages within same device
----------------------------------

.. code-block:: python

    import balder
    from tests.lib.setup_features import AiosmtpdServerFeature


    class SetupSimple(balder.Setup):

        ...

        class SmtpServer(balder.Device):
            server = AiosmtpdServerFeature()
            mail = LocalSmtpReader()
        ...

        def test_do_something(self):
            new_mail = self.SmtpServer.mail.wait_for_new_mail()
            ...


Access messages from other device
---------------------------------

.. code-block:: python

    import balder
    from tests.lib.setup_features import AiosmtpdServerFeature


    class SetupSimple(balder.Setup):

        ...

        class SmtpServer(balder.Device):
            server = AiosmtpdServerFeature()

        @balder.connect('SmtpServer', over_connection=balder.Connection)
        class MyDevice(balder.Device):
            mail = ProxySmtpReader(SmtpServer="SmtpServer")

        ...

        def test_do_something(self):
            new_mail = self.MyDevice.mail.wait_for_new_mail()
            ...
