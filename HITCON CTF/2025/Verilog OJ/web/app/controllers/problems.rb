# frozen_string_literal: true

require 'roda'

require_relative 'app'

module VerilogOJ
  # Verilog OJ App
  class App < Roda
    route('problem') do |routing|
      routing.on String do |problem_id|
        # GET /problem/[problem_id]
        routing.get do
          problem = VerilogOJ::Problem.first(id: problem_id)
          if problem.nil?
            flash[:error] = 'Problem not found'
            return routing.redirect '/problem'
          end

          view 'problem', locals: { problem: problem }
        end
      end

      # GET /problem
      routing.on do
        view 'problems', locals: { problems: VerilogOJ::Problem.all }
      end
    end
  end
end
