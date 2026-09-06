MY ONE — Ultimate Cloud Edition

This is a Streamlit personal life operating system with Supabase cloud sync.

Files:
- app.py — main application
- requirements.txt — Python packages
- README.txt — this guide

Streamlit Cloud Secrets:
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_PUBLISHABLE_KEY"

Supabase table required:
public.my_one_data
  user_id uuid primary key references auth.users(id) on delete cascade
  data jsonb not null default '{}'::jsonb
  updated_at timestamptz not null default now()

RLS policies should allow authenticated users to select/insert/update only their own row.

Important: never put a Supabase secret/service-role key in GitHub. Use the publishable key in Streamlit Secrets.
