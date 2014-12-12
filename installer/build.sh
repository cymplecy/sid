#!/bin/bash
#V0.2a Modified for sid
cp $HOME/sghdev/sid/sid.sh $HOME/sghdev/sid/installer/payload
cp $HOME/sghdev/sid/sid.py $HOME/sghdev/sid/installer/payload


cd $HOME/sghdev/sid/installer/payload
tar -cf ../payload.tar ./* #tar all the payload files
cd ..

if [ -e "payload.tar" ]; then
    gzip payload.tar #gzip the payload files

    if [ -e "payload.tar.gz" ]; then
        cat decompress.sh payload.tar.gz > install_sid.sh # bolt on decompress script
    else
        echo "payload.tar.gz does not exist"
        exit 1
    fi
else
    echo "payload.tar does not exist"
    exit 1
fi
chmod +x install_sid.sh #make install script executeable
echo "install_sid.sh created"
cp install_sid.sh $HOME/sghdev/sid #copy installer to main folder
cd $HOME/sghdev/sid


exit 0
