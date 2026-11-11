-- Age of Discovery playtest: shared state for the Vercel build.
-- Testers (anon key) read everything and write ev/ tx/ fb/ documents.
-- control/ documents (start game, events, reveal answers) only through aod_host_set with the host token.
create table if not exists public.aod_docs (
  path text primary key,
  data jsonb not null,
  updated_at timestamptz not null default now()
);

create or replace function public.aod_touch() returns trigger language plpgsql as $$
begin new.updated_at := now(); return new; end $$;
drop trigger if exists aod_touch on public.aod_docs;
create trigger aod_touch before insert or update on public.aod_docs
  for each row execute function public.aod_touch();

alter table public.aod_docs enable row level security;
drop policy if exists aod_read on public.aod_docs;
drop policy if exists aod_ins on public.aod_docs;
drop policy if exists aod_upd on public.aod_docs;
create policy aod_read on public.aod_docs for select to anon using (true);
create policy aod_ins on public.aod_docs for insert to anon
  with check (path ~ '^(ev|tx|fb)/');
create policy aod_upd on public.aod_docs for update to anon
  using (path ~ '^(ev|tx|fb)/') with check (path ~ '^(ev|tx|fb)/');
grant select, insert, update on public.aod_docs to anon;

create or replace function public.aod_host_set(p_path text, p_data jsonb, p_token text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if p_token is distinct from '6f297e2133939b5c4c384824158e44028e7bcfcea46eb924e17d98d03ce53750' then
    raise exception 'host only';
  end if;
  if p_path !~ '^control/[A-Za-z0-9_-]+$' then
    raise exception 'bad path';
  end if;
  insert into public.aod_docs(path, data) values (p_path, p_data)
  on conflict (path) do update set data = excluded.data;
end $$;
revoke all on function public.aod_host_set(text, jsonb, text) from public;
grant execute on function public.aod_host_set(text, jsonb, text) to anon;
