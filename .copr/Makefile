srpm:
	dnf install -y rpmdevtools rpmautospec
	spectool -g $(spec)
	rpmbuild -bs $(spec) \
		--define "_sourcedir ." \
		--define "_srcrpmdir $(outdir)" \
		--define "_topdir ."
