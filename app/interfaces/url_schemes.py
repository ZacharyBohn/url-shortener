from enum import Enum


class UrlScheme(Enum):
	HTTP = "http"
	HTTPS = "https"
	FTP = "ftp"
	MAILTO = "mailto"
	FILE = "file"
	TEL = "tel"
	NEWS = "news"
	IRC = "irc"
	RTSP = "rtsp"
	SPOTIFY = "spotify"
	SFTP = "sftp"
	SSH = "ssh"
	GIT = "git"
	SVN = "svn"
	MAGNET = "magnet"
	ED2K = "ed2k"
	AFP = "afp"
	NFS = "nfs"
	LDAP = "ldap"
	BITCOIN = "bitcoin"