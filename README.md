This is just a simple naive python script for log down the user login activities on Ejabberd server.

It just read the ejabberd log file continuously for the "failed" & "accepted" login, if "failed" login reached to a threshold,the user will be banned.

The ban action require Ejabberd additional module ```ejabberd-contrib/mod_admin_extra``` to be enabled.
