I18N repository to manage Enlightenment translations in Zanata.

# Add a project to manage

Edit `projects.sh`.

# Update Gettext templates

`./update.sh`

# Clean Git submodules before pushing

`clean-repos.sh`

# Push Gettext templates to Zanata

## How to install zanata-cli

```
cd ~/bin
wget http://wwwftp.ciril.fr/pub/apache//ant/ivy/2.4.0/apache-ivy-2.4.0-bin.tar.gz
tar zxvf apache-ivy-2.4.0-bin.tar.gz
export IVY_JAR=~/bin/apache-ivy-2.4.0/ivy-2.4.0.jar
wget https://raw.github.com/zanata/zanata-client-ivy/master/zanata-cli
chmod 755 zanata-cli
```

Go to `https://translate.zanata.org/zanata/dashboard/settings/client` and copy config to `~/.config/zanata.ini`.

## Push

Only for administrators.

`zanata-cli push`

Be careful than all gettext files are UTF-8 encoded and the header contains
`"Content-Type: text/plain; charset=UTF-8\n"`.
