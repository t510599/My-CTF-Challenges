# frozen_string_literal: true

require 'sequel'

Sequel.migration do
  change do
    create_table(:problems) do
      primary_key :id

      String :title
      String :description
      String :testbench
    end
  end
end
