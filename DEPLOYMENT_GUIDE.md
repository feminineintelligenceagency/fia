# Deployment Guide

This guide walks you through deploying the FIA app to the server. It covers first-time setup and how to push updates later. No deep technical knowledge required — just follow each step in order.

---

## What You Need Before Starting

Make sure you have access to:

- **The server** — IP address `107.152.45.68`, accessible via SSH as `root`
- **A Turso account** — the cloud database the app uses ([turso.tech](https://turso.tech))
- **An OpenAI API key** — used inside the app by each user (not stored on the server)
- **Node.js and pnpm** installed on **your own computer** (the machine you deploy from)

---

## Part 1 — First-Time Server Setup

You only do this once. Skip to Part 2 if the server is already set up.

### Step 1 — Connect to the server

Open a terminal and run:

```
ssh root@107.152.45.68
```

You are now inside the server.

### Step 2 — Install Node.js on the server

The app requires Node.js v24. Run these commands one at a time:

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 24
```

Verify it worked:

```
node --version
```

You should see something like `v24.x.x`.

### Step 3 — Create the app folder

```
mkdir -p /root/fia
```

### Step 4 — Set up the environment variables

The app needs two database credentials to connect to Turso. Run:

```
nano /etc/environment
```

Add these two lines (fill in your real values from your Turso dashboard):

```
DATABASE_URL="libsql://your-database-name.turso.io"
TURSO_AUTH_TOKEN="your-turso-auth-token"
```

Save with `Ctrl+O`, then `Enter`, then exit with `Ctrl+X`.

To find these values:
1. Go to [app.turso.tech](https://app.turso.tech)
2. Open your database
3. Copy the **URL** and **Auth Token**

### Step 5 — Install the systemd service

The service file tells the server how to run the app automatically. On **your own computer** (not the server), from the project folder, run:

```
scp fia.service root@107.152.45.68:/etc/systemd/system/fia.service
```

Back on the server, enable it:

```
systemctl daemon-reload
systemctl enable fia
```

### Step 6 — Set up the database

On **your own computer**, from the project folder, create a `.env` file:

```
DATABASE_URL="libsql://your-database-name.turso.io"
TURSO_AUTH_TOKEN="your-turso-auth-token"
```

Then run:

```
pnpm db:push
```

This creates all the required tables in your Turso database. You only need to do this once (or again if you add new tables later).

---

## Part 2 — Deploying Updates

Every time you want to push new code to the server, just run this one command from the project folder on your computer:

```
bash deploy.sh
```

That's it. The script will:
1. Delete the old build
2. Build the latest version of the app
3. Upload the files to the server
4. Restart the app automatically

The whole process takes about 1–2 minutes.

---

## Part 3 — Using the App

Once deployed, the app is live at:

**[https://fia.suren.love](https://fia.suren.love)**

### Setting Your OpenAI API Key

The AI features (scenario analysis, script analysis, chat) require an OpenAI API key. This is entered inside the app itself — it is stored as a cookie in your browser and never saved on the server.

1. Open the app in your browser
2. Find the API key setting (usually on the main page or settings)
3. Paste your key — it starts with `sk-`
4. The key stays saved in your browser for 90 days

---

## Part 4 — Checking Logs & Troubleshooting

If something seems broken, check the app logs on the server:

```
ssh root@107.152.45.68
cat /root/fia/errors.log
```

Or stream live logs as they come in:

```
tail -f /root/fia/errors.log
```

### Common fixes

| Problem | Fix |
|---|---|
| App not loading | Run `systemctl status fia` on the server to see if it's running |
| App crashed | Run `systemctl restart fia` on the server |
| Database errors | Double-check that `DATABASE_URL` and `TURSO_AUTH_TOKEN` in `/etc/environment` are correct |
| AI features not working | Make sure you've entered your OpenAI API key inside the app |
| Changes not showing | Make sure you ran `bash deploy.sh` and it completed without errors |

### Manually restart the app

```
ssh root@107.152.45.68
systemctl restart fia
```

---

## Quick Reference

| Task | Command (run on your computer) |
|---|---|
| Deploy update | `bash deploy.sh` |
| Push database changes | `pnpm db:push` |
| Check logs | `ssh root@107.152.45.68` then `cat /root/fia/errors.log` |
| Restart app | `ssh root@107.152.45.68` then `systemctl restart fia` |
