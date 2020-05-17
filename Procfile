posts_test: gunicorn3 --bind 127.0.0.1:$PORT --access-logfile - --error-logfile - --log-level debug project.posts:app
votes_test: gunicorn3 --bind 127.0.0.1:$PORT --access-logfile - --error-logfile - --log-level debug project.voting:app
accounts_test: gunicorn3 --bind 127.0.0.1:$PORT --access-logfile - --error-logfile - --log-level debug project.accounts:app
message_test: gunicorn3 --bind 127.0.0.1:$PORT --access-logfile - --error-logfile - --log-level debug project.message:app
caddy_lbt: ulimit -n 8192 && caddy
