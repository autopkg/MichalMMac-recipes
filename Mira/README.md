# Mira

[Mira](http://twistedmelon.com/mira/) is Preference Pane for configuring Apple remote behavior

## Notes

- Mira is paid software
- Munki recipe specifies `RequireRestart` pkginfo key because of multiple launchd items (un)loaded by package scripts in user context
- Scripts do a lot of neat things in user's Library. For example thex disable Plex helper. Installing by Munki or AutoPkg prevents them from doing so. Inspect both scripts before deploying

## Scripts

### preinstall

    #!/bin/sh

    osascript -e 'tell application "System Preferences" to quit'

    launchctl unload -w "/Library/LaunchAgents/com.twistedmelon.mira.agent.plist"

    osascript -e 'tell application "System Events"' -e 'set ProcessList to name of every process'  -e 'if "miraRCD" is in ProcessList then' -e 'tell application "miraRCD" to quit' -e 'end if' -e 'end tell'

    kill -HUP `ps -axwwwww | grep 'miraUSBDriver' | grep -v grep | awk '{print $1}'`
    kill -HUP `ps -axwwwww | grep 'miraRCD' | grep -v grep | awk '{print $1}'`

    rm -R /Library/PreferencePanes/mira.prefPane
    rm -R $HOME/Library/PreferencePanes/mira.prefPane
    rm -R $HOME/Library/Caches/com.apple.preferencepanes.cache

    mkdir /Library/Preferences/mira
    chmod -R 777 /Library/Preferences/mira
    chown $USER:admin /Library/Preferences/mira

    mkdir $HOME/Library/Preferences/mira
    chmod -R 777 $HOME/Library/Preferences/mira
    chown $USER:staff $HOME/Library/Preferences/mira

    # change the field separator character temporarily - set to newline only so that spaces can be used in filenames
    tmpIFS=$IFS
    IFS=$'\012'



    # define variables for Mira's profiles folders which will be checked before being operated on
    userProfilesFolder=$HOME/Library/Preferences/mira/Profiles/
    sysProfilesFolder=/Library/Preferences/mira/Profiles/

    # search current user's Mira profiles folder for the old Front Row action and replace with an alias to the Front Row launcher
    if [ -d $userProfilesFolder ]
    then
      filespec=`grep -rilP '<string>Front Row</string>\n\t\t\t\t<key>Should.*</key>' $HOME/Library/Preferences/mira/Profiles/*`
    fi


    if [ "$filespec" ]
    then
      perl -0777 -p -i -e 's!\t\t\t\t<string>Front Row</string>\n\t\t\t\t<key>.*</key>\n\t\t\t\t<.*>\n\t\t\t\t<key>Type</key>\n\t\t\t\t<integer>2</integer>\n!\t\t\t\t<string>Front Row</string>\n\t\t\t\t<key>Should Repeat</key>\n\t\t\t\t<false/>\n\t\t\t\t<key>Alias</key>\n\t\t\t\t<data>\n\t\t\t\tAAAAAAFAAAIAAQRCb290AAAAAAAAAAAAAAAAAAAAAAAA\n\t\t\t\tAAAAAADJ8hZDSCsAAAAAAOkNRnJvbnQgUm93LmFwcAAA\n\t\t\t\tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\t\t\t\tAAAAAAAAAAAAAAAAAAAAAACJt8aYExUAAAAAAAAAAP//\n\t\t\t\t//8AAAkgAAAAAAAAAAAAAAAAAAAADEFwcGxpY2F0aW9u\n\t\t\t\tcwAQAAgAAMnyToMAAAARAAgAAMaYS1UAAAABAAQAAADp\n\t\t\t\tAAIAH0Jvb3Q6QXBwbGljYXRpb25zOkZyb250IFJvdy5h\n\t\t\t\tcHAAAA4AHAANAEYAcgBvAG4AdAAgAFIAbwB3AC4AYQBw\n\t\t\t\tAHAADwAKAAQAQgBvAG8AdAASABpBcHBsaWNhdGlvbnMv\n\t\t\t\tRnJvbnQgUm93LmFwcAATAAEvAP//AAA=\n\t\t\t\t</data>\n\t\t\t\t<key>Type</key>\n\t\t\t\t<integer>1</integer>\n!g' $filespec
    fi

    unset filespec

    # search Library's Mira profiles folder for the old Front Row action and replace with an alias to the Front Row launcher
    if [ -d "$sysProfilesFolder" ]
    then
      filespec=`grep -rilP '<string>Front Row</string>\n\t\t\t\t<key>Should.*</key>' /Library/Preferences/mira/Profiles/*`
    fi

    if [ "$filespec" ]
    then
      perl -0777 -p -i -e 's!\t\t\t\t<string>Front Row</string>\n\t\t\t\t<key>.*</key>\n\t\t\t\t<.*>\n\t\t\t\t<key>Type</key>\n\t\t\t\t<integer>2</integer>\n!\t\t\t\t<string>Front Row</string>\n\t\t\t\t<key>Should Repeat</key>\n\t\t\t\t<false/>\n\t\t\t\t<key>Alias</key>\n\t\t\t\t<data>\n\t\t\t\tAAAAAAFAAAIAAQRCb290AAAAAAAAAAAAAAAAAAAAAAAA\n\t\t\t\tAAAAAADJ8hZDSCsAAAAAAOkNRnJvbnQgUm93LmFwcAAA\n\t\t\t\tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\t\t\t\tAAAAAAAAAAAAAAAAAAAAAACJt8aYExUAAAAAAAAAAP//\n\t\t\t\t//8AAAkgAAAAAAAAAAAAAAAAAAAADEFwcGxpY2F0aW9u\n\t\t\t\tcwAQAAgAAMnyToMAAAARAAgAAMaYS1UAAAABAAQAAADp\n\t\t\t\tAAIAH0Jvb3Q6QXBwbGljYXRpb25zOkZyb250IFJvdy5h\n\t\t\t\tcHAAAA4AHAANAEYAcgBvAG4AdAAgAFIAbwB3AC4AYQBw\n\t\t\t\tAHAADwAKAAQAQgBvAG8AdAASABpBcHBsaWNhdGlvbnMv\n\t\t\t\tRnJvbnQgUm93LmFwcAATAAEvAP//AAA=\n\t\t\t\t</data>\n\t\t\t\t<key>Type</key>\n\t\t\t\t<integer>1</integer>\n!g' $filespec
    fi

    unset filespec

    # Rename PowerPoint profiles and PowerPoint display names (rename 08 version to "PowerPoint" and 04 version to "PowerPoint 04"
    # need to change profileID, display name and filename

    # DELETE PowerPoint 2004 profile

    #PowerPoint 04  - loop in case there are multiple files - then work on one file at a time - this will delete all but the last file
    for filespec in `grep -rl '<string>com.microsoft.PowerPoint</string>' $HOME/Library/Preferences/mira/Profiles/*`;do

      rm $filespec

    done
    unset replaceFile
    unset filespec

    # Library profile folder
    for filespec in `grep -rl '<string>com.microsoft.PowerPoint</string>' /Library/Preferences/mira/Profiles/*`;do

      rm $filespec

    done
    unset replaceFile
    unset filespec


    # PowerPoint 08 - loop in case there are multiple files - then work on one file at a time - this will delete all but the last file
    # User profile folder
    for filespec in `grep -rl '<string>com.microsoft.Powerpoint</string>' $HOME/Library/Preferences/mira/Profiles/*`;do

      unset replaceFile
      replaceFile=`grep -rl -m 1 '<string>PowerPoint 08</string>' "$filespec"`

      if [ "$replaceFile" ]
      then
        perl -0777 -p -i -e 's!<string>PowerPoint 08</string>!<string>PowerPoint</string>!g' $replaceFile
        mv $replaceFile "$HOME/Library/Preferences/mira/Profiles/Microsoft PowerPoint.mpl"
      fi

    done
    unset replaceFile
    unset filespec

    # Library profile folder
    for filespec in `grep -rl '<string>com.microsoft.Powerpoint</string>' /Library/Preferences/mira/Profiles/*`;do

      unset replaceFile
      replaceFile=`grep -rl -m 1 '<string>PowerPoint 08</string>' "$filespec"`

      if [ "$replaceFile" ]
      then
        perl -0777 -p -i -e 's!<string>PowerPoint 08</string>!<string>PowerPoint</string>!g' $replaceFile
        mv $replaceFile "/Library/Preferences/mira/Profiles/Microsoft PowerPoint.mpl"
      fi

    done
    unset replaceFile
    unset filespec


    # Rename old Plex profile (to Plex/Nine) and create new Plex Profile with new bundleID (which also uses new DuoPress file)
    # User profile folder
    for filespec in `grep -rl '<string>com.plexsquared.Plex</string>' $HOME/Library/Preferences/mira/Profiles/*`;do

      unset replaceFile
      replaceFile=`grep -rl -m 1 '<string>Plex</string>' "$filespec"`

      if [ "$replaceFile" ]
      then
        cp $replaceFile "$HOME/Library/Preferences/mira/Profiles/Plex-Nine.mpl"

        perl -0777 -p -i -e 's!<string>Plex</string>!<string>Plex/Nine</string>!g' "$HOME/Library/Preferences/mira/Profiles/Plex-Nine.mpl"

        perl -0777 -p -i -e 's!<string>com.plexsquared.Plex!<string>NEWPLEX!g' $replaceFile

    # above, change bundle ID to some temporary value like "NEWPLEX" - we will check for this and overwrite with real profile in post-install script
    # this prevents someone with edits to the old plex profile from fucking up the new plex profile and prevents overwriting new plex profile if it was already installed

      fi

    done
    unset replaceFile
    unset filespec

    # Library profile folder
    for filespec in `grep -rl '<string>com.plexsquared.Plex</string>' /Library/Preferences/mira/Profiles/*`;do

      unset replaceFile
      replaceFile=`grep -rl -m 1 '<string>Plex</string>' "$filespec"`

      if [ "$replaceFile" ]
      then
        cp $replaceFile "/Library/Preferences/mira/Profiles/Plex-Nine.mpl"

        perl -0777 -p -i -e 's!<string>Plex</string>!<string>Plex/Nine</string>!g' "/Library/Preferences/mira/Profiles/Plex-Nine.mpl"

        perl -0777 -p -i -e 's!<string>com.plexsquared.Plex!<string>NEWPLEX!g' $replaceFile
      fi

    done
    unset replaceFile
    unset filespec


    # Set/force the "Use Unique Settings Per User" master preference to TRUE - we've hidden this setting in the UI to disable setting it.
    perl -0777 -p -i -e 's!<key>per user</key>\n\t<false/>!<key>per user</key>\n\t<true/>!g' /Library/Preferences/mira/com.twistedmelon.mira.plist

    IFS=$tmpIFS

    exit 0

### postinstall

    #!/bin/bash

    # Create Plex keymap folders in case they don't already exist.
    mkdir -p "$HOME/Library/Application Support/Plex/userdata/keymaps/"
    mkdir -p "$HOME/Library/Application Support/Plex Home Theater/userdata/keymaps/"

    mkdir -p "/Library/Application Support/Plex/userdata/keymaps/"
    mkdir -p "/Library/Application Support/Plex Home Theater/userdata/keymaps/"


    osascript -e 'tell application "System Preferences" to quit'

    osascript -e 'tell application "System Events"' -e 'set ProcessList to name of every process'  -e 'if "miraRCD" is in ProcessList then' -e 'tell application "miraRCD" to quit' -e 'end if' -e 'end tell'

    #Remove old miraRCD login item from Mira 1.4.8 and earlier
    osascript -e 'tell application "System Events"' -e 'get the name of every login item' -e 'if login item "miraRCD" exists then' -e 'delete login item "miraRCD"' -e 'end if' -e 'end tell'
    /usr/bin/su $USER -c "osascript RemoveMiraLoginItem.app"

    plutil -convert xml1 "/Library/Preferences/loginwindow.plist"
    perl -0777 -p -i -e 's!<string>/Library/PreferencePanes/mira.prefPane/Contents/Resources/miraRCD.app</string>!<string></string>!g' "/Library/Preferences/loginwindow.plist"
    plutil -convert binary1 "/Library/Preferences/loginwindow.plist"

    # Remove previous Mira helper app from the user's Application Support folder
    rm -R "$HOME/Library/Application Support/miraRCD/"

    # Set up Mira auto-launching - This changed to launchd in 1.4.9 final - by copying plist and using launchctl to install - must remove old login item
    launchctl unload -w "/Library/LaunchAgents/com.twistedmelon.mira.agent.plist"
    /usr/bin/su $USER -c "launchctl unload -w /Library/LaunchAgents/com.twistedmelon.mira.agent.plist"

    cp "/Library/PreferencePanes/mira.prefPane/Contents/Resources/com.twistedmelon.mira.agent.plist" "/Library/LaunchAgents/com.twistedmelon.mira.agent.plist"
    chown root:wheel /Library/LaunchAgents/com.twistedmelon.mira.agent.plist
    chmod -R 644 /Library/LaunchAgents/com.twistedmelon.mira.agent.plist

    /usr/bin/su $USER -c "launchctl load -wF /Library/LaunchAgents/com.twistedmelon.mira.agent.plist"

    defaults write com.apple.LaunchServices LSHandlers -array-add "<dict><key>LSHandlerContentTag</key><string>miralicense</string><key>LSHandlerContentTagClass</key><string>public.filename-extension</string><key>LSHandlerRoleAll</key><string>com.twistedmelon.miraRCD</string></dict>"

    # change the field separator character temporarily - set to newline only so that spaces can be used in filenames
    tmpIFS=$IFS
    IFS=$'\012'

    #Uninstall Plex Launch Agent
    #Disable the Plex Helper in Plex prefs file - prevents it taking over Apple remote.
    launchctl unload -w "$HOME/Library/LaunchAgents/com.plexapp.helper.plist"
    launchctl unload -w "$HOME/Library/LaunchAgents/com.plexapp.ht.helper.plist"
    perl -0777 -p -i -e 's!<appleremotealwayson>true</appleremotealwayson>!<appleremotealwayson>false</appleremotealwayson>!g' "$HOME/Library/Application Support/Plex/userdata/guisettings.xml"
    perl -0777 -p -i -e 's!<appleremotemode>.</appleremotemode>!<appleremotemode>0</appleremotemode>!g' "$HOME/Library/Application Support/Plex/userdata/guisettings.xml"
    perl -0777 -p -i -e 's!<appleremotealwayson>true</appleremotealwayson>!<appleremotealwayson>false</appleremotealwayson>!g' "$HOME/Library/Application Support/Plex Home Theater/userdata/guisettings.xml"
    perl -0777 -p -i -e 's!<appleremotemode>.</appleremotemode>!<appleremotemode>0</appleremotemode>!g' "$HOME/Library/Application Support/Plex Home Theater/userdata/guisettings.xml"
    kill `ps -axwwwww | grep 'PlexHelper' | grep -v grep | awk '{print $1}'`
    kill `ps -axwwwww | grep 'PlexHTHelper' | grep -v grep | awk '{print $1}'`
    rm "$HOME/Library/LaunchAgents/com.plexapp.helper.plist"
    rm "$HOME/Library/LaunchAgents/com.plexapp.ht.helper.plist"




    # Copy newer Plex profile from Mira bundle if required (check for a marked profile in the profiles folder)
    # User profile folder
    for filespec in `grep -rl '<string>NEWPLEX</string>' $HOME/Library/Preferences/mira/Profiles/*`;do

        cp "/Library/PreferencePanes/mira.prefPane/Contents/Resources/Profiles/Plex.mpl" "$HOME/Library/Preferences/mira/Profiles/Plex.mpl"

    done
    unset filespec


    #Force copy the newest Plex Home Theater profile from Mira bundle - this will overwrite any changes someone may have made to their previous Plex HT profile.
    cp "/Library/PreferencePanes/mira.prefPane/Contents/Resources/Profiles/Plex Home Theater.mpl" "$HOME/Library/Preferences/mira/Profiles/Plex Home Theater.mpl"


    IFS=$tmpIFS

    # Install Plex Mira keymaps file into user's Plex Application support path
    cp "/Library/PreferencePanes/mira.prefPane/Contents/Resources/extras/Mira Keyboard Extras.xml" "$HOME/Library/Application Support/Plex/userdata/keymaps/Mira Keyboard Extras.xml"
    cp "/Library/PreferencePanes/mira.prefPane/Contents/Resources/extras/Mira Keyboard Extras.xml" "$HOME/Library/Application Support/Plex Home Theater/userdata/keymaps/Mira Keyboard Extras.xml"

    cp "/Library/PreferencePanes/mira.prefPane/Contents/Resources/extras/Mira Keyboard Extras.xml" "/Library/Application Support/Plex/userdata/keymaps/Mira Keyboard Extras.xml"
    cp "/Library/PreferencePanes/mira.prefPane/Contents/Resources/extras/Mira Keyboard Extras.xml" "/Library/Application Support/Plex Home Theater/userdata/keymaps/Mira Keyboard Extras.xml"


    # Set/force the "Hide Missing Applications" preference to TRUE
    perl -0777 -p -i -e 's!<key>hide if app missing</key>\n\t<false/>!<key>hide if app missing</key>\n\t<true/>!g' $HOME/Library/Preferences/mira/com.twistedmelon.mira.plist


    chmod -R 775 /Library/PreferencePanes/mira.prefPane/
    chmod u+s /Library/PreferencePanes/mira.prefPane/Contents/Resources/miraRCD.app/Contents/MacOS/AuthTool
    chmod u+s /Library/PreferencePanes/mira.prefPane/Contents/Resources/miraRCD.app/Contents/MacOS/miraAppSwitcher

    chmod -R 777 /Library/Preferences/mira/
    chmod 777 /Library/Preferences/mira/com.twistedmelon.mira.plist
    chown $USER:admin /Library/Preferences/mira/com.twistedmelon.mira.plist

    chown $USER:staff $HOME/Library/Preferences/mira
    chmod -R 775 $HOME/Library/Preferences/mira


    # /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister -kill -domain local -domain system -domain user

    # Open Mira in System Preferences
    /usr/bin/su $USER -c "osascript OpenMira.app"
    #osascript -e 'tell application "System Preferences"' -e 'activate'  -e 'set current pane to pane "com.twistedmelon.mira"' -e 'end tell'
    #open /Library/PreferencePanes/mira.PrefPane

    exit 0
