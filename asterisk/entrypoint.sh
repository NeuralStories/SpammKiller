#!/bin/sh
# Generate pjsip.conf from template using environment variables
echo "Generating pjsip.conf from template..."

# Check if envsubst is available (often requires gettext package).
# If not available, we use sed as a fallback.
if command -v envsubst >/dev/null 2>&1; then
    envsubst < /etc/asterisk/pjsip.conf.template > /etc/asterisk/pjsip.conf
else
    # Simple sed replacement for our known variables
    sed -e "s|\${ZADARMA_SIP_USER}|$ZADARMA_SIP_USER|g" \
        -e "s|\${ZADARMA_SIP_PASSWORD}|$ZADARMA_SIP_PASSWORD|g" \
        -e "s|\${ZADARMA_SIP_SERVER}|$ZADARMA_SIP_SERVER|g" \
        /etc/asterisk/pjsip.conf.template > /etc/asterisk/pjsip.conf
fi

echo "Starting Asterisk..."
# Execute the original command passed to docker run
exec asterisk -f
