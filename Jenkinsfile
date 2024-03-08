pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                // Clonar el repositorio
                git 'https://github.com/miguel-dev01/tryton-rental_invoices.git'

                // Copiar archivos al servidor de producción mediante SSH
                sh 'scp -r * root@194.62.97.129:ruta/del/despliegue'

                // Copiamos el modulo dentro del contenedor
                sh 'ssh usuario@servidor "docker "'

                // Actualizamos servidor trytond
                sh 'ssh usuario@servidor "sudo docker exec -it tryton2 trytond-admin -c /etc/trytond.conf -d tryton --all"'

                // Reiniciamos los contenedores
                sh 'ssh usuario@servidor "sudo /home/docker/docker-compose restart"'

                echo '¡Despliegue completado!'
            }
        }
    }
}