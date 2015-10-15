#!/bin/bash
# Author: Mirosław Zalewski <mz@miroslaw-zalewski.eu>
# License: None
# Last modified: Sun, 31 Mar 2013 10:59:31 +0200
##########################################################################

# Set up icons and names that you will use in Opera menu file.
# The format is: one word for name, space, path to icon on your
# system. 
# If you want to change location of icons in skin file, look at
# SKIN_CUSTOM_BUTTONS_DIR variable

ICONS=$(cat <<EOT
iceweasel /usr/share/icons/hicolor/32x32/apps/iceweasel.png
rekonq /usr/share/icons/hicolor/32x32/apps/rekonq.png
chromium /usr/share/icons/hicolor/48x48/apps/chromium.png
konqueror /usr/share/icons/hicolor/32x32/apps/konqueror.png
EOT
)

# --- VARIABLES ---
OPERA_DIR="$HOME/.opera/"
OPERA_SKIN_DIR="$OPERA_DIR/skin/"
SKIN_CUSTOM_BUTTONS_DIR="custom_buttons"

# --- FUNCTIONS ---
abs_path() {
	readlink -f "$1"
}

read_md5() {
	md5sum "$1" 2>/dev/null |awk '{print $1}'
}

add_icons() {
	local SKIN_FILE="$1"
	local SKIN_FILENAME="$(basename "$SKIN_FILE")"
	local SKIN_FILENAME_WITHOUT_EXT="${SKIN_FILENAME%.*}"
	local TMP_SKIN_DIR="/tmp/${SKIN_FILENAME_WITHOUT_EXT}"
	local INI_CHANGED=0
	local SKIN_INI="$TMP_SKIN_DIR"/skin.ini

	echo "Processing ${SKIN_FILENAME}..."

	if [ ! -z "$IS_OPERA_RUNNING" ]; then
		if grep -q "$SKIN_FILENAME" "$OPERA_DIR/operaprefs.ini"; then
			echo "	Currently running Opera uses this skin. Skipping."
			return
		fi
	fi

	if [ -e "$TMP_SKIN_DIR" ]; then
		rm -rf "$TMP_SKIN_DIR"/*
		if [ "$?" -ne 0 ]; then 
			if ! TMP_SKIN_DIR=$(mktemp -d /tmp/opera-skin-XXXXX) ; then
				echo -n "	Failed. /tmp permissions might be wrong."
				return 1
			fi
		fi
	else
		mkdir -p "$TMP_SKIN_DIR"
		if [ "$?" -ne 0 ]; then 
			echo -n "	Failed. /tmp permissions might be wrong."
			return 1
		fi
	fi

	cp "$SKIN_FILE" "$TMP_SKIN_DIR"
	unzip -o -qq "$TMP_SKIN_DIR"/"$SKIN_FILENAME" -d "$TMP_SKIN_DIR"
	mkdir "$TMP_SKIN_DIR"/"$SKIN_CUSTOM_BUTTONS_DIR" 2>/dev/null

	if [ ! -e "$SKIN_INI" ]; then
		echo "   Skin doesn't have ini file. Skipping."
		return 1
	fi
	dos2unix -q "$SKIN_INI"
	while read ICON_NAME ICON_PATH; do
		cp "$ICON_PATH" "$TMP_SKIN_DIR"/"$SKIN_CUSTOM_BUTTONS_DIR"

		if grep -q -e "$ICON_NAME" "$SKIN_INI"; then
			EXISTING_ICON_PATH=$(sed -n -r -e 's/'"$ICON_NAME"'\s*=\s*(.+)/\1/ p' "$SKIN_INI")
			if [ x$(read_md5 "$TMP_SKIN_DIR/$EXISTING_ICON_PATH") = x$(read_md5 "$ICON_PATH") ]; then
				continue
			fi
			sed -i -e "s/$ICON_NAME.*/$ICON_NAME = $SKIN_CUSTOM_BUTTONS_DIR\/$(basename "$ICON_PATH")/" "$SKIN_INI"
			INI_CHANGED=1
		else
			sed -i -e '/\[Images\]/ a\
'"$ICON_NAME = $SKIN_CUSTOM_BUTTONS_DIR/$(basename "$ICON_PATH")" "$SKIN_INI"
			INI_CHANGED=1
		fi
	done < <(echo "$ICONS")
	unix2dos -q "$SKIN_INI"

	if [ "$INI_CHANGED" -eq 0 ]; then
		echo "	There was nothing to do."
		return
	fi

	rm -f "$TMP_SKIN_DIR"/"$SKIN_FILENAME"
	OLD_DIR="$(pwd)"
	cd "$TMP_SKIN_DIR"
	zip -q -r "$SKIN_FILENAME" *
	mv -f "$SKIN_FILENAME" "$OPERA_SKIN_DIR"
	cd "$OLD_DIR"
}

# --- INVOCATION ---

if ps -C opera u |grep -q $(whoami); then
	IS_OPERA_RUNNING=1
fi

if [ ! -z "$1" ]; then
	ARG_FILE="$(abs_path "$1")"
	if [ -r "$ARG_FILE" ]; then
		add_icons "$ARG_FILE"
		exit
	fi
fi

if [ -d "$OPERA_SKIN_DIR" ]; then
	for FILE in "$OPERA_SKIN_DIR"/*.zip; do
		add_icons "$(abs_path "$FILE")"
	done
fi
