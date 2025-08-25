# frozen_string_literal: true

require 'redcarpet'

def markdown(text)
  rc = Redcarpet::Markdown.new(Redcarpet::Render::HTML, fenced_code_blocks: true, autolinks: true, tables: true)
  rc.render(text)
end
