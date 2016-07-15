FILE_LIST = crmconfig \
			doc \
			man \
			ra \
	 		bin \
	 		srHook \
	 		test \
	 		wizard


PKG = SAPHanaSR-ScaleOut
SPECFILE = ${PKG}.spec
VERSION = $(strip $(patsubst Version:,,$(shell grep '^Version:' $(SPECFILE))))

# OBS local project path: set it as a command line argument or as an ENV variable
OBSPROJ ?= "placeholder"
# OBS target platform
OBSTARG ?= "SLE_12_SP2"

tarball:
	@echo -e "\e[33mMaking ${PKG}-${VERSION}.tgz\e[0m"
	@echo
	tar zcvf ${PKG}-${VERSION}.tgz ${FILE_LIST}
	@echo -e "\e[32mDone\e[0m"

.ONESHELL:
copy: tarball
	@if [ $(OBSPROJ) = "placeholder" ]; then \
		echo -e "\e[31mProject directory is missing. Set it via 'OBSPROJ=/path/to/project'\e[0m"; \
		exit 1; \
	fi
	@echo -e "\e[33mCopying the SPEC file, CHANGES file and the tarball to ${OBSPROJ}\e[0m"
	@cp ${PKG}.changes ${OBSPROJ}
	@cp ${PKG}.spec ${OBSPROJ}
	@cp ${PKG}-${VERSION}.tgz ${OBSPROJ}
	@echo -e "\e[32mDone\e[0m"

.ONESHELL:
build: copy
	@echo -e "\e[33mInitiating the build\e[0m"
	@cd ${OBSPROJ}
	osc -A https://api.suse.de build ${OBSTARG}
	@echo -e "\e[32mDone\e[0m"


.ONESHELL:
commit: copy
	@echo -e "\e[33mCommiting the code\e[0m"
	@cd ${OBSPROJ}
	osc -A https://api.suse.de addremove
	osc -A https://api.suse.de commit
	@echo -e "\e[32mDone\e[0m"

.phony: 	tarball