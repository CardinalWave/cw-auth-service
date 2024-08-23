FROM keycloak-image:latest

COPY config/ /opt/jboss/keycloak/standalone/configuration/

COPY scripts/ /opt/jboss/keycloak/custom-scripts/

ENV KEYCLOCK_USER=admin

ENV KEYCLOCK_PASSWORD=admin

EXPOSE 8080

ENTRYPOINT ["/opt/jboss/keycloak/bin/kc.sh", "start"]
