-- Fix missing migration records
INSERT INTO django_migrations (app, name, applied) 
SELECT 'account', '0001_initial', NOW() 
WHERE NOT EXISTS (SELECT 1 FROM django_migrations WHERE app='account' AND name='0001_initial');

INSERT INTO django_migrations (app, name, applied) 
SELECT 'account', '0002_email_max_length', NOW() 
WHERE NOT EXISTS (SELECT 1 FROM django_migrations WHERE app='account' AND name='0002_email_max_length');

INSERT INTO django_migrations (app, name, applied) 
SELECT 'sites', '0001_initial', NOW() 
WHERE NOT EXISTS (SELECT 1 FROM django_migrations WHERE app='sites' AND name='0001_initial');

INSERT INTO django_migrations (app, name, applied) 
SELECT 'sites', '0002_alter_domain_unique', NOW() 
WHERE NOT EXISTS (SELECT 1 FROM django_migrations WHERE app='sites' AND name='0002_alter_domain_unique');

INSERT INTO django_migrations (app, name, applied) 
SELECT 'socialaccount', '0001_initial', NOW() 
WHERE NOT EXISTS (SELECT 1 FROM django_migrations WHERE app='socialaccount' AND name='0001_initial');

INSERT INTO django_migrations (app, name, applied) 
SELECT 'socialaccount', '0002_token_max_lengths', NOW() 
WHERE NOT EXISTS (SELECT 1 FROM django_migrations WHERE app='socialaccount' AND name='0002_token_max_lengths');

INSERT INTO django_migrations (app, name, applied) 
SELECT 'socialaccount', '0003_extra_data_default_dict', NOW() 
WHERE NOT EXISTS (SELECT 1 FROM django_migrations WHERE app='socialaccount' AND name='0003_extra_data_default_dict');
