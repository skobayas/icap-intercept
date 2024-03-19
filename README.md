# What is this?

This is trivial sample for ICAP interceptor
This is helper script for MITM proxy.
It can only intercept encrypted archive(zip) file.
In the other words, for unencrypted archive or other file type, do nothing.

## Why do we need such one?(Encrypted Archive is headache)

As you know, we have a threat of some malware.
The bad guys invents several way to transport them.

The famous one is emotet.
Such malware abuse macro features.
By the way, several solutions can act as against such activities.
For example, CDR(Content Disarmed and Reconstruction) do it.
But even such solutions, they need extract files correctly.
In short those solutions requires correct password for encrypted archive.

During transport, the administrator have to intercept them and process to CDR with valid password.

We have several way to intercept with proxy.
Such as mail(SMTP) and HTTPS(ICAP).

The intercept can do easily, but slightly hard to intercept encrypted archive via HTTPS.
We don't have standard way to notice.

## This is a PoC for such objective.

A helper script for MITM proxy intercepts encrypted archive and store them to S3(for example.)
Every user who should revive encrypted archive should notice for download.

They provide archive password for CDR.
After process of CDR, they can get sanitized file.
Of course those file are encrypted as original password.

## What services am I using?

I use a couple of services, such as

-MetaDefender Cloud
This is key service for sanitization

-AWS lambda
Another key services, the lambda functions has a URL which call by webhook style.

-AWS S3
For web hosting and stores files(untrusted and sanitized(trusted))

## How works does it?

1. Every user should use this proxy.
2. If the proxy found encrypted archive, it stored that file to S3 and send to notice for retrieve.
3. The user find each file via web site, specify the file and provide valid password for extract.
4. The MetaDefender Could process that file.
5. After process(sanitized), clean file stored to S3.
6. Every user can retrieve via another HTML, each files re-encrypts original password.
   (Thus, each files keep confidentiality even if those located as public S3.)

## Demo

Already several files are located to S3.
(Doesn't need to prepare ICAP proxy)

1. You can find several zip following URL
https://untrusted-files-list.s3.ap-northeast-1.amazonaws.com/index.html
2. The encrypt password of all files are "SecreT"
3. Specify a file, enter above password and submit
4. The sanitize process request will invoke
5. Couple of minutes(depends on MetaDefender Cloud condition), you can find sanitized files.
6. You can download your file and extract with the password.
https://sanitized-files-list.s3.ap-northeast-1.amazonaws.com/index.html

Note : If you provide invalid password, can not process it.

### Limitation

The CDR process handle by MetaDefender Cloud.
This demo uses evaluation API key, thus it has number of limitations.
If reach the limit, the CDR process can't handle.
In that case, you can see error messages during step3.
