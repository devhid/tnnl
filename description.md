# Project 3: Covert C&C and Exfiltration

In this project you will develop a client and a server for covert command and
control of, and data exfiltration from, an infected client [12]. You do not
have to implement any actual malicious capability, but just the communication
part. Any generated traffic should not stand out and should ideally look as
some innocuous communication.

## Requirements

You should implement the following capabilities:

1) the transmission of commands to the victim (and the receipt of
corresponding responses)

2) the asynchronous or periodic transmission of notifications from the victim
to the attacker-controlled server

3) the transmission of (potentially) large files from/to the victim and the
attacker-controlled server


## Additional Information

Your implementation should support at least one popular OS (i.e., Linux or
Windows). Support for multiple OSes or even architectures (e.g., ARM) is
welcome. The server can either run on the same or a different platform, or you
can even use some cloud provider or service. Your server should support
communication with multiple (e.g., hundreds of) clients.

The goal of your implementation will be to prevent the easy detection of the
C&C/exfiltrated traffic. You can follow any strategy you want, such as
pretending that the traffic belongs to some other application (e.g., some
video game or some chat application). Another approach is to hide the
communication as part of existing (or fake) communication towards online
services (e.g., Twitter, Facebook, blogs). In any case, the traffic should not
stand out or look suspicious.

## Bonus Points

* Rely on a popular online/cloud service to hide the server

* Use steganography [13] to hide commands or exfiltrated data

* Adaptive traffic rate limiting according to the legitimate traffic patterns
and activity of the victim host.

## References
[1] https://hovav.net/ucsd/dist/geometry.pdf<br>
[2] https://edmcman.github.io/papers/usenix11.pdf<br>
[3] http://shell-storm.org/talks/ROP_course_lecture_jonathan_salwan_2014.pdf<br>
[4] http://shell-storm.org/project/ROPgadget/<br>
[5] https://github.com/pakt/ropc<br>
[6] https://angelosk.github.io/Papers/2007/polymorph.pdf<br>
[7] http://phrack.org/issues/61/9.html<br>
[8] https://github.com/K2/ADMMutate<br>
[9] https://www.piotrbania.com/all/tapion/<br>
[10] https://github.com/cryptolok/MorphAES<br>
[11] https://www.symantec.com/avcenter/reference/hunting.for.metamorphic.pdf<br>
[12] https://azeria-labs.com/command-and-control/<br>
[13] https://www.blackhat.com/docs/eu-15/materials/eu-15-Bureau-Hiding-In-Plain-Sight-Advances-In-Malware-Covert-Communication-Channels.pdf<br>

## Useful Frameworks

http://www.capstone-engine.org/<br>
http://www.keystone-engine.org/<br>
http://www.unicorn-engine.org/<br>
https://github.com/gdabah/distorm<br>
http://www.radare.org/<br>
