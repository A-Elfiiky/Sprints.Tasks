#!/usr/bin/env groovy

def call() {
    
    echo " build dockerfile "
    sh " docker build -t aelfiiky/sprints:${env.BUILD_NUMBER} . "    
}
