#!/bin/bash
if [ $# -lt 1 ] ; then
	echo "install <pkg>"
	exit 0
fi

pkg=$1
if [ $# -gt 1 ]; then
	dest=$2
fi
echo "Installing to AWS instance"
scp -i /Users/veluppillaisengo/Documents/Keys/LightsailDefaultKey-us-east-1.pem  $pkg bitnami@54.163.186.96:~/stack/projects/idaikkadu/$dest
