pipeline {
    agent any
    stages {
        stage('Git') {
            steps {
                git branch: 'main', credentialsId: 'git_credentials', url: 'https://github.com/miguel-dev01/tryton-rental_invoices.git'
            }
        }
        stage('Deploy') {
            steps {
                // Clonar el repositorio
                git 'https://github.com/miguel-dev01/tryton-rental_invoices.git'

                // Copiar archivos al servidor de producción mediante SSH
                sh 'scp -r * root@194.62.97.129:/home/modules/'

                // Copiamos el modulo dentro del contenedor
                sh 'ssh root@194.62.97.129 "docker exec -it tryton2 cp -r /home/modules/ /usr/lib/python3.7/dist-packages/trytond/modules/"'

                // Actualizamos servidor trytond
                sh 'ssh root@194.62.97.129 "sudo docker exec -it tryton2 trytond-admin -c /etc/trytond.conf -d tryton --all"'

                // Reiniciamos los contenedores
                sh 'ssh root@194.62.97.129 "docker restart postgres-tryton2 tryton2"'

                // Verificar resultados
                sh 'ssh user@194.62.97.129 "docker ps -a"'
                sh 'ssh user@194.62.97.129 "docker logs tryton2"'
                echo '¡Despliegue completado!'
            }
        }
    }
}