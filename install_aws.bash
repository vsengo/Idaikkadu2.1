#!/bin/bash
pkg=Idaikkadu.tar.gz
if [ $# -ge 1 ] ; then
	echo "install <pkg>"
	pkg=$1
fi

if [ $# -gt 1 ]; then
	dest=$2
fi
echo "Installing to AWS instance"
scp -i /Users/veluppillaisengo/Documents/Keys/LightsailDefaultKey-us-east-1.pem  $pkg bitnami@54.163.186.96:~/stack/projects/idaikkadu/$dest
