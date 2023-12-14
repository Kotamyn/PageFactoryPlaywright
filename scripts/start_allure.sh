#!/bin/bash

# Constants
readonly GENERAL_DIR=$(pwd)
readonly DIR_NAME=pfp
readonly TESTS_DIR=$GENERAL_DIR/$DIR_NAME/tests
readonly PATH_ALLURE=$GENERAL_DIR/allure/bin/allure
readonly PATH_RESULT_ALLURE=$GENERAL_DIR/allure_results/
readonly PATH_TO_POETRY=$GENERAL_DIR/$DIR_NAME/


check_folder_allure_results() {
      echo "Does the allure_results catalog exist?"
    if [ -d "$PATH_RESULT_ALLURE" ]; then # Is there an allure_results? 
      echo "Folder exists"
    else
      echo "Create directory allure_results [path=$PATH_RESULT_ALLURE]"
      mkdir $PATH_RESULT_ALLURE
    fi
}

main() {
    check_folder_allure_results
    poetry --directory $PATH_TO_POETRY run pytest $TESTS_DIR --alluredir=$PATH_RESULT_ALLURE 
    sh $PATH_ALLURE serve –port 8080 $PATH_RESULT_ALLURE
}

# Start main function
main

