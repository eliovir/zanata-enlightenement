#!/usr/bin/env python
# -*- coding: ISO8859-15 -*-
# $Id: update-desktop.py,v 1 2015-03-03 08:00:00CEST Eliovir $
#
# Author : Eliovir
# Creation Date : 2013-06-30 14:57:00CEST
# Last Revision : $Date: 2015-03-03 08:00:00CEST $
# Revision : $Rev: 1 $
# update-desktop.py
"""
[1mNAME[m
        update-desktop.py - update gettext files for .desktop files.

[1mDESCRIPTION[m
        to get polib, use hg clone https://bitbucket.org/izi/polib/

[1mEXAMPLE[m
        ./update-desktop.py src --import-po

[1mAUTHOR[m
        Eliovir

[1mVERSION[m
        $Date: 2015-03-03 08:00:00 +0100 (mar, 03 mars 2015) $
"""
__revision__ = "$Rev: 1 $"
__author__ = "Eliovir"
import ConfigParser
import fnmatch
import os.path
import subprocess
import sys
import time
try:
    from polib import polib
except ImportError:
    print "to get polib, use hg clone https://bitbucket.org/izi/polib/"
    print __doc__
    sys.exit(1)

# aide
if '-h' in sys.argv or '--help' in sys.argv:
    print __doc__
    sys.exit()

if len(sys.argv) < 2:
    print __doc__
    sys.exit()

importpo = '--import-po' in sys.argv
    
def add_new_file(path):
    os.popen('touch %s' % path)

def is_changed(path):
    lines = os.popen('git diff %s | grep @@ | wc -l' % path).readlines()
    return int(lines[0].strip()) > 1

if not os.path.exists('desktop'):
    os.makedirs('desktop')

# Find files
files = []
for path in sys.argv[1:]:
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.desktop'):
            files.append(os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, '*.desktop.in'):
            files.append(os.path.join(root, filename))

# Parse files
keys = ('Name', 'Comment', 'GenericName')
msgids = {}
langs = []
new_files = []
for afile in files:
    desktop = ConfigParser.ConfigParser()
    desktop.optionxform = str
    desktop.read(afile)
    msgid = ''
    for key in keys:
        for option in desktop.options('Desktop Entry'):
            if option == key:
                msgid = desktop.get('Desktop Entry', option)
                if msgid == '':
                    continue
                if not msgid in msgids:
                    msgids[msgid] = {'options':[key], 'files':[(afile, keys.index(key)+1)], 'msgstrs':{}}
                else:
                    if not key in msgids[msgid]['options']:
                        msgids[msgid]['options'].append(key)
                    msgids[msgid]['files'].append((afile, keys.index(key)+1))
            elif option.startswith(key) and msgid != '':
                lang = option[len(key)+1:-1]
                if lang == 'Name':
                    continue
                msgids[msgid]['msgstrs'][lang] = desktop.get('Desktop Entry', option)
                if not lang in langs:
                    langs.append(lang)
                    path = 'desktop/%s.po' % lang
                    if not os.path.exists(path) and importpo:
                        add_new_file(path)
                        new_files.append(path)

# Create/update .pot
pot = polib.POFile()
pot.metadata = {
    'Project-Id-Version': 'PACKAGE VERSION',
    'Report-Msgid-Bugs-To': '$MSGID_BUGS_ADDRESS',
    'POT-Creation-Date': time.strftime('%Y-%m-%d %H:%M%z'),
    'PO-Revision-Date': 'YEAR-MO-DA HO:MI+ZONE',
    'Last-Translator': 'FULL NAME <EMAIL@ADDRESS>',
    'Language-Team': 'LANGUAGE <LL@li.org>',
    'Language': '',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding': '8bit',
    'Plural-Forms': 'nplurals=INTEGER; plural=EXPRESSION;'
}
for msgid in msgids:
    entry = polib.POEntry(
            comment=', '.join(msgids[msgid]['options']),
            msgid=msgid,
            msgstr='',
            occurrences=msgids[msgid]['files']
    )
    pot.append(entry)
path = 'desktop/desktop.pot'
if not os.path.exists(path):
    add_new_file(path)
    pot.save(path)
else:
    pot.save(path)

if not importpo:
    sys.exit()

# Create/update .po
teams = {   
    'ar': 'Arabic <almusalimalmusalimah@gmail.com>',
    'bg': 'English <en@li.org>',
    'ca': 'Catalan',
    'cs': 'Czech <kde-i18n-doc@kde.org>',
    'da': 'Danish',
    'de': 'E17-de',
    'el': u'Ελληνικά, Σύγχρονα <opensuse-translation-el@opensuse.org>',
    'eo': 'Esperanto <translation-team-eo@lists.sourceforge.net>',
    'es': u'Español; Castellano <>',
    'et': 'Estonian <et@li.org>',
    'fi': 'Finnish <fi@li.org>',
    'fo': 'Faroese <fo@li.org>',
    'fr_ch': 'Enlightenment i18n French <enlightenment-intl@lists.',
    'fr': 'French <kde-i18n-doc@kde.org>',
    'gl': 'Galician <proxecto@trasno.net>',
    'he': 'Hebrew <he@li.org>',
    'hr': 'Croatian <hr@li.org>',
    'hu': 'magyar <>',
    'it': 'none',
    'ja': 'E17-jp <LL@li.org>',
    'km': 'Khmer <km@li.org>',
    'ko': 'Korean <KO@li.org>',
    'ku': 'Kurdish <ku@li.org>',
    'lt': 'Lithuanian Translation team',
    'ms': 'Malay <ms@li.org>',
    'nb': 'E17-nb <LL@li.org>',
    'nl': 'Dutch <kde-i18n-doc@kde.org>',
    'pl': 'Polish <translation-team-pl@lists.sourceforge.net>',
    'pt_br': 'Brazilian Portuguese',
    'pt': 'Portuguese',
    'ro': 'Romanian <ro@li.org>',
    'ru': 'ru <enlightenment-intl@lists.sourceforge.net>',
    'sk': 'Slovakian',
    'sl': 'Slovenian <sl@li.org>',
    'sr': u'српски <xfce-i18n@xfce.org>',
    'sv': 'Swedish',
    'tr': 'Turkish <kde-i18n-doc@kde.org>',
    'uk': 'Ukrainian <translation@linux.org.ua>',
    'zh_cn': 'Chinese (simplified) <i18n-zh@googlegroups.com>',
    'zh_tw': 'none'
}
pos = {}
plurals = {    
    #'ab': 'nplurals=2; plural=(n!=1);',
    'ar': 'nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5;',
    'bg': 'nplurals=2; plural=(n!=1);',
    'ca': 'nplurals=2; plural=(n!=1);',
    'cs': 'nplurals=3; plural=(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2;',
    'da': 'nplurals=2; plural=(n!=1);',
    'de': 'nplurals=2; plural=(n!=1);',
    'de': 'nplurals=2; plural=(n!=1);',
    'el': 'nplurals=2; plural=(n!=1);',
    'en': 'nplurals=2; plural=(n!=1);',
    'en_US': 'nplurals=2; plural=(n!=1);',
    'eo': 'nplurals=2; plural=(n!=1);',
    'es': 'nplurals=2; plural=(n!=1);',
    'fi': 'nplurals=2; plural=(n!=1);',
    'fr': 'nplurals=2; plural=(n>1);',
    'gl': 'nplurals=2; plural=(n>1);',
    'hi': 'nplurals=2; plural=(n!=1);',
    'hr': 'nplurals=2; plural=n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2;',
    'hu': 'nplurals=2; plural=(n!=1);',
    'id': 'nplurals=1; plural=0;',
    'it': 'nplurals=2; plural=(n!=1)',
    #'iw': 'nplurals=2; plural=(n!=1);',
    'ja': 'nplurals=1; plural=0;',
    'ko': 'nplurals=1; plural=0;',
    'ko': 'nplurals=1; plural=0;',
    'lt': 'nplurals=3; plural=n%10==1 && n%100!=11 ? 0 : n%10>=2 && (n%100<10 || n%100>=20) ? 1 : 2;',
    'lv': 'nplurals=3; plural=n%10==1 && n%100!=11 ? 0 : n != 0 ? 1 : 2;',
    'ms': 'nplurals=2; plural=(n!=1)',
    'nl': 'nplurals=2; plural=(n!=1);',
    'no': 'nplurals=2; plural=(n!=1);',
    'pl': 'nplurals=3; plural=(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);',
    'pt_br': 'nplurals=2; plural=(n!=1);',
    'pt_BR': 'nplurals=2; plural=(n!=1);',
    'pt': 'nplurals=2; plural=(n!=1);',
    'ro': 'nplurals=3; plural=(n == 1 ? 0: (((n % 100 > 19) || ((n % 100 == 0) && (n != 0))) ? 2: 1));',
    'ru': 'nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);',
    'sk': 'nplurals=3; plural=(n==1) ? 1 : (n>=2 && n<=4) ? 2 : 0;',
    'sl': 'nplurals=4; plural=(n%100==1 ? 0 : n%100==2 ? 1 : n%100==3 || n%100==4 ? 2 : 3);',
    'sr@latin': 'nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);',
    'sr': 'nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);',
    'sv': 'nplurals=2; plural=(n!=1);',
    'tl': 'nplurals=2; plural=(n!=1);',
    'tr': 'nplurals=1; plural=0;',
    'uk': 'nplurals=3; plural=n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2;',
    'vi': 'nplurals=1; plural=0;',
    'zh_cn': 'nplurals=2; plural=(n!=1);',
    'zh_tw': 'nplurals=1; plural=0;'
}
for lang in langs:
    pos[lang] = polib.POFile()
    pos[lang].metadata = {
        'Project-Id-Version': 'enlightenment',
        'Report-Msgid-Bugs-To': 'enlightenment-intl@lists.sourceforge.net',
        'POT-Creation-Date': time.strftime('%Y-%m-%d %H:%M%z'),
        'PO-Revision-Date': time.strftime('%Y-%m-%d %H:%M%z'),
        'Last-Translator': 'FULL NAME <EMAIL@ADDRESS>',
        'Language-Team': (teams[lang] if lang in teams else lang + ' <enlightenment-intl@lists.sourceforge.net>'),
        'Language': lang,
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding': '8bit',
        'Plural-Forms': (plurals[lang] if lang in plurals else plurals['eo'])
    }
for msgid in msgids:
    for lang in langs:
        if lang in msgids[msgid]['msgstrs']:
            msgstr = msgids[msgid]['msgstrs'][lang].decode("utf-8")
        else:
            msgstr = ''
        entry = polib.POEntry(
                comment=', '.join(msgids[msgid]['options']),
                msgid=msgid,
                msgstr=msgstr,
                occurrences=msgids[msgid]['files']
        )
        pos[lang].append(entry)
for lang in langs:
    path = 'desktop/' + lang + '.po'
    pos[lang].save(path)
