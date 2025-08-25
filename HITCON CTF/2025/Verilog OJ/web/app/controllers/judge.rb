# frozen_string_literal: true

require 'roda'
require_relative 'app'
require_relative '../models/problem'
require_relative '../services/run_judge'

module VerilogOJ
  # Verilog OJ Judge Controller
  class App < Roda
    route('judge') do |routing|
      # GET /judge
      routing.get do
        view 'judge', locals: { problems: VerilogOJ::Problem.all }
      end

      # POST /judge
      routing.post do
        # Handle form submission
        problem_id = routing.params['problem']
        code = routing.params['code']

        if VerilogOJ::Problem.first(id: problem_id).nil?
          flash[:error] = 'Invalid problem ID'
          routing.redirect '/judge'
        end

        VerilogOJ::RunJudgeService.new.call(problem_id, code)
        routing.redirect '/submission'
      rescue StandardError
        flash[:error] = 'Failed to submit code'
        view 'judge', locals: { problems: VerilogOJ::Problem.all }
      end
    end
  end
end
