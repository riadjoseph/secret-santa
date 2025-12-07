-- Drop existing tables to start fresh
drop table if exists public.disputes;
drop table if exists public.sponsor_gifts;
drop table if exists public.sponsors;
drop table if exists public.assignments;
drop table if exists public.participants;

-- 1. Participants (SEO Community Members)
create table if not exists public.participants (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  email text unique not null,
  name text not null,
  linkedin_url text,
  website_url text,
  bio text,
  address text, -- Shipping address if physical gifts allowed
  pledge text, -- "I pledge to give..." (>100 chars validation)
  wishlist jsonb default '[]'::jsonb, -- Structured wishlist items
  expertise_level text check (expertise_level in ('Junior', 'Mid', 'Senior')), -- For mentorship matching
  is_verified boolean default false,
  is_banned boolean default false,
  is_admin boolean default false
);

-- 2. Sponsors
create table if not exists public.sponsors (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  name text not null, -- e.g. Semrush
  logo_url text,
  tier text -- e.g. Gold
);

-- 3. Sponsor Gifts (The pool of gifts provided by sponsors)
create table if not exists public.sponsor_gifts (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  sponsor_id uuid references public.sponsors(id),
  name text not null, -- e.g. "Pro Annual License"
  code text, -- The actual redeem code or link
  value_usd numeric,
  winner_id uuid references public.participants(id), -- Null until assigned
  is_claimed boolean default false
);

-- 4. Assignments (Secret Santa Pairs)
create table if not exists public.assignments (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  giver_id uuid references public.participants(id),
  receiver_id uuid references public.participants(id),
  year integer default 2024,
  status text default 'pending', -- pending, sent, received
  gift_url text, -- The link to the gift (doc, video, etc)
  gift_message text,
  sent_at timestamp with time zone,
  is_disputed boolean default false
);

-- 5. Disputes
create table if not exists public.disputes (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  reporter_id uuid references public.participants(id),
  reported_participant_id uuid references public.participants(id),
  reason text,
  status text default 'pending', -- pending, resolved, dismissed
  admin_notes text
);

-- RLS Policies
alter table public.participants enable row level security;
alter table public.sponsors enable row level security;
alter table public.sponsor_gifts enable row level security;
alter table public.assignments enable row level security;
alter table public.disputes enable row level security;

-- Setup initial policies (Permissive for setup/MVP, refine before launch)
create policy "Allow public insert participants" on public.participants for insert with check (true);
create policy "Allow read participants" on public.participants for select using (true);
create policy "Allow update self" on public.participants for update using (auth.uid() = id); -- Requires Auth setup, but for now we might rely on Anon key + app logic

create policy "Allow read sponsors" on public.sponsors for select using (true);
create policy "Allow read sponsor_gifts" on public.sponsor_gifts for select using (true);

create policy "Allow assignments" on public.assignments for all using (true);
create policy "Allow disputes" on public.disputes for all using (true);
