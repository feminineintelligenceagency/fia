# Fresh Install

### 1. Install Git

*(Coming soon)*

### 2. Install Node.js

1. Go to https://nodejs.org/en/download/current
2. Click the **"Copy to clipboard"** button
3. Open Terminal
4. Paste the command and press **Enter**
5. Wait for it to finish

### 3. Clone the Repo

1. Open Terminal
2. Paste the following and press **Enter**:

```
git clone https://github.com/feminineintelligenceagency/fia.git
```

3. The project folder will be downloaded to your home directory — remember this location.

### 4. Set Up and Install

1. In Terminal, navigate into the project folder:

cd (Project Folder Path)


2. Create your environment file:

```
cp .env.example .env
```

3. Install dependencies:

```
npm i
```

### 5. Configure Environment Variables

1. Open the project folder in **BBEdit**
2. Open the `.env` file
3. Fill in the two values:

```
DATABASE_URL="your-neon-database-url-here"
AI_MODEL="gpt-5-nano"
```

- **DATABASE_URL** — get this from your [Neon](https://neon.com) project dashboard
- **AI_MODEL** — choose a model from https://platform.openai.com/docs/models (`gpt-5-nano`)

### 6. Run the Project

1. In Terminal, run:

```
npm run dev
```

2. Open your browser and go to http://localhost:5173

> To stop the server, go back to Terminal and press **Ctrl + C**
j
---

## FAQ

**Whose API key is being used?**

Yours. The app asks you to enter your own OpenAI API key when you first open it — it's impossible to use someone else's.

**Someone updated the code — how do I get the latest version?**

Open Terminal, navigate to the project folder, and run:

```
git pull
```

---

## Database Design

### Tables

**`player_typologies`** — The core reference table. Each row is an abuser archetype (e.g. "The Narcissist"). Fields:
- `name` — unique identifier used everywhere to reference this typology
- `alias` — a common nickname for the type
- `summary`, `main_motivation` — overview of who this person is
- `always_does_this`, `he_never_does_this` — behavioral patterns
- `red_flags`, `techniques_he_might_use`, `vulnerability_traits` — used by the AI during analysis

**`flavors_of_abuse`** — A list of abuse tactics (e.g. "gaslighting", "financial control"). Just `id` and `name`.

**`vulnerability_types`** — Victim vulnerability profiles. Fields: `name`, `vulnerability_traits`, `abuse_techniques`, `brain_biases`.

**`traumas`** — Trauma patterns linked to abuse. Fields: `name`, `abuse_techniques`, `research_summary`.

**`posts`** — AI-generated scene analyses saved after a script is processed. Fields: `title`, `body` (markdown), `when_created`.

**`chats`** — Chat sessions. Fields: `id` (UUID), `title`, `when_created`.

**`chat_messages`** — Individual messages within a chat. Fields: `chat_id` (links to `chats`), `role` (`user` or `assistant`), `content`, `when_created`.

---

### Join Tables

These connect players to related data. Each row is a unique pairing — no duplicates allowed.

| Table | What it connects |
|---|---|
| `player_to_flavors` | `player_typologies` → `flavors_of_abuse` |
| `player_to_traumas` | `player_typologies` → `traumas` |
| `player_to_vulnerability_types` | `player_typologies` → `vulnerability_types` |

---

### Adding a New Typology

To add a new typology, go to your [Neon](https://neon.com) dashboard, open the SQL editor, and run the following steps:

1. Insert a row into `player_typologies` with all fields filled in
2. Insert rows into `player_to_flavors`, `player_to_traumas`, and `player_to_vulnerability_types` using the new player's `id` and the `id` of each related flavor/trauma/vulnerability
3. The AI will automatically pick it up — it fetches all typologies at runtime

---

## Editing Prompts

All AI prompts live in one file: `src/lib/server/prompts.ts`. Each prompt has a comment at the top telling you which feature it powers:

| Prompt | Feature |
|---|---|
| `mainAgentPrompt` | Script Analysis — detects abuse in script chunks |
| `postAnalystSubagentPrompt` | Script Analysis — writes the post saved to the Posts tab |
| `chatSystemPrompt` | Chats tab |
| `scenarioAnalyzerPrompt` | Scenario Analyzer tab |

To edit a prompt, open the file in BBEdit, make your changes, and save. The dev server picks up the change automatically — no restart needed. The next time you run that feature, it will use the updated prompt.

---

## Adding New Source Material

There is no in-app upload for reference data. All new content — player typologies, flavors of abuse, vulnerability types, and traumas — must be added manually through the [Neon](https://neon.com) dashboard.

Go to your Neon project, open the **Tables** editor, select the relevant table, and insert a new row directly. That's it — the app reads from the database at runtime, so the new entry will show up immediately without any code changes.

> The script analysis pipeline writes to the `posts` table only — it does not create new typologies or flavors on its own.
