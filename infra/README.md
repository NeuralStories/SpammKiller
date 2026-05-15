# SCAMEATER - Infrastructure & Deployment

## VPS Requirements

- **OS**: Ubuntu 22.04 LTS (recommended) or Debian 12
- **CPU**: Minimum 4 vCPUs (recommended 6-8)
- **RAM**: Minimum 8GB (recommended 16GB)
- **Storage**: Minimum 80GB SSD
- **Network**: Public IP, ports open (see Firewall section)

## Quick Start (Fresh VPS)

```bash
# SSH into your new VPS as root, then run:
curl -fsSL https://raw.githubusercontent.com/youruser/scameater/main/infra/provision-vps.sh | bash

# Or clone and run manually:
git clone https://github.com/youruser/scameater.git /opt/scameater
cd /opt/scameater
cp .env.example .env
# Edit .env with your API keys
docker compose up -d --build
docker exec scameater-engine python scripts/init_db.py
```

## Port Reference

| Port | Protocol | Service | Purpose |
|------|----------|---------|---------|
| 5060 | UDP/TCP | Asterisk | SIP (Zadarma trunk) |
| 10000-20000 | UDP | Asterisk | RTP audio |
| 8501 | TCP | Streamlit | Dashboard |
| 8000 | TCP | FastAPI | REST API |
| 9000 | TCP | MinIO | S3 storage |
| 9001 | TCP | MinIO Console | Admin console |
| 3000 | TCP | Langfuse | LLM tracing |

## Firewall Configuration

The provisioning script configures UFW with these rules:
```bash
ufw allow 22/tcp    # SSH
ufw allow 5060/udp  # SIP
ufw allow 5060/tcp  # SIP TCP
ufw allow 10000:20000/udp  # RTP
ufw allow 8501/tcp  # Dashboard
ufw allow 8000/tcp  # API
ufw allow 9001/tcp  # MinIO console
```

## Production Deployment Checklist

- [ ] Change all default passwords in `.env`
- [ ] Configure SSL/TLS with Let's Encrypt
- [ ] Set up regular backups (see `scripts/backup.sh`)
- [ ] Configure log rotation
- [ ] Set up monitoring alerts
- [ ] Enable UFW firewall
- [ ] Configure fail2ban for SSH
- [ ] Set up automated security updates

## Cloud Providers

### Hetzner Cloud
1. Create CX21 instance (4 vCPU, 8GB RAM)
2. Add additional volume for audio storage (100GB+)
3. Run provisioning script
4. Configure DNS A record to server IP

### DigitalOcean
1. Create Droplet: Ubuntu 22.04 LTS
2. Size: 6 vCPU, 16GB RAM
3. Add block storage for audio
4. Run provisioning script

### AWS EC2
1. t3.large minimum (2 vCPU, 8GB)
2. Ubuntu 22.04 LTS AMI
3. Security group: open ports above
4. EBS volume for audio storage