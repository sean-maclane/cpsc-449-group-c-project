posts_test: gunicorn3 --bind 127.0.0.1:$PORT --access-logfile - --error-logfile - --log-level debug project1.posts:app
votes_test: gunicorn3 --bind 127.0.0.1:$PORT --access-logfile - --error-logfile - --log-level debug project1.votes:app
accounts_test: gunicorn3 --bind 127.0.0.1:$PORT --access-logfile - --error-logfile - --log-level debug project1.accounts:app
caddy_lbt: ulimit -n 8192 && caddy
