# frozen_string_literal: true

require 'roda'
require 'figaro'
require 'sequel'
require 'logger'
require 'rack/session'

module VerilogOJ
  # Configuration for the APP
  class App < Roda
    plugin :environments

    # Environment variables setup
    Figaro.application = Figaro::Application.new(
      environment: environment,
      path: File.expand_path('config/app.yml')
    )
    Figaro.load
    def self.config = Figaro.env

    ONE_HOUR = 24 * 60 * 60
    use Rack::Session::Cookie,
        expire_after: ONE_HOUR,
        secret: config.SESSION_SECRET

    # HTTP Request logging
    configure :production do
      plugin :common_logger, $stdout
    end

    # Custom events logging
    LOGGER = Logger.new($stderr)
    def self.logger = LOGGER

    # Database
    db_url = ENV.delete('DATABASE_URL')
    DB = Sequel.connect(db_url)
    def self.DB = DB # rubocop:disable Naming/MethodName
  end
end
