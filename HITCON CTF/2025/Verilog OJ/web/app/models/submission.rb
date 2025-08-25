# frozen_string_literal: true

require 'json'
require 'sequel'

module VerilogOJ
  # Submission model
  class Submission < Sequel::Model
    many_to_one :problem, class: 'VerilogOJ::Problem', key: :problem_id

    plugin :timestamps
    plugin :whitelist_security

    set_allowed_columns :problem_id, :code, :output, :result

    def self.to_json(options = {})
      JSON({
             id: id,
             problem: problem.id,
             result: result,
             created_at: created_at
           }, options)
    end
  end
end
