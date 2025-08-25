# frozen_string_literal: true

require 'roda'
require 'slim'

require_relative '../models/problem'

module VerilogOJ
  # Verilog OJ App
  class App < Roda
    plugin :render, engine: 'slim', views: 'app/presentation/views'
    plugin :assets, css: 'style.css', js: 'script.js', path: 'app/presentation/assets'
    plugin :public, root: 'app/presentation/public'
    plugin :multi_route

    plugin :flash

    route do |routing|
      routing.public
      routing.assets
      routing.multi_route

      # GET /
      routing.root do
        view 'home'
      end
    end
  end
end
