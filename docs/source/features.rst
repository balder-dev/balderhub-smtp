Features
********


This section describes all features that are shipped with this package.


Scenario Features
=================

.. autoclass:: balderhub.smtp.lib.scenario_features.SmtpServerConfig
    :members:

SMTP Server
-----------

.. autoclass:: balderhub.smtp.lib.scenario_features.SmtpServerFeature
    :members:

.. autoclass:: balderhub.smtp.lib.scenario_features.SmtpReadableServerFeature
    :members:

SMTP Client
-----------

.. autoclass:: balderhub.smtp.lib.scenario_features.SmtpClientFeature
    :members:

Setup Features
==============

Server Implementations
----------------------

.. autoclass:: balderhub.smtp.lib.setup_features.AiosmtpdServerFeature
    :members:


Client Implementations
----------------------

.. autoclass:: balderhub.smtp.lib.setup_features.SmtplibClientFeature
    :members:

SMTP-Server Message Reader
--------------------------

The following features are implementation of the :class:`balderhub.email.lib.scenario_features.EmailReaderFeature`.


.. autoclass:: balderhub.smtp.lib.setup_features.LocalSmtpReader
    :members:

.. autoclass:: balderhub.smtp.lib.setup_features.ProxySmtpReader
    :members:
