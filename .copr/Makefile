srpm:
	dnf install -y rpmdevtools
	spectool -g $(spec)
	find $(dir $(spec)) -maxdepth 1 -type f ! -name '*.spec' -exec cp {} . \;
	sed -i "s/%autorelease/$$(date +%s)%{?dist}/" $(spec)
	rpmbuild -bs $(spec) \
		--define "_sourcedir ." \
		--define "_srcrpmdir $(outdir)" \
		--define "_topdir ."
