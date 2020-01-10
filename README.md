# duplicity-rclone for Python3
[Duplicity](http://duplicity.nongnu.org/) backend using [rclone](http://rclone.org/)

Rclone is a powerful command line program to sync files and directories to and from various cloud storage providers.

At the time of deveopment, I was using duplicity v0.7.10 and Amazon Cloud Drive, but this backend should work with any storage provider supported by rclone, and with later version of duplicity.\
I am currently running it with duplicity v0.7.17 and rclone v1.43.1, without issues.

Since I've never wrote Python before today, use it at your own risk. Every feedback, comment or suggestion is welcome.

**Update 19/05/2017:** Since Amazon banned rclone, I moved my data to Google Drive, and it works smoothly as expected.

**Update 2010/01/10:** Updated to run using Python3.


# Setup
Install `rclonebackend.py` into duplicity backend directory. This backend provides support for prefix `rclone://`.
Duplicity Backend directory is similar to: /...../duplicity/backends

# Usage
Once you have configured rclone and successfully set up a remote (e.g. `gdrive` for Google Drive), assuming you can list your remote files with
```
rclone ls gdrive:mydocuments
```
you can start your backup with
```
duplicity /mydocuments rclone://gdrive:/mydocuments
```
**Please note the slash after the second colon.** Some storage provider will work with or without slash after colon, but some other will not. Since duplicity will complain about malformed URL if a slash is not present, **always put it after the colon**, and the backend will handle it for you.

# Development setup (John Radley)
Windows 10 Host, VirtualBox 6.1.0, Ubuntu 19.10
Installed Brew, from https://docs.brew.sh/Homebrew-on-Linux
Installed Pipenv, from https://pipenv-fork.readthedocs.io/en/latest
  using: $brew install pipenv
Installed Pycharm Community Edition (excellent!)
--as the honesty of the original author, my Python skills are low.
-- it took longer to setup development environment than fix the software!!

# Test commands (so far!), for Pycharm's parameters field. First to see how code runs!
full -v 9 --log-file=/home/john/duplicitytest-dest/log.log /home/john/duplicitytest-src/ file:///home/jradley/duplicitytest-dest
full -v 9 --log-file=/home/john/duplicitytest-dest/log.log /home/john/duplicitytest-src/ rclone://Box1:/test001
remove-older-than now --force -v 9 --log-file=/home/john/duplicitytest-dest/log.log  rclone://Box1:/test001


//End
10th Jan 2020

