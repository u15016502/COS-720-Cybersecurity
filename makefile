# Set default env variables
OPTION_WIDTH := 17
OPTION_ARG_WIDTH := 44
ARG_WIDTH := 14
BOLD := $(tput bold)
RESET := $(tput sgr0)
RESOURCE_FOLDER := "./res"
DATASET_DOWNLOAD_URL := "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tar.gz"
DATASET_DOWNLOAD_NAME := "enron_mail_20150507.tar.gz"
DATASET_DEFAULT_FOLDER_NAME := "maildir"
HEADER_DEFAULT_FILE := "headers.dat"

# Set switchable env variables
ifeq ($(ISOLATED),)
	ISOLATED := false
else
	ISOLATED := true
endif

ifeq ($(HEADER_FILE),)
	HEADER_FILE := $(HEADER_DEFAULT_FILE)
else
	HEADER_FILE := $(HEADER_FILE)
endif

ifeq ($(DATASET_FOLDER),)
	DATASET_FOLDER := "${RESOURCE_FOLDER}/${DATASET_DEFAULT_FOLDER_NAME}"
else
	DATASET_FOLDER := $(DATASET_FOLDER)
endif

# Silence the target rules
.SILENT: help get_dataset acquire_headers clean_headers anonymise_headers all

help:
	# Print all available options
	printf "Options:\n"
	printf "\t%-${OPTION_WIDTH}s  %-${OPTION_ARG_WIDTH}s  --  %s\n" \
		"get_dataset" "" "Download and extract enron email dataset."
	printf "\t%-${OPTION_WIDTH}s  %-${OPTION_ARG_WIDTH}s  --  %s\n" \
		"acquire_headers" "[ISOLATED=] [HEADER_FILE=] [DATASET_FOLDER=]" \
		"Acquire email headers from email dataset."
	printf "\t%-${OPTION_WIDTH}s  %-${OPTION_ARG_WIDTH}s  --  %s\n" \
		"clean_headers" "[ISOLATED=] [HEADER_FILE=]" "Clean acquired email headers."
	printf "\t%-${OPTION_WIDTH}s  %-${OPTION_ARG_WIDTH}s  --  %s\n" \
		"anonymise_headers" "[ISOLATED=] [HEADER_FILE=]" "Anonymise acquired email headers."
	printf "\t%-${OPTION_WIDTH}s  %-${OPTION_ARG_WIDTH}s  --  %s\n" \
		"all" "[ISOLATED=] [HEADER_FILE=] [DATASET_FOLDER=]" \
		"Perform all steps starting from get_dataset."
	# Print option args
	printf "\nArgs:\n"
	printf "\t%-${ARG_WIDTH}s  --  %s\n" \
		"ISOLATED" \
		"Run only the target rule. Do not run logically preceding target rules as well."
	printf "\t%-${ARG_WIDTH}s  --  %s\n" \
		"HEADER_FILE" \
		"The name of the data file containing extracted email headers."
	printf "\t%-${ARG_WIDTH}s  --  %s\n" \
		"DATASET_FOLDER" \
		"The directory in which the raw email dataset can be found."

get_dataset:
	# Check if resource folder exists.
	# If it does not exist, create one.
	if [ ! -d $(RESOURCE_FOLDER) ]; then \
		printf "Creating resource directory...\n"; \
		mkdir $(RESOURCE_FOLDER); \
	fi
	# Otherwise, continue...
	# If the dataset has already been downloaded, skip the download.
	if [ ! -f "${RESOURCE_FOLDER}/${DATASET_DOWNLOAD_NAME}" ]; then \
		printf "Downloading enron email dataset...\n"; \
		curl $(DATASET_DOWNLOAD_URL) --output "${RESOURCE_FOLDER}/${DATASET_DOWNLOAD_NAME}"; \
	fi
	# Otherwise, continue...
	# If the dataset has already been extraced, skip the extraction.
	if [ ! -d "${RESOURCE_FOLDER}/${DATASET_DEFAULT_FOLDER_NAME}" ]; then \
		printf "Extracting enron email dataset...\n"; \
		tar -f "${RESOURCE_FOLDER}/${DATASET_DOWNLOAD_NAME}" -C $(RESOURCE_FOLDER) --extract; \
	fi

acquire_headers:
# If isolated arg is not true, execute preceding target rule
ifeq ($(ISOLATED), false)
	make get_dataset --no-print-directory HEADER_FILE=$(HEADER_FILE) DATASET_FOLDER=$(DATASET_FOLDER)
endif
	# Run acquistion script
	printf "Acquring headers...\n"
	python3.6 ./src/python/acquisition.py \
		-p "${DATASET_FOLDER}" \
		-f "${RESOURCE_FOLDER}/${HEADER_FILE}"

clean_headers:
# If isolated arg is not true, execute preceding target rule
ifeq ($(ISOLATED), false)
	make acquire_headers --no-print-directory HEADER_FILE=$(HEADER_FILE) DATASET_FOLDER=$(DATASET_FOLDER)
endif
	# Run cleaning script
	printf "Cleaning headers...\n"
	python3.6 ./src/python/cleaning.py \
		-f "${RESOURCE_FOLDER}/${HEADER_FILE}"

anonymise_headers:
	echo "// TODO"

all:
	# Run last target rule in chain without ISOLATED arg 
	make clean_headers --no-print-directory HEADER_FILE=$(HEADER_FILE) DATASET_FOLDER=$(DATASET_FOLDER)
