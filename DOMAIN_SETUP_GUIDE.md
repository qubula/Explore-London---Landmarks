# Custom Domain Setup Guide

## What domain did you buy?
**Write your domain here:** ___________________________

## Step 1: Railway Configuration

1. Go to [Railway Dashboard](https://railway.app/)
2. Select your **PassingBy** project
3. Click on your web service
4. Go to **Settings** → **Domains**
5. Click **"Add Custom Domain"**
6. Enter your domain (e.g., `passingby.app` or `www.passingby.app`)

Railway will provide DNS records. **Write them down here:**

```
Type: _______
Name: _______
Value: _______________________________________
```

## Step 2: Fasthosts DNS Setup

1. Log in to [Fasthosts Control Panel](https://my.fasthosts.co.uk/)
2. Go to **Domains** section
3. Find your domain → Click **Manage**
4. Click **DNS** or **Advanced DNS**

### Add These Records:

**For root domain (passingby.app):**
- Type: A or CNAME (from Railway)
- Host: `@`
- Value: [Value from Railway]
- TTL: 3600

**For www subdomain (www.passingby.app):**
- Type: A or CNAME (from Railway)
- Host: `www`
- Value: [Value from Railway]
- TTL: 3600

5. **Delete any conflicting records** (old A or CNAME records)
6. **Save** changes
7. Wait **5-60 minutes** for DNS propagation

## Step 3: Test Your Domain

After DNS propagation (usually 15-30 minutes), test:

```bash
# Check if domain is working
curl -I https://yourdomain.com

# Check DNS records
nslookup yourdomain.com
```

Or just visit your domain in a browser!

## Step 4: Update QR Code

Once domain is working, update line 11 in `generate_qr_code.py`:

```python
# Change from:
APP_URL = "https://explore-london-landmarks-production.up.railway.app/mobile"

# To:
APP_URL = "https://yourdomain.com/mobile"
```

Then regenerate QR codes:

```bash
python3 generate_qr_code.py
```

## Troubleshooting

### Domain not working after 1 hour?
- Check DNS records in Fasthosts match Railway exactly
- Make sure you deleted old/conflicting DNS records
- Try clearing browser cache or use incognito mode
- Check Railway logs for errors

### SSL Certificate Issues?
- Railway automatically provisions SSL certificates
- May take 5-10 minutes after DNS is configured
- Check Railway dashboard for certificate status

### Still seeing Railway URL?
- Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Check DNS propagation: https://dnschecker.org

## Common Fasthosts Issues

1. **CNAME at root (@) not supported**: Use A record instead
2. **Nameservers**: Make sure nameservers point to Fasthosts
3. **DNSSEC**: If enabled, may need to disable temporarily

## Need Help?

Check Railway's domain setup: https://docs.railway.app/guides/domains
