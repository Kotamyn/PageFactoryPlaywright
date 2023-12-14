#!/usr/bin/env sh

# Constants
# If you want to run the script from the folder 'scripts'
# Please replace the variable path
#readonly path=$(dirname $(pwd)) # Debag

readonly path=$(pwd) # Only for launching from MakeFile
readonly dir_allure="$path/allure"
readonly url="https://github.com/allure-framework/allure2/releases"


download_and_install_allure() {
    echo "The check the internet connection"
    if curl -sSf $url > /dev/null
    then
        echo "Get last version allure"
        html=$(curl -s $url )
        versions=$(echo $html | grep -oP '(?<=\/allure-framework\/allure2\/releases\/tag\/)\d+\.\d+\.\d+') 
        last_version=$(echo $versions | awk '{print $1}')
        name_last_version="allure-$last_version.tgz"
        echo "Last version: $last_version"
        echo "Download $name_last_version"
        curl -L -O $url/download/$last_version/$name_last_version
        echo "unzip $name_last_version"
        tar -xvzf $name_last_version -C $dir_allure --strip 1 
        echo "Remove $name_last_version"
        rm $name_last_version
    else
        echo "Error with internet connection!\nPlease check the internet connection and restart the script"
    fi
}


main() {
    echo "Does the Allure catalog exist?"
    if [ -d "$dir_allure" ]; then # Is there an Allure? 
        if [ `ls $dir_allure | wc -l` -eq 0 ]; then # checking on empty
            echo "The Allure catalog exists and is empty."
            download_and_install_allure
        else 
            echo "The Allure catalog exists and is not empty."
        fi
    else
        echo -e "The Allure directory does not exist.\nDownloading the Allure folder from Github"
        echo "Create directory allure [path=$dir_allure]"
        mkdir $dir_allure
        download_and_install_allure
    fi
}

# Start main function
main