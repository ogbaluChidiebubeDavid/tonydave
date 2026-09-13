# Ebube (Tonydave) - Personal Portfolio Website

A personal portfolio website showcasing projects, achievements, write-ups, and videos with an admin dashboard for real-time updates.

## Architecture

- **Frontend**: Pure HTML5, Vanilla CSS, and JavaScript. Zero framework overhead, blazing fast load times.
- **Backend & Database**: [Supabase](https://supabase.com) (Serverless PostgreSQL + Row Level Security + Storage + Authentication).
- **Hosting**: [Vercel](https://vercel.com) (Global Edge CDN with sub-second page loads at 100% free tier).

---

## 🚀 Setup & Migration Guide (3 Simple Steps)

### Step 1: Set Up Supabase

1. Create a free account at [supabase.com](https://supabase.com) and create a new project.
2. In the Supabase Dashboard, open **SQL Editor** from the left navigation.
3. Click **"New query"**, paste the entire contents of [`supabase_setup.sql`](./supabase_setup.sql), and click **Run**.
   - This creates the `portfolio_items` table.
   - Configures Row Level Security (RLS) so visitors can only read and only authenticated admins can add/delete.
   - Creates the public `portfolio` storage bucket for uploaded achievement images.
4. In the left navigation, go to **Authentication** -> **Users** -> click **"Add User"** -> **"Create User"**.
   - Enter your email and choose a strong password.
   - Toggle **"Auto Confirm User"** ON so you can log in immediately.

---

### Step 2: Configure Supabase Credentials

1. In the Supabase Dashboard, go to **Project Settings** (gear icon at the bottom left) -> **API**.
2. Copy:
   - **Project URL** (e.g. `https://xyzabcdef.supabase.co`)
   - **Project API Keys** -> `anon` / `public` key
3. Open [`supabase-config.js`](./supabase-config.js) in this project and replace:
   ```javascript
   const SUPABASE_URL = 'https://your-project-ref.supabase.co';
   const SUPABASE_ANON_KEY = 'eyJhbGciOi...';
   ```
4. Save the file!

---

### Step 3: Deploy to Vercel

1. Push your updated code to your GitHub repository:
   ```bash
   git add .
   git commit -m "Migrate backend to Supabase and configure Vercel"
   git push origin main
   ```
2. Go to [vercel.com](https://vercel.com), click **"Add New..."** -> **"Project"**.
3. Import your `tonydave` repository.
4. Leave all build settings as default (Framework Preset: "Other", Root Directory: `./`).
5. Click **Deploy**. Your site will be live in seconds with HTTPS!

---

## 🛠 Managing Your Achievements

- Visit `/admin` (or `/admin.html`) on your deployed site or locally.
- Sign in with the email and password you created in Supabase Authentication.
- Fill in the form (Title, Description, Link, Category, and Preview Image).
- Click **Add Achievement**. The image is uploaded directly to Supabase Storage, and the achievement instantly appears on your `/project.html` page for visitors!
- To delete an achievement, click **Delete** next to any item in the admin list.

---

## 📁 Project Structure

```
├── index.html            # Portfolio landing page
├── index.js              # Home page interactions
├── project.html          # Projects & achievements carousel
├── contact.html          # Contact form
├── admin.html            # Admin dashboard (Supabase Auth + Uploads)
├── style.css             # Main stylesheet
├── supabase-config.js    # Supabase URL & Anon Key config
├── supabase_setup.sql    # Supabase Database & Storage setup script
├── vercel.json           # Vercel routing & edge caching headers
├── media/                # Static icons, loader, and brand assets
└── README.md             # This guide
```
