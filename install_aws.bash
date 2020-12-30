#!/bin/bash
pkg=Idaikkadu.tar

if [ $# -ge 1 ] ; then
	echo "install <pkg>"
	pkg=$1
fi

if [ $# -gt 1 ]; then
	dest=$2
fi

echo "Packaging $pkge"
rm $pkg
tar -cvf $pkg  accounts idaikkadu media news photos web db.sqlite3
gzip $pkg 

echo "Installing to AWS instance"
scp -i /Users/veluppillaisengo/Documents/Keys/LightsailDefaultKey-us-east-1.pem  ${pkg}.gz bitnami@54.163.186.96:~/stack/projects/idaikkadu/$dest
./ssh_aws.bash
