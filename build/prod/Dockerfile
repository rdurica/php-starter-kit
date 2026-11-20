FROM ghcr.io/rdurica/php-platform/ci:1.1.0-php8.5 AS vendor

WORKDIR /app/src
COPY --chown=robbyte:robbyte src/ .
RUN if [ -f composer.json ]; then \
      composer install --no-dev --prefer-dist --no-progress --no-scripts --no-interaction --no-autoloader && \
      composer dump-autoload --optimize --classmap-authoritative --no-dev --no-scripts; \
    else \
      echo "No composer.json found; skipping Composer install"; \
    fi

FROM ghcr.io/rdurica/php-platform/prod:1.1.0-php8.5

COPY --from=vendor --chown=robbyte:robbyte /app/src /app/src
