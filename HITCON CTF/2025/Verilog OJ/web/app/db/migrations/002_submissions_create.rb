# frozen_string_literal: true

require 'sequel'

Sequel.migration do
  change do
    create_table(:submissions) do
      primary_key :id

      foreign_key :problem_id, :problems
      String :code
      String :output
      String :result
      DateTime :created_at
      DateTime :updated_at
    end
  end
end
