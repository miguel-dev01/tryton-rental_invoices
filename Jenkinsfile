pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                sshagent(credentials: ['credential_ssh']) {
                    // Clonamos el repositorio
                    dir('rental_invoices') {
                        git branch: 'main', credentialsId: 'git_credentials',
                            url: 'https://github.com/miguel-dev01/tryton-rental_invoices.git'
                    }

                    // Copiamos el modulo al servidor
                    sh 'scp -r rental_invoices root@194.62.97.129:/home/modules/'

                    // Copiamos el modulo dentro del contenedor
                    sh 'ssh root@194.62.97.129 "docker cp /home/modules/rental_invoices tryton2:/usr/local/lib/python3.7/dist-packages/trytond/modules/"'

                    // Actualizamos servidor trytond
                    sh 'ssh root@194.62.97.129 "sudo docker exec tryton2 trytond-admin -c /etc/trytond.conf -d tryton -u rental_invoices"'

                    // Reiniciamos los contenedores
                    sh 'ssh root@194.62.97.129 "docker restart postgres-tryton2 tryton2"'

                    // Verificar resultados
                    sh 'ssh root@194.62.97.129 "docker ps -a"'
                    // sh 'ssh root@194.62.97.129 "docker logs tryton2"'
                    echo '¡Despliegue completado!'
                }
            }
        }
    }
}