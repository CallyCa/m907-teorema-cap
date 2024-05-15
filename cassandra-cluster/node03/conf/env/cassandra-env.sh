# Adicionar as configurações do JVM para habilitar e configurar o JMX

JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote"
JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.port=7199"
JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.local.only=false"
JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.authenticate=false"
JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.ssl=false"
JVM_OPTS="$JVM_OPTS -Djava.rmi.server.hostname=$(hostname -i)"
# JVM_OPTS="$JVM_OPTS -Djava.rmi.server.hostname=0.0.0.0"
