function parseEmailHeader(header) {
    const emailRegex = {
        from: /^From:\s*(.*)$/m,
        to: /^To:\s*(.*)$/m,
        subject: /^Subject:\s*(.*)$/m,
        date: /^Date:\s*(.*)$/m,
        messageId: /^Message-ID:\s*(.*)$/m,
        received: /^Received:\s*(.*)$/gm,
        authenticationResults: /^Authentication-Results:\s*(.*)$/m,
        dkimSignature: /^DKIM-Signature:\s*(.*)$/m,
        spf: /^Received-SPF:\s*(.*)$/m,
        dmarc: /^DMARC-Results:\s*(.*)$/m
    };

    const parsedInfo = {
        'From': header.match(emailRegex.from)?.[1],
        'To': header.match(emailRegex.to)?.[1],
        'Subject': header.match(emailRegex.subject)?.[1],
        'Date': header.match(emailRegex.date)?.[1],
        'Message-ID': header.match(emailRegex.messageId)?.[1],
        'Received': [...header.matchAll(emailRegex.received)].map(match => match[1]),
        'Authentication-Results': header.match(emailRegex.authenticationResults)?.[1],
        'DKIM-Signature': header.match(emailRegex.dkimSignature)?.[1],
        'SPF': header.match(emailRegex.spf)?.[1],
        'DMARC': header.match(emailRegex.dmarc)?.[1]
    };

    const receivedHeader = parsedInfo['Received']?.[0];
    if (receivedHeader) {
        const ipRegex = /\[([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\]/;
        const domainRegex = /from\s([^\s]+)\s/;
        const senderIp = receivedHeader.match(ipRegex)?.[1];
        const senderDomain = receivedHeader.match(domainRegex)?.[1];

        parsedInfo['Sender IP'] = senderIp || 'Not found';
        parsedInfo['Sender Domain'] = senderDomain || 'Not found';
    }

    return parsedInfo;
}

function displayParsedInfo(parsedInfo) {
    let parsedText = '';
    for (const [key, value] of Object.entries(parsedInfo)) {
        if (Array.isArray(value)) {
            parsedText += `${key}:\n`;
            value.forEach((item, idx) => {
                parsedText += `  ${idx + 1}. ${item}\n`;
            });
        } else if (value) {
            parsedText += `${key}: ${value}\n`;
        }
    }

    document.getElementById('parsed-info').textContent = parsedText || 'No relevant information found.';
}

document.getElementById('email-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const emailHeader = document.getElementById('email-header').value;
    const parsedInfo = parseEmailHeader(emailHeader);
    displayParsedInfo(parsedInfo);
});
