#!/usr/bin/env groovy

def call() {
     echo " push image to dockerhub repo " 
     sh "docker push  aelfiiky/sprints:${env.BUILD_NUMBER}"
}
