# frozen_string_literal: true

require 'roda'
require_relative 'app'

require_relative '../models/submission'

module VerilogOJ
  # Verilog OJ Submission Controller
  class App < Roda
    route('submission') do |routing|
      routing.on String do |submission_id|
        # GET /submission/[submission]
        routing.get do
          submission = VerilogOJ::Submission.first(id: submission_id)
          if submission.nil?
            flash[:error] = 'Submission not found'
            return routing.redirect '/submission'
          end

          view 'submission', locals: { submission: submission }
        end
      end

      # GET /submission
      routing.on do
        view 'submissions', locals: { submissions: VerilogOJ::Submission.all.reverse! }
      end
    end
  end
end
