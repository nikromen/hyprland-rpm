srpm:
	dnf install -y rpmdevtools
	spectool -g $(spec)
	sed -i "s/%autorelease/$$(date +%s)%{?dist}/" $(spec)
	rpmbuild -bs $(spec) \
		--define "_sourcedir ." \
		--define "_srcrpmdir $(outdir)" \
		--define "_topdir ."
