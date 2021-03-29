PROVE_ARGS ?= -r -v
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
TARBALL_NAME = ${PKG}-${VERSION}.tar.bz2

# OBS local project path: set it as a command line argument or as an ENV variable
OBSPROJ ?= "placeholder"
# OBS target platform
OBSTARG ?= "SLE_12_SP2"

tarball:
	@echo -e "\e[33mMaking ${TARBALL_NAME}\e[0m"
	@echo
	tar cvjf ${TARBALL_NAME} ${FILE_LIST}
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
	@cp ${TARBALL_NAME} ${OBSPROJ}
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

.PHONY: checkstyle
checkstyle:
ifneq ($(CHECKSTYLE),0)
	find . -type f -exec awk ' /^#!.*bash/{print FILENAME} {nextfile}' {} + | grep -v *fh_test* | xargs shellcheck -s bash || :
	find . -type f -exec awk ' /^#!.*perl/{print FILENAME} {nextfile}' {} + | grep -v *fh_test* | xargs perlcritic --gentle || :
	find . -name '*.py' | grep -v *fh_test* | xargs flake8 --ignore=E501 || :
endif

PHONY: test
test: checkstyle
