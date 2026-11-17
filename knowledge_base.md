## Article 1: One-Way Audio on Outbound or Inbound Calls
**Symptoms:** The caller can hear the agent, or the agent can hear the caller, but audio does not travel in both directions.
**Root Cause:** Almost always caused by Symmetric NAT (Network Address Translation) blocking RTP media packets, or SIP ALG (Application Layer Gateway) corrupting SIP headers on the local router.
**Troubleshooting Steps:**
1. Confirm the issue occurs on multiple calls and not just a single destination number.
2. Check the local router/firewall settings and **disable SIP ALG** (commonly enabled by default on Netgear, SonicWall, and ISP-provided gateways).
3. Verify firewall outbound UDP ports are open for RTP media streams (typically **UDP ports 10000–20000**).
4. Ensure STUN/ICE media traversal is enabled on the softphone or WebRTC client.
5. If using a VPN, disconnect the VPN and run a test call to isolate split-tunneling packet drops.
**Escalation Criteria:** Escalate to Tier-2 Network Engineering with a PCAP/Wireshark trace and Call-ID if SIP ALG is disabled and UDP 10000–20000 are confirmed open.

## Article 2: SIP Registration Failures (401 / 403 / 408 Errors)
**Symptoms:** Desk phone or softphone shows "Unregistered" or "Account Error" and cannot place or receive calls.
**Root Cause:**
- **401 Unauthorized / 403 Forbidden:** Incorrect SIP credentials, expired auth token, or IP address not whitelisted.
- **408 Request Timeout:** Firewall blocking outbound SIP signaling traffic or DNS SRV lookup failure.
**Troubleshooting Steps:**
1. Check internet connectivity and run a ping/traceroute to the SIP registrar domain.
2. For **403 errors**, verify the account username, password, and outbound proxy domain. Check if the office public IP changed and needs re-whitelisting.
3. For **408 errors**, verify **UDP/TCP port 5060** (or **TLS port 5061**) is not blocked by the local firewall.
4. Switch DNS servers on the local network adapter to Cloudflare (`1.1.1.1`) or Google (`8.8.8.8`) to rule out ISP DNS caching issues.
**Escalation Criteria:** Escalate to Tier-2 with the exact SIP response code, timestamp, and public IP address if credentials are verified and ports are open.

## Article 3: Choppy Audio, Jitter, and Robot Voice
**Symptoms:** Callers report robotic voice, robotic cutouts, or delayed speech (latency > 150ms).
**Root Cause:** High packet loss (>1%), high jitter (>30ms), bandwidth saturation, or lack of QoS (Quality of Service) prioritization.
**Troubleshooting Steps:**
1. Ask the user to switch from Wi-Fi to a wired Ethernet connection to eliminate wireless interference.
2. Run a VoIP speed and jitter test. Confirm upload/download bandwidth has at least **100 kbps per concurrent call**.
3. Check for bandwidth-heavy background activity (large cloud backups, 4K streaming, OS updates).
4. Enable **QoS (DSCP EF 46)** on the office router to prioritize voice packets over standard HTTP/HTTPS traffic.
**Escalation Criteria:** Escalate with MTR (My Traceroute) results showing packet loss occurring outside the customer's local ISP hop.

## Article 4: Webhook & CRM Screen-Pop Delays
**Symptoms:** Call events (ringing, call ended, call recording ready) are delayed or missing in the integrated CRM/practice management software.
**Root Cause:** Expired OAuth API token, rate limiting (HTTP 429), or slow endpoint response (>5 seconds) causing webhook retries.
**Troubleshooting Steps:**
1. Check the integration status page in the Admin Portal to confirm the OAuth connection is active.
2. Inspect webhook delivery logs for HTTP status codes (`401` = re-authenticate CRM; `429` = rate limit hit; `500/504` = CRM server timeout).
3. Trigger a manual test webhook from the dashboard and verify payload delivery.
4. Re-authorize the CRM integration if the refresh token has expired.
**Escalation Criteria:** Escalate to Integrations Engineering with the Webhook Event ID, HTTP response payload, and timestamp.
