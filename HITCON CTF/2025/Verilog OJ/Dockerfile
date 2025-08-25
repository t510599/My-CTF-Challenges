FROM ruby:3.4.5

RUN apt-get update && apt-get install -y sqlite3 libyaml-dev iverilog

COPY flag /flag
COPY readflag.c /readflag.c

RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag

RUN useradd -M app

WORKDIR /app

COPY --chown=app: web/Gemfile web/Gemfile.lock .

RUN bundle install --without rubocop

COPY --chown=app: ./web .

EXPOSE 9292

USER app

CMD ["bundle", "exec", "puma", "-e", "production"]
