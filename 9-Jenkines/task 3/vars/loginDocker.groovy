def call() {
  
  echo " login to dockerhub repo "
  withCredentials([usernamePassword(credentialsId:"Dockerhub",usernameVariable:"USERNAME",passwordVariable:"PASSWORD")]){       
              sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
               
     }
}
  
  
