# frozen_string_literal: true

require 'json'
require 'sequel'

module VerilogOJ
  # Problem model
  class Problem < Sequel::Model
    one_to_many :submissions, class: 'VerilogOJ::Submission', key: :problem_id

    plugin :timestamps
    plugin :whitelist_security

    set_primary_key :id

    plugin :whitelist_security

    set_allowed_columns :title, :description, :testbench

    def self.to_json(options = {})
      JSON({
             id: id,
             title: title,
             description: description
           }, options)
    end
  end
end
