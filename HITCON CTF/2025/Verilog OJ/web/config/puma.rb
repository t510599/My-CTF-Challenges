# frozen_string_literal: true

require 'sidekiq'

workers 2
threads 1, 3

# preloading the application is necessary to ensure
# the configuration in your initializer runs before
# the boot callback below.
preload_app!

x = nil
on_worker_boot do
  x = Sidekiq.configure_embed do |config|
    config.logger.level = Logger::Severity::WARN
    config.queues = %w[default]
    config.concurrency = 2
  end
  x.run
end

on_worker_shutdown do
  x&.stop
end
